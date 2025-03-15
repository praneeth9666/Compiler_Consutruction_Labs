import ast
from ast import *
prog=' '
with open("P0/input.py") as f:
    prog = f.read()
tree = ast.parse(prog)
for node in ast.walk(tree):
    if isinstance(node,ast.Name):
        print(f"Name: {node.id}")
