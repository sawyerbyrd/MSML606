# imports
from tree_node import TreeNode

class RecipeVisualizer:
    @staticmethod
    def display_tree(node, level=0, step=1, max_depth=30):
        if level > max_depth:
            print("  " * level + "... (more nodes)")
            return

        indent = "  " * level
        # Add step number to step nodes
        if node.node_type == 'step':
            icon = node.node_type.capitalize() + f" {step}: "
            step += 1
        else:
            icon = node.node_type.capitalize() + ": "

        # Show metadata for ingredients (quantity/unit)
        extra = ""
        if node.node_type == 'ingredient' and node.metadata.get('quantity'):
            q = node.metadata['quantity']
            u = node.metadata.get('unit', '')
            extra = f" ({q} {u})" if u else f" ({q})"

        print(f"{indent}{icon}{node.label}{extra}")

        for child in node.children:
            RecipeVisualizer.display_tree(child, level + 1, step, max_depth)
