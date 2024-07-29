import ast
import astor
import random
from Core.utils import name_generator


class DummyVariableInserter(ast.NodeTransformer):
    def __init__(self, dummy_args_min=1, dummy_args_max=3):
        self.dummy_args_min = dummy_args_min
        self.dummy_args_max = dummy_args_max
        self.obfuscation_flags = [name_generator.generate_name() for _ in range(3)]

    def generate_random_value(self):
        return random.choice([0, '', False, None, 0.0])

    def visit_FunctionDef(self, node):
        # Generate dummy arguments
        dummy_args_count = random.randint(self.dummy_args_min, self.dummy_args_max)
        dummy_args = [name_generator.generate_name() for _ in range(dummy_args_count)]
        dummy_values = [self.generate_random_value() for _ in range(dummy_args_count)]

        # Add dummy arguments to the function definition with default values
        for dummy_name, dummy_value in zip(dummy_args, dummy_values):
            node.args.args.append(ast.arg(arg=dummy_name, annotation=None))
            node.args.defaults.append(ast.Constant(value=dummy_value))

        # Add dummy variables in unreachable if statements
        selected_flag = random.choice(self.obfuscation_flags)
        condition_type = random.choice(['bool', 'int', 'math'])

        if condition_type == 'bool':
            condition = ast.Compare(left=ast.Name(id=selected_flag, ctx=ast.Load()), ops=[ast.Eq()], comparators=[ast.Constant(value=True)])
        elif condition_type == 'int':
            condition = ast.Compare(left=ast.Name(id=selected_flag, ctx=ast.Load()), ops=[ast.Eq()], comparators=[ast.Constant(value=1)])
        elif condition_type == 'math':
            condition = ast.Compare(left=ast.BinOp(left=ast.Name(id=selected_flag, ctx=ast.Load()), op=ast.Add(), right=ast.Constant(value=1)), ops=[ast.Eq()], comparators=[ast.Constant(value=1000)])

        unreachable_if = ast.If(
            test=condition,
            body=[
                ast.Assign(targets=[ast.Name(id=dummy_name, ctx=ast.Store())], value=ast.Constant(value=dummy_value))
                for dummy_name, dummy_value in zip(dummy_args, dummy_values)
            ] + [
                ast.Expr(value=ast.BinOp(left=ast.Name(id=dummy_name, ctx=ast.Load()), op=ast.Add(), right=ast.Constant(value=0)))
                if isinstance(dummy_value, (int, float)) else
                ast.Expr(value=ast.BinOp(left=ast.Name(id=dummy_name, ctx=ast.Load()), op=ast.Add(), right=ast.Constant(value='a')))
                if isinstance(dummy_value, str) else
                ast.Expr(value=ast.UnaryOp(op=ast.Not(), operand=ast.Name(id=dummy_name, ctx=ast.Load())))
                if isinstance(dummy_value, bool) else
                ast.Expr(value=ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[ast.Name(id=dummy_name, ctx=ast.Load())], keywords=[]))
                for dummy_name, dummy_value in zip(dummy_args, dummy_values)
            ],
            orelse=[]
        )

        # Insert the unreachable if statement at a random position in the function body
        insert_pos = random.randint(0, len(node.body))
        node.body.insert(insert_pos, unreachable_if)
        return node

def insert_dummy_variables(code, dummy_args_min=1, dummy_args_max=3):
    tree = ast.parse(code)
    inserter = DummyVariableInserter(dummy_args_min, dummy_args_max)
    tree = inserter.visit(tree)
    
    # Add the obfuscation flags at the top of the module with impossible conditions
    for flag in inserter.obfuscation_flags:
        condition_type = random.choice(['bool', 'int', 'math'])
        if condition_type == 'bool':
            flag_assign = ast.Assign(
                targets=[ast.Name(id=flag, ctx=ast.Store())],
                value=ast.Constant(value=False)
            )
        elif condition_type == 'int':
            flag_assign = ast.Assign(
                targets=[ast.Name(id=flag, ctx=ast.Store())],
                value=ast.BinOp(left=ast.Constant(value=1), op=ast.Add(), right=ast.Constant(value=1))
            )
        elif condition_type == 'math':
            flag_assign = ast.Assign(
                targets=[ast.Name(id=flag, ctx=ast.Store())],
                value=ast.BinOp(left=ast.Constant(value=1000), op=ast.Add(), right=ast.Constant(value=1))
            )
        tree.body.insert(0, flag_assign)
    
    return astor.to_source(tree)
