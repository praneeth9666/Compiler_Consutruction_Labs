import ast
from ast import *
prog=' '
<<<<<<< HEAD
with open("/home/jovyan/Compiler_Construction/lab0-team-kash_mr-p/P0/print.py") as f:
    prog = f.read()
tree = ast.parse(prog)
class AddParent(ast.NodeVisitor):
    def visit_Name(self,node,parent=None):
        if isinstance(node, ast.Name):
            print(f"Name: {node.id}")
=======
with open("/home/jovyan/Compiler_Construction/lab0-team-kash_mr-p/P0/input.py") as f:
    prog = f.read()
tree = ast.parse(prog)
class AddParent(ast.NodeVisitor):
    def visit_Name(self,node):
        if isinstance(node, ast.Name):
            print(f"Name: {node.id}")
            
>>>>>>> bb35613b0adcdc30b8577e27915cbf86c4921bb9
            #print(node._fields)
            
        #parent=node.parent;    
        self.generic_visit(node)
<<<<<<< HEAD
visitor=AddParent()
visitor.visit_Name(tree)
for node in ast.walk(tree):
    print(node._fields)
    node._fields.
        
=======
class AddParent1(ast.NodeTransformer):
    def visitor(self,node,parent=None):
        if isinstance(node, ast.Name):
            print(f"Name: {node.id}")
            
            #print(node._fields)
            
        #parent=node.parent;    
        self.generic_visit(node)
class ParentAdder(ast.NodeVisitor):
    def visit(self, node):
        if not hasattr(self, 'parent_node'):
            self.parent_node = None    
        setattr(node, 'parent', self.parent_node if hasattr(self, 'parent_node') else None)
        old_parent_node = self.parent_node
        self.parent_node = node
        super().visit(node)
        self.parent_node = old_parent_node                
visitor=AddParent()
visitor.visit_Name(tree)
parent_adder = ParentAdder()
parent_adder.visit(tree)
for node in ast.walk(tree):
    print(f"{type(node).__name__}: Parent - {type(node.parent).__name__ if node.parent else None}")
for node in ast.walk(tree):
    print(node._fields)
>>>>>>> bb35613b0adcdc30b8577e27915cbf86c4921bb9

