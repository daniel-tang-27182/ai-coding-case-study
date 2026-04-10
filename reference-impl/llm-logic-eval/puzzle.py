import json
from typing import Dict, List
from direct_clue import *
from attribute_relation_clue import *
from position_relation_clue import *
from puzzle_data import AttrName

class Puzzle:
    def __init__(self, solution: list[Dict[str, str]]):
        self.solution = solution
        self.clues = []

    def getPuzzlePrompt(self):
        num_people = len(self.solution)
        attribute_domains = self.get_attribute_domains()
        available_attributes = attribute_domains.keys()

        promptText = ""
        promptText += (
            f"There are {num_people} people attending a party. Everyone is sitting in a row. "
            + f"The left most seat will be referred to as position 0, the next seat to the right will be referred to as position 1"
            + f" and so on. Each person has a " + ', '.join(available_attributes) + ".\n\n"
        )
        for attr_name, attr_values in attribute_domains.items():
            promptText += f"The possible values for {attr_name} are: {', '.join(attr_values)}\n"

        promptText += "\nBelow are a set of clues about each person.\n\n"

        for clue in self.clues:
            promptText += str(clue) + " "

        promptText += f"\n\nCan you figure out what each person's " + ', '.join(available_attributes) + " are?\n\n"

        promptText += "Please write the anwser as a JSON array demarked with in <solution></solution> tags, where each element is a JSON objects. "
        promptText += "Do not include anything else in the output. For example:\n"
        promptText += "<solution>\n"
        promptText += json.dumps(self.get_dummy_solution(), indent=4)
        promptText += "\n</solution>\n"

        return promptText

    def pretty_print_solution(self) -> None:
        print(json.dumps(self.solution, indent=4))

    def get_dummy_solution(self):
        dummy_solution = []
        for attr_dict in self.solution:
            dummy_attr_dict = {}
            for attr in attr_dict:
                if attr == "Position":
                    dummy_attr_dict[attr] = attr_dict[attr]
                else:
                    dummy_attr_dict[attr] = "X"
            dummy_solution.append(dummy_attr_dict)
        return dummy_solution

    """Get the set of all possible values for each attribute from the solution.
    
    Returns:
        Dictionary mapping attribute name to list of all possible values for that attribute
    """
    def get_attribute_domains(self) -> Dict[str, List[str]]:
        attribute_domains: Dict[str, List[str]] = {}
        attr_names = [attr for attr in self.solution[0].keys()]
        for attr_name in attr_names:
            if attr_name != "Position":
                values = []
                for person in self.solution:
                    values.append(person[attr_name])
                attribute_domains[attr_name] = values
        
        return attribute_domains