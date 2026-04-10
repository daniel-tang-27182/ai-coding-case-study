from constraint import Problem, AllDifferentConstraint
from typing import Dict, List
from data import AttrName

def create_problem_from_used_values(used_values: Dict[AttrName, List[str]]) -> Problem:
    problem = Problem()
    num_people = len(next(iter(used_values.values())))
    
    # Add variables for each position and each attribute, and add AllDifferentConstraint
    # Variable naming: pos_{position}_{attr_name}
    for attr_enum in used_values.keys():
        attr_name = attr_enum.value
        variables_for_attr = []
        for position in range(num_people):
            variable_name = f"pos_{position}_{attr_name}"
            domain = used_values[attr_enum]
            problem.addVariable(variable_name, domain)
            variables_for_attr.append(variable_name)
        
        # Add AllDifferentConstraint for each attribute to ensure each value is used exactly once
        problem.addConstraint(AllDifferentConstraint(), variables_for_attr)
    
    return problem

def pretty_print_constraint_solutions(solutions: list[Dict[str, str]]) -> None:
    for solution in solutions:
        print(solution)

