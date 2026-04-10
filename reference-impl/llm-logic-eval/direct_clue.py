from constraint import FunctionConstraint
from csp_utils import get_csp_variable_name


class DirectClue:
    def __init__(self, position: int, attr_name: str, attr_value):
        self.position = position
        self.attr_name = attr_name
        self.attr_value = attr_value

    def __str__(self):
        return f"The person sitting at position {self.position} has {self.attr_value} as their {self.attr_name}."

    def __repr__(self):
        return f"DC(pos={self.position},attr_name={self.attr_name},attr_value={self.attr_value})"

    def add_to_csp_problem(self, csp_problem, num_people: int):
        csp_variable = get_csp_variable_name(self.position, self.attr_name)
        csp_constraint = FunctionConstraint(
            lambda var: var == self.attr_value,
        )
        csp_problem.addConstraint(csp_constraint, [csp_variable])

