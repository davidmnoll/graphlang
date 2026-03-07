# Project Organization Recommendations

## Current Structure

```
graphlang/
├── cpp/           # C++ implementation (hash-based content addressing)
├── py/            # Python implementation (matrix/curve experiments)
├── js/            # TypeScript visualization + YAML playground
├── prove/         # Lean 4 proofs (multiple experimental modules)
├── artifacts/     # Generated outputs
├── Graphlang/     # Duplicate? Orphaned Lean file
└── docs/          # Documentation (new)
```

## Issues Identified

### 1. Scattered Lean Code
- `prove/` contains the main Lean project
- `Graphlang/Basic.lean` exists at root level (orphaned?)
- Multiple experimental modules: `DigitStream`, `DigitWreath`, `GraphLang`

### 2. Python Module Organization
- Flat structure with 20+ files in `py/`
- Mix of core modules, tests, experiments, and demos
- No clear separation between library and scripts

### 3. Inconsistent Naming
- `prove/` vs `Graphlang/` for Lean
- Some files use underscores, some use hyphens
- No consistent module naming convention

### 4. Missing Shared Concepts
- Each subproject implements similar concepts independently
- No shared specification or interface definition
- Hard to ensure consistency across implementations

---

## Recommended Structure

```
graphlang/
├── docs/                      # All documentation
│   ├── design/               # Design documents
│   │   ├── number-program-mapping.md
│   │   └── encoding-spec.md  # Formal specification
│   ├── api/                  # API documentation
│   └── examples/             # Usage examples
│
├── spec/                      # Formal specifications (language-agnostic)
│   ├── hilbert-encoding.md   # Hilbert curve encoding spec
│   ├── data-types.md         # Nat, Char, String encoding spec
│   └── test-vectors.json     # Shared test cases for all implementations
│
├── core/                      # Core library implementations
│   ├── python/
│   │   ├── graphlang/        # Package directory
│   │   │   ├── __init__.py
│   │   │   ├── encoding/     # Curve implementations
│   │   │   │   ├── hilbert.py
│   │   │   │   └── morton.py
│   │   │   ├── types/        # Data type encoding
│   │   │   │   ├── nat.py
│   │   │   │   ├── char.py
│   │   │   │   └── string.py
│   │   │   ├── graph.py      # Core graph operations
│   │   │   └── store.py      # Graph store (int-addressed)
│   │   ├── tests/
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   ├── cpp/
│   │   ├── include/
│   │   │   └── graphlang/
│   │   │       ├── encoding.hpp
│   │   │       ├── types.hpp
│   │   │       └── store.hpp
│   │   ├── src/
│   │   ├── tests/
│   │   └── CMakeLists.txt
│   │
│   └── lean/                  # Consolidated Lean project
│       ├── Graphlang/
│       │   ├── Basic.lean
│       │   ├── Encoding/
│       │   │   └── Hilbert.lean
│       │   ├── Types/
│       │   │   ├── Nat.lean
│       │   │   └── String.lean
│       │   └── Proofs/
│       │       └── Bijection.lean
│       ├── lakefile.lean
│       └── lean-toolchain
│
├── tools/                     # Development tools
│   ├── visualizer/           # JS/TS visualization (moved from js/)
│   │   ├── src/
│   │   └── package.json
│   └── scripts/              # Build, test, utility scripts
│
├── experiments/               # Experimental code (not production)
│   ├── python/               # Moved from py/ experiments
│   │   ├── trajectory_animation.py
│   │   ├── huge_matrix_demo.py
│   │   └── ...
│   └── lean/                 # Experimental Lean (DigitWreath, etc.)
│
└── README.md
```

---

## Migration Steps

### Phase 1: Documentation & Specs
1. Create `docs/` and `spec/` directories
2. Move/create design documents
3. Write formal encoding specification
4. Create shared test vectors JSON

### Phase 2: Python Reorganization
1. Create proper Python package structure under `core/python/graphlang/`
2. Move core modules (matrix_base, matrix_hilbert, matrix_morton)
3. Move experiments to `experiments/python/`
4. Add `pyproject.toml` for proper packaging

### Phase 3: C++ Updates
1. Update to use integer-based addressing (replace SHA-256 hashes)
2. Add Hilbert curve encoding
3. Implement data type encoding
4. Ensure tests match spec test vectors

### Phase 4: Lean Consolidation
1. Move all Lean code to `core/lean/`
2. Remove orphaned `Graphlang/` at root
3. Organize into `Encoding/`, `Types/`, `Proofs/`
4. Focus proofs on core properties (bijection, etc.)

### Phase 5: Tools & Cleanup
1. Move JS visualizer to `tools/visualizer/`
2. Create build/test scripts
3. Remove duplicates and dead code

---

## Naming Conventions

### Files
- Python: `snake_case.py`
- C++: `snake_case.cpp`, `snake_case.hpp`
- Lean: `PascalCase.lean`
- Docs: `kebab-case.md`

### Modules/Namespaces
- Python: `graphlang.encoding.hilbert`
- C++: `graphlang::encoding::hilbert`
- Lean: `Graphlang.Encoding.Hilbert`

### Types/Classes
- All languages: `PascalCase` (e.g., `GraphStore`, `HilbertEncoder`)

### Functions
- Python: `snake_case`
- C++: `snake_case` or `camelCase` (pick one)
- Lean: `camelCase` for defs, `PascalCase` for types

---

## Shared Test Vectors

Create `spec/test-vectors.json`:

```json
{
  "hilbert_encoding": [
    {"input": 0, "edges": [], "description": "empty graph"},
    {"input": 1, "edges": [[0, 0]], "description": "single self-edge at origin"},
    {"input": 11, "edges": [[0,0], [0,1], [1,1]], "description": "example from spec"}
  ],
  "nat_encoding": [
    {"nat": 0, "graph_id": 0},
    {"nat": 1, "graph_id": "?"},
    {"nat": 5, "graph_id": "?"}
  ],
  "string_encoding": [
    {"string": "", "graph_id": 0},
    {"string": "Hi", "graph_id": "?"}
  ]
}
```

All implementations should pass these test vectors.

---

## Priority Recommendations

### High Priority
1. **Consolidate Lean code** - currently most scattered
2. **Create encoding specification** - needed for consistency
3. **Update C++ to use integer addressing** - currently uses hashes

### Medium Priority
4. **Reorganize Python** - working but messy
5. **Create shared test vectors** - ensures implementations match
6. **Add proper packaging** - pyproject.toml, CMake improvements

### Lower Priority
7. **Move visualizer** - works fine where it is
8. **Separate experiments** - nice-to-have for clarity
