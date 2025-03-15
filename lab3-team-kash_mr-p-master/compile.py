import ast
import sys
if len(sys.argv) != 2:
        print("Usage: python script.py input_file.py")
        sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = input_file_path.replace('.py', '.s')
with open(input_file_path) as f:
    prog = f.read()

import ply.lex as lex
import ast
from ast import *



tree=ast.parse(prog)
#print(ast.dump(tree,indent=2))

class Instruction:
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands 
    def __str__(self):
        # Format the instruction for printing
        return f"{self.opcode} {' '.join(self.operands)}"
    def get_read_variables(self):
        read_vars = []
        if self.opcode in ['movl', 'addl', 'pushl', 'negl']:
            read_vars.append(self.operands[0])
        elif self.opcode == 'call':
            read_vars.append(self.operands[1])       
        return set(var for var in read_vars if not var.startswith('$'))

    def get_written_variables(self):
        if self.opcode in ['movl', 'addl']:
            return set([self.operands[1]])
        elif self.opcode in ['negl']:
            return set([self.operands[0]])    
        return set()          

class AssemblyIR:
    def __init__(self):
        self.instructions = []
    def add_instruction(self, opcode, operands):
        self.instructions.append(Instruction(opcode, operands))
    def print_assembly(self):
        for instruction in self.instructions:
            print(instruction)
    def get_instructions(self):
        return self.instructions
    def set_instructions(self,instructions):
        self.instructions=instructions   
    def del_redundant_movs(self):
        self.instructions = [instr for instr in self.instructions if not (
            instr.opcode == 'movl' and instr.operands[0] == instr.operands[1]
        )]               

tempCount = 0
nodeList = []
variables = {}
variable_list=[]

def add_nodes(n, complexParent=False):
    global tempCount
    global nodeList

    if complexParent and isinstance(n, (ast.BinOp, ast.UnaryOp)):
        '''if isinstance(n, ast.BinOp) and (isinstance(n.left, ast.Name) or isinstance(n.left, ast.Constant)) and (isinstance(n.right, ast.Name) or isinstance(n.right, ast.Constant)):
            left = add_nodes(n.left, True)
            right = add_nodes(n.right, True)
            operation = '+' if isinstance(n.op, ast.Add) else '-'  # Extend this for other operations as needed
            return f"{left} {operation} {right}"'''    
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
        if not recVal.startswith('temp'):
            nodeList.append(f"\n{targID} = {recVal}")
        else:    
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

with open('output2.py', 'w') as file:
    file.write(temp)

with open("output2.py") as f:
    prog = f.read()

