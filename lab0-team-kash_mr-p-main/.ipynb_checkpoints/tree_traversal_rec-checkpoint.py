import ast
from ast import *
prog=' '
with open("/home/jovyan/Compiler_Construction/lab0-team-kash_mr-p/P0/input.py") as f:
    prog = f.read()
tree = ast.parse(prog)
def print_names(node):
    if isinstance(node, ast.Name):
        print(f"Name: {node.id}")
    for child in ast.iter_child_nodes(node):
        print_names(child)
#print_names_recursive(tree)
print(ast.dump(tree,indent=2))    