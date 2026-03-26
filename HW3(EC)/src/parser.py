# imports
import re
from tree_node import TreeNode

# Compile regex once for efficiency
# This regex captures:
# 1. Quantity: either a decimal number (e.g., 2, 1.5) or a fraction (e.g., 1/2)
# 2. Unit: a sequence of letters (e.g., "cup", "tsp"), possibly followed by a period (e.g., "c.")
# 3. Ingredient name: the rest of the line
ATTACHED_REGEX = re.compile(r'^(\d+(?:\.\d+)?|\d+\/\d+)([a-zA-Z\.]+)$')


def extract_quantity_unit_label(ingredient_text, units):
    """
    Extract quantity, unit, and label from an ingredient string.
    
    Returns:
        (quantity, unit, label)
    """
    # Handle empty or malformed
    if not ingredient_text or not isinstance(ingredient_text, str):
        return None, None, ingredient_text if ingredient_text else "Missing ingredient"

    ingredient_text = ingredient_text.strip()
    if not ingredient_text:
        return None, None, "Missing ingredient"

    tokens = ingredient_text.split()
    quantity_tokens = []
    i = 0

    # collect consecutive number tokens (integers, decimals, fractions)
    while i < len(tokens):
        token = tokens[i]
        # Check if token is a pure number (int, decimal, fraction)
        if re.match(r'^\d+(?:\.\d+)?$', token) or re.match(r'^\d+\/\d+$', token):
            quantity_tokens.append(token)
            i += 1
        else:
            # If token contains a number attached to a unit (e.g., "1/2c")
            match = ATTACHED_REGEX.match(token)
            if match:
                # Split into quantity and unit
                quantity_tokens.append(match.group(1))
                # The unit is the second part, treat it as the unit token
                tokens = [match.group(2)] + tokens[i+1:]
                break
            else:
                break  # no more quantity tokens

    # If we found quantity tokens, combine them
    if quantity_tokens:
        quantity = ' '.join(quantity_tokens)
        # Next token might be a unit
        if i < len(tokens):
            # Check if the next token is a known unit (case-insensitive, ignore trailing dots)
            candidate_unit = tokens[i].strip('.')
            if candidate_unit.lower() in units:
                unit = tokens[i]
                # Remove trailing dot for consistency
                if unit.endswith('.'):
                    unit = unit[:-1]
                label = ' '.join(tokens[i+1:]) if i+1 < len(tokens) else ""
            else:
                # No unit, so label starts from the current token
                unit = None
                label = ' '.join(tokens[i:])
        else:
            # No tokens after quantity
            unit = None
            label = ""
    else:
        # No quantity found at the beginning – use whole text as label
        quantity = None
        unit = None
        label = ingredient_text

    # Clean up empty label
    if label == "":
        label = ingredient_text  # fallback to original text

    return quantity, unit, label

def parse_ingredient(ingredient_text, units={'cup', 'cups', 'c', 'tsp', 'tbsp', 'g', 'kg', 'oz', 'lb', 'clove', 'cloves', 'pinch'}, quantity_indicators={'1/2', '1/4', '3/4', '1/3', '2/3', '1/8', '3/8', '5/8', '7/8'}):
    """
    Parse ingredient text into a node with metadata.
    Handles various formats and noise.
    """
    # Handle empty or missing ingredients
    if not ingredient_text or ingredient_text.strip() == "":
        return TreeNode(
            label="Missing ingredient",
            node_type='ingredient',
            metadata={'quantity': None, 'unit': 'None'}
        )
    
    # Extract components
    quantity, unit, label = extract_quantity_unit_label(ingredient_text, units)

    # If there is still no quantity but the string starts with a number (e.g., "3 eggs"),
    # this is a simple fallback case.
    if quantity is None and re.match(r'^\d+', ingredient_text):
        
        parts = ingredient_text.split()
        if parts[0].replace('.', '').isdigit():
            quantity = parts[0]
            # Check if next token is a unit
            if len(parts) > 1 and parts[1].lower() in units:
                unit = parts[1]
                label = ' '.join(parts[2:]) if len(parts) > 2 else ""
            else:
                label = ' '.join(parts[1:])
        else:
            label = ingredient_text
    
    return TreeNode(
        label=label if label else ingredient_text,
        node_type='ingredient',
        metadata={
            'quantity': quantity,
            'unit': unit,
            'original_text': ingredient_text,
            'cleaned': True
        }
    )