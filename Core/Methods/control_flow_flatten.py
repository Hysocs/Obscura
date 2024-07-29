import ast
import logging
from Core.utils import name_generator  # Import the name_generator instance

logger = logging.getLogger(__name__)

class ControlFlowFlattener(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        new_body = []
        state_counter = 1
        states = {}

        # Generate a random name for the state variable
        state_var_name = name_generator.generate_name()
        state_var = ast.Name(id=state_var_name, ctx=ast.Store())
        state_value = ast.Constant(value=state_counter)
        new_body.append(ast.Assign(targets=[state_var], value=state_value))

        for stmt in node.body:
            state_name = f"{state_var_name}_{state_counter}"
            state_counter += 1
            states[state_name] = stmt

        while_loop = ast.While(
            test=ast.Compare(
                left=ast.Name(id=state_var_name, ctx=ast.Load()),
                ops=[ast.NotEq()],
                comparators=[ast.Constant(value=-1)]
            ),
            body=[],
            orelse=[]
        )

        for state_name, stmt in states.items():
            try:
                state_index = int(state_name.split('_')[-1])
                next_state = state_index + 1 if state_index < state_counter else -1
                if_node = ast.If(
                    test=ast.Compare(
                        left=ast.Name(id=state_var_name, ctx=ast.Load()),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=state_index)]
                    ),
                    body=[stmt, ast.Assign(targets=[ast.Name(id=state_var_name, ctx=ast.Store())], value=ast.Constant(value=next_state))],
                    orelse=[]
                )
                while_loop.body.append(if_node)
            except ValueError:
                logger.error(f"Failed to parse state index from state name: {state_name}")

        # Ensure the last state is set to -1 to terminate the loop
        terminate_if = ast.If(
            test=ast.Compare(
                left=ast.Name(id=state_var_name, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=state_counter)]
            ),
            body=[ast.Assign(targets=[ast.Name(id=state_var_name, ctx=ast.Store())], value=ast.Constant(value=-1))],
            orelse=[]
        )
        while_loop.body.append(terminate_if)

        new_body.append(while_loop)
        node.body = new_body

        return node


def control_flow_flatten_obfuscate(code):
    tree = ast.parse(code)
    flattener = ControlFlowFlattener()
    flattened_tree = flattener.visit(tree)
    ast.fix_missing_locations(flattened_tree)
    return ast.unparse(flattened_tree)