tree = ast.parse(prog)
stack_len=count*4
assembly_code=" "
ir = AssemblyIR()
#print(ast.dump(tree,indent=2))
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
                #left_operand = f"{variables[left]}(%ebp)"
                left_operand=f"{left}"
            elif isinstance(value.left, ast.Constant):
                left_operand = f"${value.left.value}"
            if isinstance(value.right, ast.Name):
                right_operand = f"{right}"
            elif isinstance(value.right, ast.Constant):
                right_operand = f"${value.right.value}"
            ir.add_instruction("movl", [left_operand,variable]) 
            ir.add_instruction("addl", [right_operand,variable])   
            assembly_code += f"    movl {left_operand}, {variable}\n"
            assembly_code += f"    addl {right_operand}, {variable}\n"
            #assembly_code += f"    movl , {variables[variable]}(%ebp)\n"
        elif isinstance(value,ast.UnaryOp):
            operand = value.operand.id if isinstance(value.operand, ast.Name) else value.operand.value
            if isinstance(value.operand, ast.Name):
                operand = f"{operand}"
            elif isinstance(value.operand, ast.Constant):
                operand = f"${value.operand.value}"
            ir.add_instruction("movl", [operand,variable])
            assembly_code += f"    movl {operand}, {variable}\n"
            #assembly_code += f"    movl {operand}, %ecx\n"
             
            ir.add_instruction("negl", [variable]) 
            assembly_code += f"    negl {variable}\n"
            #assembly_code += f"    movl %ecx, {variables[variable]}(%ebp)\n"

        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'print':
            arg_name = value.args[0].id
            ir.add_instruction("pushl", [arg_name])
            assembly_code += f"    pushl {arg_name}\n"\
            #assembly_code += f"    pushl %ecx\n"
            ir.add_instruction("call", ["print_int_nl"])
            assembly_code += f"    call print_int_nl\n"
            #assembly_code += f"    addl $4, %esp\n"
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'eval':
            ir.add_instruction("call", ["eval_input_int",f"{variable}"])
            assembly_code += f"    call eval_input_int {variable}\n"
            #assembly_code += "    call eval_input_int\n"
            #ir.add_instruction("movl", ["%eax",variable])
            #assembly_code += f"    movl %eax, {variable}\n"
        elif isinstance(value, ast.Name):
            src_variable = value.id
            src_variable_location = f"{variables[src_variable]}(%ebp)"
            #assembly_code += f"    movl {src_variable}, %ecx\n"
            ir.add_instruction("movl", [src_variable,variable])
            assembly_code += f"    movl {src_variable}, {variable}\n"
        elif isinstance(value, ast.Constant):
            constant_value = value.value
            ir.add_instruction("movl", [f"${constant_value}",variable])
            assembly_code += f"    movl ${constant_value}, {variable}\n"         
    elif isinstance(node, ast.Expr):
        value = node.value
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'print':
            arg_value = value.args[0]
            if isinstance(arg_value, ast.Constant):
                constant_value = arg_value.value
                #ir.add_instruction("pushl", [constant_value])
                #assembly_code += f"    pushl ${constant_value}\n"
                ir.add_instruction("call", ["print_int_nl",f"${constant_value}"])
                assembly_code += "    call print_int_nl\n"
                #assembly_code += "    addl $4, %esp\n"

            else:
                arg_name = value.args[0].id
                #ir.add_instruction("pushl", [arg_name])
                #assembly_code += f"    pushl {arg_name}\n"
                #assembly_code += f"    pushl %ecx\n"
                ir.add_instruction("call", ["print_int_nl",f"{arg_name}"])
                assembly_code += f"    call print_int_nl {arg_name}\n"
                #assembly_code += f"    addl $4, %esp\n"    
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'eval':
            ir.add_instruction("call", ["eval_input_int",f"{variable}"])
            assembly_code += f"    call eval_input_int {variable}\n"
            #ir.add_instruction("movl", ["%eax",variable])
            #assembly_code += f"    movl %eax, {variable}\n"

# AST walk to generate assembly code
for node in ast.walk(tree):
        generate_assembly(node)       

       
#print(assembly_code)



ir.del_redundant_movs()        
#ir.print_assembly()


def liveness_analysis(instructions):
    live_after_sets = [set() for _ in instructions]
    live_before_sets = [set() for _ in instructions]
    for i in reversed(range(len(instructions))):
        if i < len(instructions) - 1:
            live_after_sets[i] = live_before_sets[i + 1]    
        live_before_sets[i] = (live_after_sets[i] - instructions[i].get_written_variables()) | instructions[i].get_read_variables()
    return live_before_sets, live_after_sets

def build_interference_graph(instructions, live_after_sets):
    graph = {}
    caller_save_registers = ['eax', 'ecx', 'edx']
    for i, instr in enumerate(instructions):
        live_after = live_after_sets[i]
        for var in instr.get_written_variables():
            graph.setdefault(var, set())

        
        for live_var in live_after:
            graph.setdefault(live_var, set())
        '''if instr.opcode == 'movl':
            s, t = instr.operands[0], instr.operands[1]
            for v in live_after:
                #print(f"{s} and {t} and {v}")
                if v != t and v != s:
                    graph.setdefault(t, set()).add(v)
                    graph.setdefault(v, set()).add(t)'''
        if instr.opcode == 'movl':
            if len(instr.operands) > 1:  
                target = instr.operands[1]
                for live_var in live_after:
                    if live_var != target:
                        graph[target].add(live_var)
                        graph[live_var].add(target)            
        elif instr.opcode in ['addl', 'subl']:
            t = instr.operands[1]
            for v in live_after:
                if v != t:
                    graph.setdefault(t, set()).add(v)
                    graph.setdefault(v, set()).add(t)
        elif instr.opcode in ['negl']:
            t = instr.operands[0]
            for v in live_after:
                if v != t:
                    graph.setdefault(t, set()).add(v)
                    graph.setdefault(v, set()).add(t)            
        elif instr.opcode == 'call':
            target = instr.operands[1]
            for live_var in live_after:
                if live_var != target:
                    graph[target].add(live_var)
                    graph[live_var].add(target)
            '''for r in caller_save_registers:
                for v in live_after:
                    graph.setdefault(r, set()).add(v)
                    graph[v].add(r)
                    #graph.setdefault(v, set()).add(r)'''           
    return graph
