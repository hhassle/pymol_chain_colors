import csv
import matplotlib.pyplot as plt
from pymol import cmd
import os

def load_chain_values_from_csv(csv_path):
    """
    Load chain identifiers and their values from a CSV file.
    Expects a header row with 'chain' and 'value' columns.

    Returns:
    - A dictionary mapping chain names to numerical values.
    """
    chain_value_dict = {}
    with open(csv_path, newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                chain = row['chain'].strip()
                value = float(row['value'])
                chain_value_dict[chain] = value
            except (KeyError, ValueError):
                print(f"Skipping invalid row: {row}")
    return chain_value_dict

def color_chains_by_value(chain_value_dict, cmap_name="viridis", min_val=None, max_val=None):
    """
    Colors chains based on a dictionary of chain-to-value mappings using a color gradient.
    
    Parameters:
    - chain_value_dict: Dictionary mapping chain identifiers to numerical values.
    - cmap_name: Name of a Matplotlib colormap (e.g., "coolwarm", "viridis").
    - min_val: Minimum value for color normalization (optional).
    - max_val: Maximum value for color normalization (optional).
    """
    if not chain_value_dict:
        print("No chains provided for coloring.")
        return
    
    # Determine normalization range
    if min_val is None:
        min_val = min(chain_value_dict.values())
    if max_val is None:
        max_val = max(chain_value_dict.values())

    value_range = max_val - min_val or 1  # Avoid division by zero
    cmap = plt.get_cmap(cmap_name)

    for i, (chain, value) in enumerate(chain_value_dict.items()):
        normalized_value = 1 - (value - min_val) / value_range
        rgb = cmap(normalized_value)[:3]  # ignore alpha
        color_name = f"chain_color_{i}"

        cmd.set_color(color_name, rgb)
        cmd.color(color_name, f"chain {chain}")
    
    print(f"Colored {len(chain_value_dict)} chains using the '{cmap_name}' colormap.")
    print(f"Value range: {min_val:.3f} to {max_val:.3f}")

def pymol_chain_colors(csv_path, cmap_name="viridis", min_val=None, max_val=None):
    """
    Main function for use in PyMOL.
    
    Arguments from PyMOL are always passed as strings, so min_val and max_val must be cast.
    """
    if not os.path.isfile(csv_path):
        print(f"File not found: {csv_path}")
        return

    # Convert min and max values from strings if provided
    try:
        min_val = float(min_val) if min_val else None
        max_val = float(max_val) if max_val else None
    except ValueError:
        print("Invalid min or max value. Please provide numeric values.")
        return

    chain_values = load_chain_values_from_csv(csv_path)
    color_chains_by_value(chain_values, cmap_name, min_val, max_val)

# Register for PyMOL
cmd.extend("pymol_chain_colors", pymol_chain_colors)
