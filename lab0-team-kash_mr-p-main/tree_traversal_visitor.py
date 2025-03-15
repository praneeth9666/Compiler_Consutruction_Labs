import ast
from ast import *
prog=' '
with open("P0/input.py") as f:
    prog = f.read()
tree = ast.parse(prog)
class NameTraversal(ast.NodeVisitor):
    def visit_Name(self,node):
        if isinstance(node, ast.Name):
            print(f"Name: {node.id}")
        self.generic_visit(node)
visitor=NameTraversal()
visitor.visit_Name(tree)

