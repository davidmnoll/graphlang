use std::collections::HashMap;

pub trait GNode {
    /**
     * list deps - references
     * - CID's are global... just check
     * - UUID's / vars must be in scope?
     *   - declarations?
     *
     * fixpoint thing?  
     *
     *
     *
     *   
     */

    /**
     * "previous" or other indexing queries are sort of like queries, but
     * match node is more explicitly a query.  The index can be view as exponent,
     * i.e. argument.  So previous might be something that should
     */

    fn has_edge(&self, a: &dyn GNode, b: &dyn GNode);

    fn map_edges(&self);

    fn filter_edges(&self);

    fn reduce_edges(&self);

    fn is_equal(&self);

    fn add_edge_generator(&self);

    fn meet(&self); // add into new node with self as meet point?

    fn join(&self); // add into new node with self as join point?

    fn evaluate(&self);

    fn match_node(&self) -> Box<dyn GNode>;

    fn insert_expr(&self) -> Box<dyn GNode>;

    fn check(&self);

    fn infer(&self);

    /**
     * serializations
     * json, yaml, numeric
     */
    fn cid(&self) -> String {
        String::new()
    }
}

pub struct GCapability {
    inbox: Box<dyn GNode>,
    outbox: Box<dyn GNode>,
}

/// A term graph. Nodes live in an arena and reference each other by
/// `NodeId`; internal traversal never touches a content address. Cids are
/// derived on demand when a node crosses the wire/storage boundary.
/// There is no root: rooting comes from the channels.
pub struct GContext {
    nodes: Vec<Box<dyn GNode>>,
    channel_map: HashMap<String, GCapability>,
}

pub struct GConstant {}

// pub struct GPiecewise {
// /**
//  * Set of pairs
//  * - positive/negative flag
//  * -
//  *
//  *
//  */
// }

pub struct GPeriodic {}

impl GContext {
    /**
     * actual:
     * conflict, local_edit, agreed_view, replay,
     * insert, resolve, recieve, broadcast
     *
     * relay?
     */

    /**
     * ideal:
     *
     */

    pub fn new() -> Self {
        Self {
            nodes: Vec::new(),
            channel_map: HashMap::new(),
        }
    }

    /// Intern a node, returning its pointer-like reference.
    // pub fn insert(&mut self, node: Box<dyn GNode>) -> &mut dyn GNode {
    //     self.nodes.push(node);
    // }

    // pub fn node(&self, id: NodeId) -> &dyn GNode {
    //     &*self.nodes[id.0 as usize]
    // }

    /// The content address of a node, for the wire/storage boundary.
    /// TODO: derive from the node's edges (canonical order, hashed) and
    /// intern so equal content yields equal cids.

    /**
     *
     * Channels.
     * if on left, right side is treated as data... pattern destructures input... output pattern appended.  data queued ?  added as term?
     *
     * then when queried, it decided which term(s) are relevant
     *
     *
     */

    // fn intern_channel(&self) -> Box<dyn GNode> {}

    // fn register_capability(&self) {}

    // fn base_node(&self) {
    //     return GNode::new();
    // }
    /// State sync on (re)connect. Returns messages to send.
    /// TODO: replay the agreed graph as GExprs (nil → agreed).
    pub fn replay(&self) -> Vec<String> {
        Vec::new()
    }
    pub fn receive(&mut self, _text: &str) {}

    pub fn broadcast(&mut self) {}
    /// Textbox changed. Returns messages to send.
    /// TODO: diff against the agreed graph.
    pub fn local_edit(&mut self, _text: &str) -> Vec<String> {
        Vec::new()
    }

    /// The conflict condition: two proposals share a base. Resolved views
    /// of (ours, theirs). TODO: surface from contains_match().
    pub fn conflict(&self) -> Option<(String, String)> {
        None
    }

    /// `choice` is "ours" or "theirs". Returns the superseding messages.
    pub fn resolve(&mut self, _choice: &str) -> Vec<String> {
        Vec::new()
    }

    /// The agreed pane: (text, digest).
    /// TODO: derive both from the agreed channel's node in the term graph.
    pub fn agreed_view(&self) -> (String, String) {
        (String::new(), String::new())
    }
}
