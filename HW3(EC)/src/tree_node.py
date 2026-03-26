class TreeNode:
    """
    A node in the recipe tree.
    
    Attributes:
        label (str): Name of the ingredient, step, or dish
        node_type (str): 'ingredient', 'step', or 'dish'
        metadata (dict): Optional additional info
        children (list): Child nodes
    """
    
    def __init__(self, label, node_type='step', metadata=None):
        self.label = label
        self.node_type = node_type  # 'ingredient', 'step', 'dish'
        self.metadata = metadata or {}
        self.children = []
    
    def add_child(self, child_node):
        """Add a child node to this node."""
        self.children.append(child_node)
    
    def __repr__(self):
        return f"TreeNode({self.label[:30]}, type={self.node_type})"
    
    def to_dict(self):
        """Convert node to dictionary."""
        return {
            'label': self.label,
            'type': self.node_type,
            'metadata': self.metadata,
            'children': [child.to_dict() for child in self.children]
        }