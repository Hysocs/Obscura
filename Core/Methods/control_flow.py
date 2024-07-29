import ast
import random
import logging
from Core.utils import name_generator

logger = logging.getLogger(__name__)

class ControlFlowObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.fake_predicates = [
            "2 + 2 == 4", 
            "3 * 3 == 9", 
            "10 - 5 == 5",
            "4 * 4 == 16",
            "20 - 10 == 10",
            "(3 * 5) % 2 == 1",
            "((10 + 2) * 3) / 2 == 18"
        ]

    def add_opaque_predicate(self, node):
        predicate = random.choice(self.fake_predicates)
        fake_if = ast.If(
            test=ast.parse(predicate).body[0].value,
            body=[node, ast.Pass()],
            orelse=[ast.Pass()]
        )
        return fake_if

    def visit_If(self, node):
        self.generic_visit(node)
        return self.add_opaque_predicate(node)
    
    def visit_While(self, node):
        self.generic_visit(node)
        return self.add_opaque_predicate(node)

    def visit_For(self, node):
        self.generic_visit(node)
        return self.add_opaque_predicate(node)


def control_flow_obfuscate(code):
    tree = ast.parse(code)
    obfuscator = ControlFlowObfuscator()
    obfuscated_tree = obfuscator.visit(tree)
    ast.fix_missing_locations(obfuscated_tree)
    return ast.unparse(obfuscated_tree)
