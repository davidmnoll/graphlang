import './style.css'
import { dump as toYaml, load as fromYaml } from 'js-yaml'

type Hash = string
type Edge = [Hash, Hash]
type EdgeList = Edge[]
type NodeStore = Record<Hash, EdgeList | null>

type IndexedEdge = [number, number]
type IndexedNode = IndexedEdge[]

type IndexedGraph = {
  nodes: IndexedNode[]
  ids: number[]
  idToHash: Hash[]
  hashToId: Record<Hash, number>
  idToIndex: Record<number, number>
  roots: number[]
}

interface FosState {
  store: NodeStore
  indexed: IndexedGraph
  actors: Record<string, number>
  currentActor: string
}

declare global {
  interface Window {
    fos?: FosState
  }
}

const CURVE_TYPE: 'morton' | 'hilbert' = 'morton'
const CURVE_LABEL =
  CURVE_TYPE === 'morton' ? 'Morton (Z-order)' : 'Hilbert'

const defaultStore: NodeStore = {
  '08c20551111cf6d2abc82e24f77b1003f02357e769bf6b14b7aa42c010c80ee1': [
    [
      'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33',
    ],
    [
      '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33',
      'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    ],
    [
      '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33',
      '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33',
    ],
  ],
  bb254e8a4ba25814ab09da70280897b4d6bbbc564920982b16a8f5b2f2e07261: [
    [
      'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33',
    ],
    [
      '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33',
      'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    ],
  ],
  '3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33': [
    [
      'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    ],
  ],
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855: null,
}

const cloneStore = (store: NodeStore): NodeStore =>
  Object.fromEntries(
    Object.entries(store).map(([hash, edges]) => [
      hash,
      edges
        ? edges.map(([from, to]) => [from, to] as Edge)
        : null,
    ]),
  )

const nextPowerOfTwo = (value: number): number => {
  let result = 1
  while (result < value) {
    result <<= 1
  }
  return result
}

const part1By1 = (input: number): number => {
  let x = input & 0xffff
  x = (x | (x << 8)) & 0x00ff00ff
  x = (x | (x << 4)) & 0x0f0f0f0f
  x = (x | (x << 2)) & 0x33333333
  x = (x | (x << 1)) & 0x55555555
  return x >>> 0
}

const mortonIndex = (row: number, col: number): number =>
  (part1By1(row) << 1) | part1By1(col)

const hilbertRotate = (
  n: number,
  x: number,
  y: number,
  rx: number,
  ry: number,
): [number, number] => {
  let nx = x
  let ny = y
  if (ry === 0) {
    if (rx === 1) {
      nx = n - 1 - nx
      ny = n - 1 - ny
    }
    ;[nx, ny] = [ny, nx]
  }
  return [nx, ny]
}

const hilbertXYToD = (n: number, x: number, y: number): number => {
  let d = 0
  let s = n >> 1
  let px = x
  let py = y
  while (s > 0) {
    const rx = (px & s) > 0 ? 1 : 0
    const ry = (py & s) > 0 ? 1 : 0
    d += s * s * ((3 * rx) ^ ry)
    ;[px, py] = hilbertRotate(s, px, py, rx, ry)
    s >>= 1
  }
  return d
}

const computeMatrixId = (pairs: Array<[number, number]>): number => {
  if (pairs.length === 0) {
    return 0
  }

  const maxIndex = pairs.reduce(
    (acc, [left, right]) => Math.max(acc, left, right),
    0,
  )

  const dim = nextPowerOfTwo(Math.max(1, maxIndex + 1))
  const totalBits = dim * dim
  let value = 0n

  for (const [row, col] of pairs) {
    if (row < 0 || col < 0 || row >= dim || col >= dim) {
      throw new Error(
        `Edge index out of bounds when computing matrix id (row=${row}, col=${col}, dim=${dim})`,
      )
    }

    const pos =
      CURVE_TYPE === 'morton'
        ? mortonIndex(row, col)
        : hilbertXYToD(dim, row, col)

    if (pos >= totalBits) {
      throw new Error(
        `Curve index out of bounds for edge (row=${row}, col=${col}) with dim=${dim}`,
      )
    }

    const bitPos = BigInt(totalBits - pos - 1)
    value |= 1n << bitPos
  }

  if (value > BigInt(Number.MAX_SAFE_INTEGER)) {
    throw new Error(
      'Computed node id exceeds Number.MAX_SAFE_INTEGER; consider using smaller graphs.',
    )
  }

  return Number(value)
}

const assignNodeNumbers = (store: NodeStore): Map<Hash, number> => {
  const assigned = new Map<Hash, number>()
  const entries = Object.entries(store)

  if (entries.length === 0) {
    return assigned
  }

  let progress = true
  const total = entries.length

  while (assigned.size < total && progress) {
    progress = false

    for (const [hash, edges] of entries) {
      if (assigned.has(hash)) {
        continue
      }

      if (!edges || edges.length === 0) {
        assigned.set(hash, 0)
        progress = true
        continue
      }

      const resolvedPairs: Array<[number, number]> = []
      let unresolved = false

      for (const [leftHash, rightHash] of edges) {
        const leftId = assigned.get(leftHash)
        const rightId = assigned.get(rightHash)

        if (leftId === undefined || rightId === undefined) {
          unresolved = true
          break
        }

        resolvedPairs.push([leftId, rightId])
      }

      if (unresolved) {
        continue
      }

      const id = computeMatrixId(resolvedPairs)

      if ([...assigned.values()].some((existing) => existing === id)) {
        // Content-addressed nodes should be unique; matching ids imply identical structure.
        // We allow duplicates but ensure they refer to structurally identical nodes.
        const duplicateHash = [...assigned.entries()].find(
          ([, value]) => value === id,
        )?.[0]
        if (duplicateHash && duplicateHash !== hash) {
          throw new Error(
            `Duplicate node id ${id} computed for hashes ${duplicateHash} and ${hash}.`,
          )
        }
      }

      assigned.set(hash, id)
      progress = true
    }
  }

  if (assigned.size !== total) {
    throw new Error(
      'Could not assign numeric ids to all nodes. The graph may contain cycles or unresolved references.',
    )
  }

  return assigned
}

const findRootHashes = (store: NodeStore): Hash[] => {
  const referenced = new Set<Hash>()
  Object.values(store).forEach((edges) => {
    edges?.forEach(([from, to]) => {
      referenced.add(from)
      referenced.add(to)
    })
  })

  const hashes = Object.keys(store)
  const roots = hashes.filter((hash) => !referenced.has(hash))
  return roots.length > 0 ? roots : hashes
}

const buildIndexedGraph = (store: NodeStore): IndexedGraph => {
  const assigned = assignNodeNumbers(store)
  const sorted = Array.from(assigned.entries()).sort((a, b) => a[1] - b[1])

  const ids = sorted.map(([, id]) => id)
  const idToHash = sorted.map(([hash]) => hash)

  const hashToId: Record<Hash, number> = {}
  const idToIndex: Record<number, number> = {}
  sorted.forEach(([hash, id], index) => {
    hashToId[hash] = id
    idToIndex[id] = index
  })

  const nodes: IndexedNode[] = sorted.map(([hash]) => {
    const edges = store[hash]
    if (!edges) {
      return []
    }

    return edges.map(([leftHash, rightHash]) => {
      const leftId = hashToId[leftHash]
      const rightId = hashToId[rightHash]

      if (leftId === undefined || rightId === undefined) {
        throw new Error(
          `Missing node id for referenced hash: ${leftHash} or ${rightHash}`,
        )
      }

      return [leftId, rightId]
    })
  })

  const rootHashes = findRootHashes(store)
  const roots = rootHashes
    .map((hash) => hashToId[hash])
    .filter((id): id is number => id !== undefined)

  return {
    nodes,
    ids,
    idToHash,
    hashToId,
    idToIndex,
    roots,
  }
}

const rebuildGraphState = (store: NodeStore) => buildIndexedGraph(store)

type ActorMap = Record<string, number>

const deriveActors = (
  indexed: IndexedGraph,
  previous?: ActorMap,
  previousCurrent?: string,
): { actors: ActorMap; current: string } => {
  const actors: ActorMap = {}
  const availableIds = new Set(indexed.ids)

  if (previous) {
    for (const [name, id] of Object.entries(previous)) {
      if (availableIds.has(id)) {
        actors[name] = id
      }
    }
  }

  const existingIds = new Set(Object.values(actors))
  const remainingRoots = indexed.roots.filter((id) => !existingIds.has(id))

  let counter = Object.keys(actors).length + 1
  remainingRoots.forEach((id) => {
    let label: string
    do {
      label = `actor-${counter++}`
    } while (label in actors)
    actors[label] = id
  })

  if (Object.keys(actors).length === 0) {
    const defaultId = indexed.ids[0] ?? 0
    actors['actor-1'] = defaultId
  }

  let current = previousCurrent
  if (!current || actors[current] === undefined) {
    current = Object.keys(actors)[0]
  }

  return { actors, current }
}

const initializeFosState = (): FosState => {
  if (!window.fos || !window.fos.store) {
    const initialStore = cloneStore(defaultStore)
    const derived = rebuildGraphState(initialStore)
    const actorInfo = deriveActors(derived)
    const initialState: FosState = {
      store: initialStore,
      indexed: derived,
      actors: actorInfo.actors,
      currentActor: actorInfo.current,
    }
    window.fos = initialState
    return initialState
  }

  const derived = rebuildGraphState(window.fos.store)
  const actorInfo = deriveActors(
    derived,
    window.fos.actors,
    window.fos.currentActor,
  )
  window.fos.indexed = derived
  window.fos.actors = actorInfo.actors
  window.fos.currentActor = actorInfo.current
  return window.fos
}

const fosState = initializeFosState()

const app = document.querySelector<HTMLDivElement>('#app')
if (!app) {
  throw new Error('App container element not found')
}

app.innerHTML = `
  <div class="fos-app">
    <h1>Graph YAML Playground</h1>
    <p class="fos-description">
      Work with the content-addressed graph store from the C++ project. Import YAML into <code>fos.store</code> or export the current store, and inspect the reconstructed graph below.
    </p>
    <div class="fos-controls">
      <label class="fos-actor-control">
        <span>Actor</span>
        <select id="fos-actor"></select>
      </label>
      <button id="fos-set-root" class="fos-set-root" type="button">Set Actor Root</button>
      <details id="fos-yaml-panel" class="fos-yaml-panel">
        <summary>YAML Import / Export</summary>
        <textarea id="fos-yaml" placeholder="Content-addressed YAML will appear here when you export, or paste YAML here to import."></textarea>
        <div class="fos-yaml-actions">
          <button id="fos-export" type="button">Export YAML</button>
          <button id="fos-import" type="button">Import YAML</button>
        </div>
      </details>
    </div>
    <div id="fos-status" class="fos-status" role="status" aria-live="polite"></div>
    <div class="fos-preview">
      <div class="fos-graph-header">
        <h2>Reconstructed Graph</h2>
        <span class="fos-curve">Curve: ${CURVE_LABEL}</span>
      </div>
      <div id="fos-path" class="fos-path"></div>
      <ol id="fos-tree" class="fos-tree"></ol>
    </div>
  </div>
`

const yamlEditor = document.querySelector<HTMLTextAreaElement>('#fos-yaml')
const statusEl = document.querySelector<HTMLDivElement>('#fos-status')
const pathEl = document.querySelector<HTMLDivElement>('#fos-path')
const treeEl = document.querySelector<HTMLOListElement>('#fos-tree')
const actorSelect = document.querySelector<HTMLSelectElement>('#fos-actor')
const setRootButton =
  document.querySelector<HTMLButtonElement>('#fos-set-root')
const importButton =
  document.querySelector<HTMLButtonElement>('#fos-import')
const exportButton =
  document.querySelector<HTMLButtonElement>('#fos-export')

if (
  !yamlEditor ||
  !statusEl ||
  !pathEl ||
  !treeEl ||
  !actorSelect ||
  !setRootButton ||
  !importButton ||
  !exportButton
) {
  throw new Error('Failed to initialize the graph UI')
}

const setStatus = (message: string, isError = false) => {
  statusEl.textContent = message
  statusEl.classList.toggle('error', isError)
}

const getHashForId = (id: number): string | undefined => {
  const index = fosState.indexed.idToIndex[id]
  if (index === undefined) {
    return undefined
  }
  return fosState.indexed.idToHash[index]
}

const getEdgesForId = (id: number): IndexedEdge[] => {
  const index = fosState.indexed.idToIndex[id]
  if (index === undefined) {
    return []
  }
  return fosState.indexed.nodes[index] ?? []
}

const getDefaultRootId = (): number => {
  const { roots, ids } = fosState.indexed
  return roots[0] ?? ids[0] ?? 0
}

const getActorRootId = (actor: string): number => {
  const rootId = fosState.actors[actor]
  if (rootId !== undefined && fosState.indexed.idToIndex[rootId] !== undefined) {
    return rootId
  }
  return getDefaultRootId()
}

const expandedSides = new Set<string>()
const sideKey = (parentId: number, edgeIndex: number, side: 'left' | 'right') =>
  `${parentId}:${edgeIndex}:${side}`

let currentActor = fosState.currentActor
let currentNodeId = getActorRootId(currentActor)
let breadcrumbs: number[] = [currentNodeId]

const clearExpansions = () => {
  expandedSides.clear()
}

const toggleSideExpansion = (
  parentId: number,
  edgeIndex: number,
  side: 'left' | 'right',
) => {
  const key = sideKey(parentId, edgeIndex, side)
  if (expandedSides.has(key)) {
    expandedSides.delete(key)
  } else {
    expandedSides.add(key)
  }
  renderEdges()
}

const zoomToNode = (targetId: number) => {
  if (fosState.indexed.idToIndex[targetId] === undefined) {
    return
  }
  if (targetId === currentNodeId) {
    return
  }
  currentNodeId = targetId
  breadcrumbs = [...breadcrumbs, targetId]
  clearExpansions()
  renderAll()
}

const navigateToBreadcrumb = (index: number) => {
  if (index < 0 || index >= breadcrumbs.length) {
    return
  }
  const targetId = breadcrumbs[index]
  currentNodeId = targetId
  breadcrumbs = breadcrumbs.slice(0, index + 1)
  clearExpansions()
  renderAll()
}

const renderBreadcrumb = () => {
  pathEl.innerHTML = ''

  const label = document.createElement('span')
  label.textContent = 'Path:'
  pathEl.appendChild(label)

  breadcrumbs.forEach((nodeId, index) => {
    if (index > 0) {
      pathEl.appendChild(document.createTextNode(' › '))
    }

    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'fos-path-segment'
    button.textContent = `Node ${nodeId}`
    const hash = getHashForId(nodeId)
    if (hash) {
      button.title = `Hash: ${hash}`
    }
    if (index === breadcrumbs.length - 1) {
      button.disabled = true
    } else {
      button.addEventListener('click', () => {
        navigateToBreadcrumb(index)
      })
    }
    pathEl.appendChild(button)
  })
}

const renderEdgesList = (
  container: HTMLOListElement,
  nodeId: number,
  visited: Set<number>,
) => {
  container.innerHTML = ''

  const edges = getEdgesForId(nodeId)

  if (!edges.length) {
    const li = document.createElement('li')
    li.className = 'fos-empty'
    li.textContent = 'No edges'
    container.appendChild(li)
    return
  }

  edges.forEach(([leftId, rightId], edgeIndex) => {
    const li = document.createElement('li')
    const row = document.createElement('div')
    row.className = 'fos-item-row fos-edge-row'

    const edgeLabel = document.createElement('span')
    edgeLabel.className = 'fos-edge-label'
    edgeLabel.textContent = `${leftId} - ${rightId}`
    const leftHash = getHashForId(leftId)
    const rightHash = getHashForId(rightId)
    if (leftHash && rightHash) {
      edgeLabel.title = `${leftHash} → ${rightHash}`
    }
    row.appendChild(edgeLabel)

    const createSideControls = (
      side: 'left' | 'right',
      targetId: number,
      targetHash?: string,
    ) => {
      const wrapper = document.createElement('div')
      wrapper.className = `fos-edge-side fos-edge-side-${side}`

      const isZero = targetId === 0
      const key = sideKey(nodeId, edgeIndex, side)
      const isExpanded = expandedSides.has(key)
      const alreadyVisited = visited.has(targetId)
      const targetIndex = fosState.indexed.idToIndex[targetId]
      const targetExists = targetIndex !== undefined

      const expandBtn = document.createElement('button')
      expandBtn.type = 'button'
      expandBtn.className = 'fos-toggle'
      expandBtn.textContent = isExpanded ? '▾' : '▸'
      expandBtn.title = isExpanded
        ? `Collapse ${side === 'left' ? 'left' : 'right'} node ${targetId}`
        : `Expand ${side === 'left' ? 'left' : 'right'} node ${targetId}`
      if (isZero || alreadyVisited || !targetExists) {
        expandBtn.disabled = true
        expandBtn.title = isZero
          ? 'No edges to expand'
          : alreadyVisited
            ? 'Expansion halted to prevent recursion'
            : 'Node not available for expansion'
      } else {
        expandBtn.addEventListener('click', (event) => {
          event.preventDefault()
          event.stopPropagation()
          toggleSideExpansion(nodeId, edgeIndex, side)
        })
      }
      wrapper.appendChild(expandBtn)

      const zoomBtn = document.createElement('button')
      zoomBtn.type = 'button'
      zoomBtn.className = 'fos-zoom'
      zoomBtn.textContent = '⤢'
      zoomBtn.title = `Navigate to node ${targetId}`
      if (!targetExists) {
        zoomBtn.disabled = true
        zoomBtn.title = 'Node not available'
      } else {
        zoomBtn.addEventListener('click', (event) => {
          event.preventDefault()
          event.stopPropagation()
          zoomToNode(targetId)
        })
      }
      wrapper.appendChild(zoomBtn)

      const label = document.createElement('span')
      label.className = `fos-item-label fos-leaf ${
        side === 'left' ? 'fos-leaf-left' : 'fos-leaf-right'
      }`
      label.textContent = `${side === 'left' ? 'L' : 'R'}: Node ${targetId}`
      if (targetHash) {
        label.title = `Hash: ${targetHash}`
      }
      wrapper.appendChild(label)

      return wrapper
    }

    row.appendChild(createSideControls('left', leftId, leftHash))
    row.appendChild(createSideControls('right', rightId, rightHash))
    li.appendChild(row)

    const renderChild = (
      side: 'left' | 'right',
      targetId: number,
    ) => {
      if (targetId === 0) {
        return
      }
      if (fosState.indexed.idToIndex[targetId] === undefined) {
        return
      }
      const key = sideKey(nodeId, edgeIndex, side)
      if (!expandedSides.has(key)) {
        return
      }

      if (visited.has(targetId)) {
        const note = document.createElement('div')
        note.className = 'fos-cycle-note'
        note.textContent = `Cycle detected at node ${targetId}`
        li.appendChild(note)
        return
      }

      const childList = document.createElement('ol')
      childList.className = `fos-sublist fos-sublist-${side}`
      const nextVisited = new Set(visited)
      nextVisited.add(targetId)
      renderEdgesList(childList, targetId, nextVisited)
      li.appendChild(childList)
    }

    renderChild('left', leftId)
    renderChild('right', rightId)

    container.appendChild(li)
  })
}

const renderEdges = () => {
  const visited = new Set<number>([currentNodeId])
  renderEdgesList(treeEl, currentNodeId, visited)
}

const renderAll = () => {
  renderBreadcrumb()
  renderEdges()
}

const populateActorSelect = () => {
  actorSelect.innerHTML = ''
  Object.entries(fosState.actors).forEach(([name, id]) => {
    const option = document.createElement('option')
    option.value = name
    option.textContent = `${name} (Node ${id})`
    if (name === currentActor) {
      option.selected = true
    }
    actorSelect.appendChild(option)
  })
}

const setActiveActor = (actor: string) => {
  if (!(actor in fosState.actors)) {
    return
  }
  currentActor = actor
  fosState.currentActor = actor
  if (window.fos) {
    window.fos.currentActor = actor
  }
  currentNodeId = getActorRootId(actor)
  breadcrumbs = [currentNodeId]
  clearExpansions()
  renderAll()
  populateActorSelect()
}

actorSelect.addEventListener('change', () => {
  setActiveActor(actorSelect.value)
})

setRootButton.addEventListener('click', () => {
  fosState.actors[currentActor] = currentNodeId
  if (window.fos) {
    window.fos.actors = { ...fosState.actors }
  }
  populateActorSelect()
  setStatus(`Set ${currentActor} root to node ${currentNodeId}.`)
})

const populateYamlEditor = () => {
  yamlEditor.value = toYaml(fosState.store, { noRefs: true })
}

const validateStore = (value: unknown): NodeStore => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Store must be a mapping of hashes to edge lists.')
  }

  const entries = Object.entries(value as Record<string, unknown>)
  if (entries.length === 0) {
    throw new Error('Store must contain at least one node.')
  }

  const result: NodeStore = {}
  const referenced = new Set<Hash>()

  for (const [hash, edgesValue] of entries) {
    if (typeof hash !== 'string' || !hash.trim()) {
      throw new Error('Node hash keys must be non-empty strings.')
    }

    if (edgesValue === null) {
      result[hash] = null
      continue
    }

    if (!Array.isArray(edgesValue)) {
      throw new Error(`Node ${hash} must map to an array of edges or null.`)
    }

    const edges: EdgeList = edgesValue.map((edge, index) => {
      if (!Array.isArray(edge) || edge.length !== 2) {
        throw new Error(`Edge ${index} of node ${hash} must be a pair.`)
      }

      const [from, to] = edge as [unknown, unknown]
      if (typeof from !== 'string' || !from.trim()) {
        throw new Error(
          `Edge ${index} of node ${hash} requires a non-empty string source.`,
        )
      }
      if (typeof to !== 'string' || !to.trim()) {
        throw new Error(
          `Edge ${index} of node ${hash} requires a non-empty string target.`,
        )
      }

      return [from, to]
    })

    edges.forEach(([from, to]) => {
      referenced.add(from)
      referenced.add(to)
    })

    result[hash] = edges
  }

  const missing = Array.from(referenced).filter(
    (hash) => !Object.prototype.hasOwnProperty.call(result, hash),
  )
  if (missing.length > 0) {
    throw new Error(
      `Missing node definition(s) for referenced hash(es): ${missing.join(', ')}`,
    )
  }

  return result
}

importButton.addEventListener('click', () => {
  try {
    const parsed = fromYaml(yamlEditor.value || '') as unknown
    const store = cloneStore(validateStore(parsed))
    fosState.store = store
    const indexed = rebuildGraphState(store)
    const actorInfo = deriveActors(indexed, fosState.actors, currentActor)
    fosState.indexed = indexed
    fosState.actors = actorInfo.actors
    fosState.currentActor = actorInfo.current
    if (window.fos) {
      window.fos.indexed = indexed
      window.fos.actors = { ...actorInfo.actors }
      window.fos.currentActor = actorInfo.current
    }
    currentActor = actorInfo.current
    currentNodeId = getActorRootId(currentActor)
    breadcrumbs = [currentNodeId]
    clearExpansions()
    populateActorSelect()
    renderAll()
    setStatus(`Graph imported from YAML (curve: ${CURVE_LABEL}).`)
  } catch (error) {
    const message =
      error instanceof Error ? error.message : 'Unknown import error.'
    setStatus(`Import failed: ${message}`, true)
  }
})

exportButton.addEventListener('click', () => {
  populateYamlEditor()
  setStatus('Graph exported to YAML.')
})

populateYamlEditor()
currentActor = fosState.currentActor
currentNodeId = getActorRootId(currentActor)
breadcrumbs = [currentNodeId]
clearExpansions()
populateActorSelect()
renderAll()
setStatus(`Loaded default graph from C++ store using ${CURVE_LABEL}.`)
