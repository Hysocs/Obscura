import ast
import astor

class InlineCodeObfuscator(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)  # Visit child nodes
        # Skip transformation for certain types that could break
        if isinstance(node.left, (ast.Call, ast.Attribute)) or isinstance(node.right, (ast.Call, ast.Attribute)):
            return node

        if isinstance(node.op, ast.Add):
            new_node = ast.BinOp(
                left=ast.BinOp(left=node.left, op=ast.Add(), right=ast.Constant(value=0)),
                op=ast.Add(),
                right=ast.BinOp(left=node.right, op=ast.Add(), right=ast.Constant(value=0))
            )
        elif isinstance(node.op, ast.Sub):
            new_node = ast.BinOp(
                left=ast.BinOp(left=node.left, op=ast.Add(), right=ast.Constant(value=0)),
                op=ast.Sub(),
                right=ast.BinOp(left=node.right, op=ast.Add(), right=ast.Constant(value=0))
            )
        elif isinstance(node.op, ast.Mult):
            new_node = ast.BinOp(
                left=ast.BinOp(left=node.left, op=ast.Mult(), right=ast.Constant(value=1)),
                op=ast.Mult(),
                right=ast.BinOp(left=node.right, op=ast.Mult(), right=ast.Constant(value=1))
            )
        elif isinstance(node.op, ast.Div):
            new_node = ast.BinOp(
                left=ast.BinOp(left=node.left, op=ast.Mult(), right=ast.Constant(value=1)),
                op=ast.Div(),
                right=ast.BinOp(left=node.right, op=ast.Mult(), right=ast.Constant(value=1))
            )
        else:
            return node
        return ast.copy_location(new_node, node)

def inline_code_obfuscate(code):
    try:
        tree = ast.parse(code)
        obfuscator = InlineCodeObfuscator()
        obfuscator.visit(tree)
        ast.fix_missing_locations(tree)
        return astor.to_source(tree)
    except Exception as e:
        print(f"Error during obfuscation: {e}")
        return code

# Example usage
if __name__ == "__main__":
    code = '''
class Example:
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.parent.move(self.parent.pos() + event.globalPos() - self.start)
            self.start = event.globalPos()
    '''
    obfuscated_code = inline_code_obfuscate(code)
    print(obfuscated_code)