'''def build_interference_graph(instructions, live_after_sets):
    graph = {}
    for i, instr in enumerate(instructions):
        # Ensure all live variables at this point interfere with the variable being written
        written_vars = instr.get_written_variables()
        for var in written_vars:
            graph.setdefault(var, set())
        for live_var in live_after_sets[i]:
            for var in written_vars:
                if live_var != var:
                    print(f"{var} and {live_var}")
                    graph[var].add(live_var)
                    graph[live_var].add(var)
    return graph'''

       
def color_graph(graph, available_registers):
    colors = {node: None for node in graph}
    node_saturation = {node: 0 for node in graph}

    def select_node():
        uncolored_nodes = [node for node in graph if colors[node] is None]
        if not uncolored_nodes:
            return None
        # Sort by saturation degree, then by degree
        uncolored_nodes.sort(key=lambda node: (node_saturation[node], len(graph[node])), reverse=True)
        return uncolored_nodes[0]

    def update_saturation(node, colored_with):
        for neighbor in graph[node]:
            if colored_with not in [colors[n] for n in graph[neighbor] if colors[n] is not None]:
                node_saturation[neighbor] += 1

    while any(color is None for color in colors.values()):
        progress_made = False
        node = select_node()
        if node is None:
            break  
        
        neighbor_colors = {colors[neighbor] for neighbor in graph[node] if colors[neighbor] is not None}
        for color in range(available_registers):
            if color not in neighbor_colors:
                colors[node] = color
                update_saturation(node, color)
                progress_made = True
                break
        
        if not progress_made:
            # No progress in this iteration; need to spill
            break

    return colors
'''def color_graph(graph, available_registers):
    """
    Colors a graph using a greedy algorithm, suitable for register allocation.

    :param graph: The interference graph, where each node represents a variable,
                  and edges represent interferences between variables.
    :param available_registers: The number of available registers (colors).
    :return: A tuple of (coloring, spills), where coloring is a dictionary mapping
             nodes to their assigned colors (registers), and spills is a set of nodes
             that could not be colored and thus need to be spilled.
    """
    coloring = {}  # Maps nodes to colors (registers)
    spills = set()  # Set of nodes that need to be spilled

    # Attempt to color each node
    for node in graph:
        forbidden_colors = set()
        for neighbor in graph[node]:
            if neighbor in coloring:
                forbidden_colors.add(coloring[neighbor])
        
        # Find the lowest color that is not forbidden
        assigned_color = None
        for color in range(available_registers):
            if color not in forbidden_colors:
                assigned_color = color
                break
        
        if assigned_color is not None:
            coloring[node] = assigned_color
        else:
            coloring[node] = None
            #spills.add(node)
    
    return coloring'''



def insert_spill_code_with_temp(instructions, spill_var,temp_var_counter):
    #temp_var = f"temp0"  # Naming the temporary variable
    modified_instructions = []
    #temp_var = f"temp{temp_var_counter}"
    for instr in instructions:
        if spill_var in instr.get_read_variables() or spill_var in instr.get_written_variables():
            temp_var = f"temp_ir{temp_var_counter}"  
            new_operands = [temp_var if op == spill_var else op for op in instr.operands]
            
            
            if instr.opcode in ['addl', 'negl']: 
                modified_instructions.append(Instruction('movl', [spill_var, temp_var]))  
                modified_instructions.append(Instruction(instr.opcode, new_operands))  
                if spill_var in instr.get_written_variables():
                    modified_instructions.append(Instruction('movl', [temp_var, spill_var]))  
            else:
                modified_instructions.append(instr)
        else:
            modified_instructions.append(instr)

    return modified_instructions

