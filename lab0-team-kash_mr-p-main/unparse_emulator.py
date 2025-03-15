import ast
from ast import *
# only thing thats not wokring is the - and space
prog=' '

# with open("/home/jovyan/4555/lab0-team-kash_mr-p/P0/input.py") as f:
with open("P0/1.2.py") as f:


    
    prog = f.read()

tree = ast.parse(prog)

nodeList = []
#our approach is to add all the needed nodes to 

def add_nodes(n):
    #What's the base case, when it's a leaf node, and its a leaf node when its a Name or a constant (a function or a constant)
    if isinstance(n, ast.Name):
        # nodeList.append('(')
        nodeList.append(n)

        # nodeList.append(')')
    elif isinstance(n, ast.Constant):
        
        nodeList.append(n)
        

    elif isinstance(n, Assign):
        nodeList.append(" New Line ")
        for target in n.targets:
            add_nodes(target)
        nodeList.append(' = ')
        add_nodes(n.value)
    elif isinstance(n, Expr):
        nodeList.append(" New Line ")
        # nodeList.append('(')
        add_nodes(n.value)
        # nodeList.append(')')
    elif isinstance(n, ast.BinOp):
        # nodeList.append('(')
        add_nodes(n.left)
        nodeList.append(n.op)
        add_nodes(n.right)
        # nodeList.append(')')
    elif isinstance(n, UnaryOp):
        nodeList.append(n.op)
        add_nodes(n.operand)
    elif isinstance(n, Module):
        for b in n.body:
            add_nodes(b)
    elif isinstance(n, Call):

        add_nodes(n.func)
        nodeList.append('(')
        for x in n.args:
            add_nodes(x)

        nodeList.append(')')
    else:
        print(n)
        raise Exception('Unrecognized')
    # elif isinstance(n, Add):
    #     return 1
    # elif isinstance(n, USub):
    #     return 1
    # elif isinstance(n, Load):
    #     return 1
    # elif isinstance(n, Store):
    #     return 1
    # else:
    #     add_nodes(n.)


add_nodes(tree)

# f = open("myfile.txt", "x")


temp = ""


for node in nodeList:
    if isinstance(node, ast.Constant):

        temp += str(node.value) 
    if isinstance(node, ast.Name):
        temp += node.id 
    elif isinstance(node, ast.Add):
        temp += " + "
    elif isinstance(node, ast.USub):
        temp += " - "
    elif(node == "("):
        temp += "("
    elif(node == ")"):
        temp += ")"
    elif(node == " = "):
        temp += " = "
    elif(node == " New Line "):
        temp += "\n"
    

print(temp)
with open('output.py', 'w') as file:
    file.write(temp)




# #post order traversal of the nodes and add them to a list, need to figure out where to put parentheses and spaces creat your program based on that
# #post order traversal and add to global list, then match every character to some sort of keyword, and create your program based on that
# list = []

# class ParentAdder(ast.NodeVisitor):
#     def visit(self, node):
#         if not hasattr(self, 'parent_node'):
#             self.parent_node = None        
#         setattr(node, 'parent', self.parent_node if hasattr(self, 'parent_node') else None)
#         temp = self.parent_node
#         self.parent_node = node
#         self.generic_visit(node)
#         self.parent_node = temp                
# parent_adder = ParentAdder()
# parent_adder.visit(tree)

# #if parent node is module, then add in some sort of line breaker or indicator to break line into the list
# def collect_names(node):
#     if(type(node.parent).__name__ == "Module" ):
#         print("Start of new\n")
#         list.append("lineBreak")
#     if isinstance(node, ast.Assign):
#         print("Assignment ")
#         list.append("Assign")
    
#     if isinstance(node, ast.Expr):
#         print("Expression")
#         list.append("Expr")

#     if isinstance(node, ast.Name):
#         print(f"Name: {node.id}")
#         list.append(node.id)
    
#     if isinstance(node, ast.USub):
#         print("-")
#         list.append('-')
#     if isinstance(node, ast.Add):
#         print("+")
#         list.append('+')
#     if isinstance(node, ast.Constant):
#         print(f"Name: {node.value}")
#         list.append(node.value)
#     for child in ast.iter_child_nodes(node):
#         collect_names(child)

# collect_names(tree)
# print("Start of list \n")

# f = open("myfile.txt", "x")


# temp = ""
# while i < len(list):
#     if (list[i] == "lineBreak"):
#         f.write(temp)
#         temp = ""
#     if(list[i] == "Assign"):
#         temp += list[i+1] + " = " 
#         i += 2
#     if(list[i] == "Expr"):
#         continue
#     if(list[i] == )
    
#     print(l)
