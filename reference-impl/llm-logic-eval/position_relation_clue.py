from constraint import FunctionConstraint
from csp_utils import get_csp_variable_name

class PositionRelationClue:
    def __init__(self, attr_name: str, attr_value_left: str, attr_value_right: str):
        self.attr_name = attr_name
        self.attr_value_left = attr_value_left
        self.attr_value_right = attr_value_right

    def __str__(self):
        return f"The person who has {self.attr_value_left} as their {self.attr_name} is sitting to the left of the person who has {self.attr_value_right} as their {self.attr_name}."
        
    def __repr__(self):
        return f"PRC(attr_name={self.attr_name},attr_value_left={self.attr_value_left},attr_value_right={self.attr_value_right})"

    def add_to_csp_problem(self, csp_problem, num_people: int):
        for pos_left in range(num_people - 1):
            csp_var_left = get_csp_variable_name(pos_left, self.attr_name)
            csp_var_right = get_csp_variable_name(pos_left + 1, self.attr_name)

            def constraint_func(left, right):
                if left == self.attr_value_left:
                    return right == self.attr_value_right
                else:
                    return True

            csp_problem.addConstraint(constraint_func, [csp_var_left, csp_var_right])