def allocate_registers_iteratively(instructions, available_registers):
    spill_count = 0
    temp_counter = 0
    previous_spills = set()
    variables_spilled = False

    while True:
        live_before_sets, live_after_sets = liveness_analysis(instructions)
        #print(f"after{live_after_sets}")
        #print(f"before{live_before_sets}")
        interference_graph = build_interference_graph(instructions, live_after_sets)
        #print(f"graph{interference_graph}")
        coloring = color_graph(interference_graph, available_registers)
        #print("Current Coloring:", coloring)

        current_spills = {var for var, color in coloring.items() if color is None}
        #print("Current Spills:", current_spills)

        
        if current_spills == previous_spills:
            print("No progress made in resolving spills; terminating iterative process.")
            break

        if not current_spills:
            print("All variables successfully allocated to registers.")
            break
        else:
            for spill_var in current_spills:
                instructions = insert_spill_code_with_temp(instructions, spill_var, temp_counter)
                temp_counter += 1
                spill_count += 1 
            #spill_var = next(iter(current_spills))
            #print(spill_var)
            #instructions = insert_spill_code_with_temp(instructions, spill_var, temp_counter)
            variables_spilled = True
            #temp_counter += 1
            
        previous_spills = current_spills
        if spill_count > 5:
            live_before_sets, live_after_sets = liveness_analysis(instructions)
            interference_graph = build_interference_graph(instructions, live_after_sets)
            coloring = color_graph(interference_graph, available_registers)
            print("Spill limit exceeded")
            break 

    return instructions, coloring, current_spills

available_registers = 3 
instructions, coloring, spilled = allocate_registers_iteratively(ir.get_instructions(), available_registers)

for instr in instructions:
    print(instr)
def generate_allocations(coloring, available_registers):
    
    # Fixed mapping from colors to register names
    color_to_register = {0: '%edi', 1: '%ebx', 2: '%esi', 3: '%edx', 4: '%esi', 5: '%edi'}
    

    allocations = {}
    stack_offset = 4  
    available_register_indexes = list(range(available_registers))
    for variable, color in coloring.items():
        if color is not None and color in available_register_indexes:
            allocations[variable] = color_to_register[color]
        else:
            allocations[variable] = f"-{stack_offset}(%ebp)"
            stack_offset += 4

    return allocations,stack_offset
#allocations = generate_allocations(coloring, available_registers)

def convert_to_assembly(instructions, allocations, stack_len):
    assembly_code = [
        ".globl main",
        "main:",
        "\tpushl %ebp",
        "\tmovl %esp, %ebp",
        f"\tsubl ${stack_len}, %esp",
        "\tpushl %ebx",
        "\tpushl %esi",
        "\tpushl %edi",
    ]

    for instruction in instructions:
        opcode = instruction.opcode
        operands = instruction.operands
        allocated_operands = [allocations.get(operand, operand) for operand in operands]

        if opcode == "call" and operands[0] == "print_int_nl":
            variable_location = allocated_operands[1]
            assembly_code.append(f"\tpushl {variable_location}")
            assembly_code.append("\tcall print_int_nl")
            assembly_code.append("\taddl $4, %esp")
        elif opcode == "call" and operands[0] == "eval_input_int":
            variable_location = allocated_operands[1]
            assembly_code.append("\tcall eval_input_int")
            assembly_code.append(f"\tmovl %eax, {variable_location}")
        elif opcode == "movl" and all(op.startswith('-') for op in allocated_operands):
            assembly_code.append(f"\tmovl {allocated_operands[0]}, %edx")
            assembly_code.append(f"\tmovl %edx, {allocated_operands[1]}")
        elif opcode == "addl" and allocated_operands[1].startswith('-'):
            
            src, dest = allocated_operands
            #if src.startswith('-'):
            #    assembly_code.append(f"\tmovl {src}, %esi")
            #    src="%esi"
            if dest.startswith('-'):
                assembly_code.append(f"\tmovl {dest}, %edx")
            assembly_code.append(f"\taddl {src}, %edx")  
            assembly_code.append(f"\tmovl %edx, {dest}") 
        else:
            if opcode == "movl" and allocated_operands[0] == allocated_operands[1]:
                continue  
            asm_instruction = f"\t{opcode} {','.join(allocated_operands)}"
            assembly_code.append(asm_instruction)    
        
        

    assembly_code += [
        "\tpopl %edi",
        "\tpopl %esi",
        "\tpopl %ebx",
        "\tmovl $0, %eax",
        "\tmovl %ebp, %esp",
        "\tpopl %ebp",
        "\tret",
    ]

    return assembly_code


allocations, stack_len = generate_allocations(coloring, available_registers)
assembly_code = convert_to_assembly(instructions, allocations, stack_len)
for variable, location in allocations.items():
    print(f"{variable}: {location}")
for line in assembly_code:
    print(line)
with open(output_file_path, 'w') as file:
    for line in assembly_code:
        file.write(line + "\n")       

    




    

