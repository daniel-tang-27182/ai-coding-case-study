from typing import Dict, List

def get_csp_variable_name(position: int, attr_name: str) -> str:
    """Convert a position and attribute name to a CSP variable name."""
    return f"pos_{position}_{attr_name}"

def parse_csp_variable_name(variable_name: str) -> tuple[int, str]:
    """Parse a CSP variable name to extract position and attribute name.
    
    Args:
        variable_name: CSP variable name in format "pos_{position}_{attr_name}"
    
    Returns:
        Tuple of (position, attr_name)
    """
    parts = variable_name.split("_", 2)
    if len(parts) != 3 or parts[0] != "pos":
        raise ValueError(f"Invalid CSP variable name format: {variable_name}")
    return (int(parts[1]), parts[2])

def convert_csp_solution_to_solution_format(csp_solution: Dict[str, str]) -> List[Dict[str, str]]:
    """Convert a CSP solution dictionary to the same format as generate_puzzle_solution.
    
    Args:
        csp_solution: Dictionary mapping CSP variable names (e.g., "pos_0_Name") to values
    
    Returns:
        List of dictionaries, each representing a person with "Position" and attribute keys
    """
    # Group variables by position
    positions_dict: Dict[int, Dict[str, str]] = {}
    
    for csp_var_name, value in csp_solution.items():
        position, attr_name = parse_csp_variable_name(csp_var_name)
        
        if position not in positions_dict:
            positions_dict[position] = {"Position": position}
        
        positions_dict[position][attr_name] = value
    
    # Convert to list sorted by position
    num_people = len(positions_dict)
    solution = []
    for position in range(num_people):
        solution.append(positions_dict[position])
    
    return solution