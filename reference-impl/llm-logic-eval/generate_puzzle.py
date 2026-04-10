import random
from typing import Dict, List
from puzzle_data import attributes_values, AttrName
from direct_clue import DirectClue
from attribute_relation_clue import AttributeRelationClue
from position_relation_clue import PositionRelationClue
from puzzle import Puzzle
from constraint import Problem, AllDifferentConstraint
from csp_utils import get_csp_variable_name, convert_csp_solution_to_solution_format

def generate_puzzle_solution(num_people: int, num_attributes: int) -> list[Dict[str, str]]:
    # Select random subset of attributes and always select the Name attribute
    available_attributes = [attr for attr in attributes_values.keys() if attr != AttrName.NAME]
    selected_attributes_enums = [AttrName.NAME] + random.sample(available_attributes, num_attributes)
    
    # Initialize tracking of used values for each attribute
    used_attributes = {attr: [] for attr in selected_attributes_enums}
    
    # Generate solution
    solution = []
    for idx in range(num_people):
        person_attributes = {}
        person_attributes["Position"] = idx
        for attr_enum in selected_attributes_enums:
            # Get available values that haven't been used for this attribute
            available_values = [v for v in attributes_values[attr_enum] if v not in used_attributes[attr_enum]]
            
            # Select a random value and track it
            selected_value = random.choice(available_values)
            used_attributes[attr_enum].append(selected_value)
            # Store with enum's value (string) for compatibility with existing code
            person_attributes[attr_enum.value] = selected_value
        solution.append(person_attributes)
    
    return solution

def init_csp_solver(attribute_domains: Dict[str, List[str]]) -> Problem:
    problem = Problem()
    num_people = len(next(iter(attribute_domains.values())))

    # Add variables for each position and each attribute, and add AllDifferentConstraint
    for attr_name in attribute_domains.keys():
        csp_variables = []
        for position in range(num_people):
            variable_name = get_csp_variable_name(position, attr_name)
            domain = attribute_domains[attr_name]
            problem.addVariable(variable_name, domain)
            csp_variables.append(variable_name)
        
        # Add AllDifferentConstraint for each attribute to ensure each value is used exactly once
        problem.addConstraint(AllDifferentConstraint(), csp_variables)
    
    return problem

def gen_all_direct_clues(solution: list[Dict[str, str]]) -> List[DirectClue]:
    clues = []
    for person in solution:
        position = person["Position"]
        for attr_name, attr_value in person.items():
            if attr_name != "Position":
                clues.append(DirectClue(position, attr_name, attr_value))
    return clues

def gen_all_attribute_relation_clues(solution: list[Dict[str, str]]) -> List[AttributeRelationClue]:
    clues = []
    for person in solution:
        attr_names = list(filter(lambda x: x != "Position", person.keys()))
        # Generate all unique unordered pairs of attributes
        for i, attr_name_a in enumerate(attr_names):
            for attr_name_b in attr_names[i+1:]:
                clues.append(AttributeRelationClue(
                    attr_name_a, person[attr_name_a],
                    attr_name_b, person[attr_name_b]
                ))
    return clues

def gen_all_position_relation_clues(solution: List[Dict[str, str]]) -> List[PositionRelationClue]:
    clues = []
    # Generate clues for all adjacent position pairs
    for position_left in range(len(solution) - 1):
        position_right = position_left + 1
        person_left = solution[position_left]
        person_right = solution[position_right]
        attr_names = list(filter(lambda x: x != "Position", person_left.keys()))
        # Generate a clue for each attribute
        for attr_name in attr_names:
            clues.append(PositionRelationClue(
                attr_name, person_left[attr_name], person_right[attr_name]
            ))
    return clues

def add_clues(puzzle: Puzzle, csp_problem, num_people: int, potential_clues, num_clues=5):
    for i in range(num_clues):
        clue = random.choice(potential_clues)
        puzzle.clues.append(clue)
        potential_clues.remove(clue)
        clue.add_to_csp_problem(csp_problem, num_people)


def generate_puzzle(num_people: int, num_attributes: int) -> Puzzle:
    solution = generate_puzzle_solution(num_people, num_attributes)
    puzzle = Puzzle(solution)

    csp_problem = init_csp_solver(puzzle.get_attribute_domains())
    potential_clues = (
        gen_all_direct_clues(solution) 
        + gen_all_attribute_relation_clues(solution)
        + gen_all_position_relation_clues(solution)
    )
    num_initial_clues = 0
    difficulty = max(num_people, num_attributes) ** 2
    if difficulty <= 100 :
        num_initial_clues = min(int(num_people * num_attributes * 1.4), len(potential_clues))
    elif difficulty < 225:
        num_initial_clues = min(int(difficulty * 2), len(potential_clues))
    elif difficulty < 289:
        num_initial_clues = min(int(difficulty * 2.3), len(potential_clues))
    else:
        num_initial_clues = min(int(difficulty * 3.1), len(potential_clues))

    print(f"num_people = {num_people}")
    print(f"num_attributes = {num_attributes}")
    # print(f"num_potential_clues = {len(potential_clues)}")
    # print(f"num_initial_clues = {num_initial_clues}")
    num_clues_per_iteration = max(1, random.randint(
        int(num_people * num_attributes * 0.06) - 1, 
        int(num_people * num_attributes * 0.06) + 1)
    )
    add_clues(puzzle, csp_problem, num_people, potential_clues, num_initial_clues)
    csp_solutions = csp_problem.getSolutions()
    num_solutions = len(csp_solutions)

    while num_solutions > 1:
        print("Number of csp solutions: ", num_solutions)
        add_clues(puzzle, csp_problem, num_people, potential_clues, num_clues_per_iteration)
        csp_solutions = csp_problem.getSolutions()
        num_solutions = len(csp_solutions)
    print(f"Num clues = {len(puzzle.clues)}")
    converted_csp_solution = convert_csp_solution_to_solution_format(csp_solutions[0])
    assert converted_csp_solution == puzzle.solution, "csp_solution must equal original puzzle solution"

    return puzzle

if __name__ == "__main__":
    total_num_clues = 0
    for i in range(1, 11):
        for j in range(1, 11):
            puzzle = generate_puzzle(i, j)
            total_num_clues += len(puzzle.clues)
    print(f"Total Num Clues = {total_num_clues}")

