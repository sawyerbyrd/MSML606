# imports
from tree_builder import TreeNode
from visualizer import RecipeVisualizer
from tree_builder import RecipeTreeBuilder

import pandas as pd
import ast

def main():
    # Load recipes from CSV
    recipes_df = pd.read_csv('../dataset/full_dataset.csv', nrows=10000, encoding='utf-8')

    # Clean data: drop rows with missing ingredients or directions, and unnecessary columns
    recipes_df.dropna(subset=['ingredients', 'directions'], how='all', inplace=True)
    recipes_df.drop(columns=['id', 'source', 'link'], inplace=True, errors='ignore')
    
    # add new column for the recipe tree
    recipes_df['recipe_tree'] = None
    
    # build recipe trees

    # build recipe trees for the test set
    builder = RecipeTreeBuilder()
    test_trees = []
    for idx, row in recipes_df.iterrows():
        recipe = {
            'title': row['title'],
            'ingredients': ast.literal_eval(row['ingredients']),
            'directions': ast.literal_eval(row['directions'])
        }
        tree = builder.build_tree(recipe)
        if tree:
            test_trees.append(tree)
            
    
    #Display the first 10 recipe trees
    for i, tree in enumerate(test_trees[:10]):
        print(f"\nRecipe {i+1}: {tree.label}")
        RecipeVisualizer.display_tree(tree)
        
if __name__ == "__main__":
    main()