import ast
import random
import logging
import string
from collections import deque
from Core.utils import NameGenerator # Import the name_generator instance

logger = logging.getLogger(__name__)


class FunctionDuplicator(ast.NodeTransformer):
    def __init__(self, name_generator):
        self.name_generator = name_generator
        self.function_mirroring = []

    def visit_ClassDef(self, node):
        new_body = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                new_body.append(item)
                duplicate_node = self.duplicate_function(item)
                new_body.append(duplicate_node)
                self.function_mirroring.append(duplicate_node)
            else:
                new_body.append(item)
        node.body = new_body
        return node

    def visit_Module(self, node):
        new_body = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                new_body.append(item)
                duplicate_node = self.duplicate_function(item)
                new_body.append(duplicate_node)
                self.function_mirroring.append(duplicate_node)
            elif isinstance(item, ast.ClassDef):
                new_body.append(self.visit_ClassDef(item))
            else:
                new_body.append(item)
        node.body = new_body
        return node

    def duplicate_function(self, node):
        duplicate_node = ast.FunctionDef(
            name=self.name_generator.generate_name(),
            args=node.args,
            body=self.insert_no_op_statements(node.body),
            decorator_list=node.decorator_list,
            returns=node.returns
        )
        return duplicate_node

    def insert_no_op_statements(self, body):
        new_body = []
        for stmt in body:
            new_body.append(stmt)
            if random.choice([True, False]):
                new_body.append(ast.Pass())
            if random.choice([True, False]):
                new_body.append(ast.Expr(value=ast.Constant(value=None)))
        return new_body

    def add_fake_calls(self, tree):
        fake_calls = []
        for func in self.function_mirroring:
            fake_call = ast.If(
                test=ast.Constant(value=False),
                body=[ast.Expr(value=ast.Call(func=ast.Name(id=func.name, ctx=ast.Load()), args=[], keywords=[]))],
                orelse=[]
            )
            fake_calls.append(fake_call)
        tree.body.extend(fake_calls)

def function_mirroring_obfuscate(code):
    try:
        tree = ast.parse(code)
        name_generator = NameGenerator()
        duplicator = FunctionDuplicator(name_generator)
        duplicator.visit(tree)
        duplicator.add_fake_calls(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception as e:
        logger.error(f"Error duplicating functions: {e}")
        return code
