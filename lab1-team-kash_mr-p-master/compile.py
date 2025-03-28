import ast
import sys
if len(sys.argv) != 2:
        print("Usage: python script.py input_file.py")
        sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = input_file_path.replace('.py', '.s')
with open(input_file_path) as f:
    prog = f.read()

tree = ast.parse(prog)

tempCount = 0
nodeList = []
variables = {}
variable_list=[]

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
        variables[tempname] =1
        variable_list.append(tempname)
        return tempname
    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'eval':
        tempname = f"temp{tempCount}"
        tempCount += 1
        func_str = "eval(input())"
        nodeList.append(f"\n{tempname} = {func_str}")
        variables[tempname] = 1
        variable_list.append(tempname)
        return tempname
    elif isinstance(n, ast.Call):
        func_name = getattr(n.func, 'id', None)
        func_args = ', '.join([add_nodes(arg, True) for arg in n.args])
        func_str = f"{func_name}({func_args})"
        if func_name == "print":
            nodeList.append(f"\n{func_str}")
        elif complexParent:
            tempname = f"temp{tempCount}"
            nodeList.append(f"\n{tempname} = {func_str}")
            variables[tempname] = 1
            variable_list.append(tempname)
        else:
            nodeList.append(f"\n{func_str}")
            return ''
    elif isinstance(n, ast.Name):
        variable_name = n.id
        variables[variable_name] = 1
        variable_list.append(variable_name)
        return variable_name
    elif isinstance(n, ast.Constant):
        return str(n.value)
    elif isinstance(n, ast.Assign):
        target = n.targets[0]
        targID = target.id
        recVal = add_nodes(n.value, True)
        nodeList.append(f"\n{targID} = {recVal}")
        variables[targID] = 1
        variable_list.append(targID)
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

count=1
for i in variables:
    variables[i]=-4*count 
    count=count+1   
temp = ""
for node in nodeList:
    if node != '\nNone':
        temp += node
#print(temp)
with open('output2.py', 'w') as file:
    file.write(temp)

with open("output2.py") as f:
    prog = f.read()

tree = ast.parse(prog)
stack_len=count*4
assembly_code = f"""
.globl main
main:
    pushl %ebp       
    movl %esp, %ebp   
    subl ${stack_len}, %esp   
    pushl %ebx
    pushl %esi
    pushl %edi
"""
print(ast.dump(tree,indent=2))
def generate_assembly(node):
    global assembly_code
    if isinstance(node, ast.Assign):
        target = node.targets[0]
        variable = target.id
        value = node.value
        if isinstance(value, ast.BinOp):
            left = value.left.id if isinstance(value.left, ast.Name) else value.left.value
            right = value.right.id if isinstance(value.right, ast.Name) else value.right.value
            op = value.op.__class__.__name__
            if isinstance(value.left, ast.Name):
                left_operand = f"{variables[left]}(%ebp)"
            elif isinstance(value.left, ast.Constant):
                left_operand = f"${value.left.value}"
            if isinstance(value.right, ast.Name):
                right_operand = f"{variables[right]}(%ebp)"
            elif isinstance(value.right, ast.Constant):
                right_operand = f"${value.right.value}"
            assembly_code += f"    movl {left_operand}, %ecx\n"
            assembly_code += f"    addl {right_operand}, %ecx\n"
            assembly_code += f"    movl %ecx, {variables[variable]}(%ebp)\n"
        elif isinstance(value,ast.UnaryOp):
            operand = value.operand.id if isinstance(value.operand, ast.Name) else value.operand.value
            if isinstance(value.operand, ast.Name):
                operand = f"{variables[operand]}(%ebp)"
            elif isinstance(value.operand, ast.Constant):
                operand = f"${value.operand.value}"
            assembly_code += f"    movl {operand}, %ecx\n"
            assembly_code += f"    negl %ecx\n"
            assembly_code += f"    movl %ecx, {variables[variable]}(%ebp)\n"

        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'print':
            arg_name = value.args[0].id
            assembly_code += f"    pushl {variables[arg_name]}(%ebp)\n"\
            #assembly_code += f"    pushl %ecx\n"
            assembly_code += f"    call print_int_nl\n"
            assembly_code += f"    addl $4, %esp\n"
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'eval':
            assembly_code += "    call eval_input_int\n"
            assembly_code += f"    movl %eax, {variables[variable]}(%ebp)\n"
        elif isinstance(value, ast.Name):
            src_variable = value.id
            src_variable_location = f"{variables[src_variable]}(%ebp)"
            assembly_code += f"    movl {src_variable_location}, %ecx\n"
            assembly_code += f"    movl %ecx, {variables[variable]}(%ebp)\n"
        elif isinstance(value, ast.Constant):
            constant_value = value.value
            assembly_code += f"    movl ${constant_value}, {variables[variable]}(%ebp)\n"       
    elif isinstance(node, ast.Expr):
        value = node.value
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'print':
            arg_value = value.args[0]
            if isinstance(arg_value, ast.Constant):
                constant_value = arg_value.value
                assembly_code += f"    pushl ${constant_value}\n"
                assembly_code += "    call print_int_nl\n"
                assembly_code += "    addl $4, %esp\n"
            else:
                arg_name = value.args[0].id
                assembly_code += f"    pushl {variables[arg_name]}(%ebp)\n"\
                #assembly_code += f"    pushl %ecx\n"
                assembly_code += f"    call print_int_nl\n"
                assembly_code += f"    addl $4, %esp\n"    
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'eval':
            assembly_code += "    call eval_input_int\n"
            assembly_code += f"    movl %eax, {variables[variable]}(%ebp)\n"

# AST walk to generate assembly code
for node in ast.walk(tree):
        generate_assembly(node)       
assembly_code += """
    popl %edi        
    popl %esi
    popl %ebx
    movl $0, %eax    
    movl %ebp, %esp  
    popl %ebp       
    ret              
"""
       
print(assembly_code)
with open(output_file_path, 'w') as file:
    file.write(assembly_code)
