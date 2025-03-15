import ast

with open("P0/1.2.py") as f:
    prog = f.read()

tree = ast.parse(prog)

tempCount = 0
nodeList = []
variable = {}

def add_nodes(n, complexParent=False):
    global tempCount
    global nodeList

    if complexParent and isinstance(n, (ast.BinOp, ast.UnaryOp)):
        tempname = f"temp{tempCount}"
        tempCount += 1
        left = add_nodes(n.left, True) if isinstance(n, ast.BinOp) else ''
        right = add_nodes(n.right, True) if isinstance(n, ast.BinOp) else add_nodes(n.operand, True)
        if isinstance(n.op, ast.Add):
            nodeList.append(f"\n{tempname} = {left} {'+'} {right}")
        elif isinstance(n.op, ast.USub):
            nodeList.append(f"\n{tempname} = {left} {'-'} {right}")
        variable[tempname] =1
        return tempname
    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'eval':
        tempname = f"temp{tempCount}"
        tempCount += 1
        func_str = "eval(input())"
        nodeList.append(f"\n{tempname} = {func_str}")
        variable[tempname] = 1
        return tempname
    elif isinstance(n, ast.Call):
        func_name = getattr(n.func, 'id', None)
        func_args = ', '.join([add_nodes(arg, True) for arg in n.args])
        func_str = f"{func_name}({func_args})"
        if complexParent:
            tempname = f"temp{tempCount}"
            nodeList.append(f"\n{tempname} = {func_str}")
            variable[tempname] = 1
        else:
            nodeList.append(f"\n{func_str}")
            return ''
    elif isinstance(n, ast.Name):
        variable_name = n.id
        variable[variable_name] = 1
        return variable_name
    elif isinstance(n, ast.Constant):
        return str(n.value)
    elif isinstance(n, ast.Assign):
        target = n.targets[0]
        targID = target.id
        recVal = add_nodes(n.value, True)
        nodeList.append(f"\n{targID} = {recVal}")
        variable[targID] = 1
        return targID
    elif isinstance(n, ast.Expr):
        expVal = add_nodes(n.value, True)
        nodeList.append(f"\n{expVal}")
        return expVal
    elif isinstance(n, ast.Module):
        for b in n.body:
            add_nodes(b, False)

# Call the function to process the AST
add_nodes(tree)



temp = ""

for node in nodeList:
    if node != '\nNone':
        temp += node
print(temp)
with open('output2.py', 'w') as file:
    file.write(temp)



        
#print(ast.dump(tree,indent=2))
