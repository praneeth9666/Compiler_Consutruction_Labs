import ast
from ast import *
prog=' '
with open("P0/input.py") as f:
    prog = f.read()
tree = ast.parse(prog)
class ParentAdder(ast.NodeVisitor):
    def visit(self, node):
        if not hasattr(self, 'parent_node'):
            self.parent_node = None        
        setattr(node, 'parent', self.parent_node if hasattr(self, 'parent_node') else None)
        temp = self.parent_node
        self.parent_node = node
        self.generic_visit(node)
        self.parent_node = temp                
parent_adder = ParentAdder()
parent_adder.visit(tree)
for node in ast.walk(tree):
    print(f"{type(node).__name__}: Parent - {type(node.parent).__name__}")
    #print(type(node).)

