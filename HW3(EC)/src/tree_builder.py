# imports
from tree_node import TreeNode
from parser import parse_ingredient
import re
STOPWORDS = {'cut', 'up', 'and', 'or', 'with', 'in', 'on', 'into', 'to', 'from', 'for', 'the', 'a', 'an', 'of'}

class RecipeTreeBuilder:
    def __init__(self):
        self.issues = {}

    # Helper functions for parsing ingredients
    
    @staticmethod
    def clean_ingredient_label(label):
        """Remove parenthetical content, punctuation, and extra spaces."""
        # Remove text in parentheses
        label = re.sub(r'\([^)]*\)', '', label)
        # Replace commas, colons, etc. with spaces
        label = re.sub(r'[,.:;]', ' ', label)
        # Remove extra spaces
        label = ' '.join(label.split())
        return label.strip()

    @staticmethod
    def tokenize(text):
        """Convert text to a set of lowercase words, ignoring stopwords."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        words = [w for w in words if w not in STOPWORDS]
        return set(words)

    def build_tree(self, recipe):
        try:
            # Root node
            title = recipe.get('title', 'Untitled Recipe')
            root = TreeNode(title, node_type='dish', metadata={'id': recipe.get('id')})

            # Parse ingredients into nodes, store with lowercase label for matching
            ingredient_nodes = []
            for ing_text in recipe.get('ingredients', []):
                ing_node = parse_ingredient(ing_text)
                ingredient_nodes.append(ing_node)

            # Create step nodes
            directions = recipe.get('directions', [])
            step_nodes = []
            for i, dir_text in enumerate(directions):
                if not dir_text:
                    dir_text = f"Step {i+1} (missing description)"
                step_node = TreeNode(dir_text.strip(), node_type='step', metadata={'step': i})
                step_nodes.append(step_node)

            # If there are no steps, attach ingredients directly to root
            if not step_nodes:
                for ing_node in ingredient_nodes:
                    root.add_child(ing_node)
                return root

            # Match ingredients to steps
            # this part is all about checking if the ingredient label appears in the step text, 
            # and if so, attaching it as a child of that step node.
            step_tokens = [self.tokenize(step_node.label) for step_node in step_nodes]

            # Attach each ingredient to the best matching step
            for ing_node in ingredient_nodes:
                label = ing_node.label.strip()
                cleaned = self.clean_ingredient_label(label)
                if not cleaned:
                    # No meaningful name, attach to first step
                    step_nodes[0].add_child(ing_node)
                    continue
                
                # Tokenize cleaned label for matching
                ing_tokens = RecipeTreeBuilder.tokenize(cleaned)
                if not ing_tokens:
                    step_nodes[0].add_child(ing_node)
                    continue

                best_score = 0
                best_step = None
                best_idx = None
                # Iterate through steps to find best match based on token overlap
                for idx, step_node in enumerate(step_nodes):
                    score = len(ing_tokens.intersection(step_tokens[idx]))
                    if score > best_score or (score == best_score and (best_idx is None or idx < best_idx)):
                        best_score = score
                        best_step = step_node
                        best_idx = idx

                if best_step and best_score > 0:
                    best_step.add_child(ing_node)
                else:
                    step_nodes[0].add_child(ing_node)

            # Chain steps together
            for i in range(len(step_nodes) - 1):
                step_nodes[i].add_child(step_nodes[i+1])

            # Attach first step to root
            root.add_child(step_nodes[0])

            return root

        except Exception as e:
            print(f"Error building tree: {e}")
            return None