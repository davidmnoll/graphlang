use std::collections::HashMap;

pub trait GExpr {
    fn left(&self) -> Box<dyn GNode>;

    fn right(&self) -> Box<dyn GNode>;
}

pub trait GNode {
    fn contains_match(&self) -> Box<dyn GNode>;

    fn insert_expr(&self) -> Box<dyn GNode>;

    fn intern_channel(&self) -> Box<dyn GNode>;

    fn get_previous(&self) -> Box<dyn GNode>;
}

/// The empty node: every operation yields another empty node.
/// Placeholder root until concrete node semantics land.
pub struct EmptyNode;

impl GNode for EmptyNode {
    fn contains_match(&self) -> Box<dyn GNode> {
        Box::new(EmptyNode)
    }

    fn insert_expr(&self) -> Box<dyn GNode> {
        Box::new(EmptyNode)
    }

    fn intern_channel(&self) -> Box<dyn GNode> {
        Box::new(EmptyNode)
    }

    fn get_previous(&self) -> Box<dyn GNode> {
        Box::new(EmptyNode)
    }
}

pub struct GCapability {
    incoming_pattern: Box<dyn GNode>, // infer from messages in inbox?
    outgoing_pattern: Box<dyn GNode>, // infer from messages in outbox?
    inbox: Box<dyn GNode>,
    outbox: Box<dyn GNode>,
}

pub struct GClient {
    root_node: Box<dyn GNode>,
    capability_map: HashMap<String, GCapability>,
}

impl GClient {
    pub fn new() -> Self {
        Self {
            root_node: Box::new(EmptyNode),
            capability_map: HashMap::new(),
        }
    }

    pub fn root_node(&self) -> &dyn GNode {
        &*self.root_node
    }

    fn register_capability(&self) {}
}

impl Default for GClient {
    fn default() -> Self {
        Self::new()
    }
}
