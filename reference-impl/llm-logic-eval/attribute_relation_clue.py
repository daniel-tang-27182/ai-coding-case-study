from constraint import FunctionConstraint
from csp_utils import get_csp_variable_name

class AttributeRelationClue:
    def __init__(self, attr_name_a: str, attr_value_a: str, attr_name_b: str, attr_value_b: str):
        self.attr_name_a = attr_name_a
        self.attr_value_a = attr_value_a
        self.attr_name_b = attr_name_b
        self.attr_value_b = attr_value_b

    def __str__(self):
        return f"The person who has {self.attr_value_a} as their {self.attr_name_a} also has {self.attr_value_b} as their {self.attr_name_b}."

    def __repr__(self):
        return f"ARC(attr_name_a={self.attr_name_a},attr_value_a={self.attr_value_a},attr_name_b={self.attr_name_b},attr_value_b={self.attr_value_b})"

    def add_to_csp_problem(self, csp_problem, num_people: int):
        # Create constraints for each position: if attr_name_a has attr_value_a, then attr_name_b must have attr_value_b
        # Using implication: not (attr_a == value_a) or (attr_b == value_b)
        for position in range(num_people):
            csp_var_a = get_csp_variable_name(position, self.attr_name_a)
            csp_var_b = get_csp_variable_name(position, self.attr_name_b)
            csp_constraint = FunctionConstraint(
                lambda a, b: not (a == self.attr_value_a) or (b == self.attr_value_b)
            )
            csp_problem.addConstraint(csp_constraint, [csp_var_a, csp_var_b])