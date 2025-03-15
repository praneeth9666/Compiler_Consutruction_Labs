#!/usr/bin/env python3.10

import ast
from ast import *
import fa
import re

def is_special_numeric(x):
    if "-" in x:
        return x[1:].isnumeric()
    return x.isnumeric()

class IRInstruction:
    def __init__(self, opcode, operands=[]):
        self.opcode = opcode
        self.operands = operands

    def __repr__(self):
        operands_str = ", ".join(self.operands)
        if(self.opcode=="label"):
            return f"{operands_str}:"
        if(self.opcode=="text"):
            return f"{operands_str}"    
        return f"{self.opcode} {operands_str}"
global_label_counter = 0


def generate_label(base):
    global global_label_counter
    label = f"{base}_{global_label_counter}"
    global_label_counter += 1
    return label



def max_var(string):
    sanitized = string.rsplit("\n")
    var_lst = []
    for x in sanitized:
        tokens = x.split(" ")
        if len(tokens) < 2:
            continue
        if "call" in tokens[0] or ":" in tokens[0] or tokens[0][0] == "j":
            continue
        for y in range(1, len(tokens)):
            temp = tokens[y].replace(",","")
            if "$" in temp:
                continue
            if "%" not in temp and temp not in var_lst:
                var_lst.append(temp)
    return var_lst

def process_line(line, var_lst,labels):
    instructions = []
    neg_num = False
    if "print" in line:
        temp = line.replace("print_any(","").replace(")","").split(" ")
        if len(temp) == 1:
            neg_num = is_special_numeric(temp[0])

    if "eval_input_pyobj" in line:
        assignment = line.find(" =")
        if assignment != -1:
            destination = line[:assignment].strip()
            #instructions.append(IRInstruction("call", ["eval_input_int"]))
            instructions.append(IRInstruction("call", ["eval_input_pyobj"]))
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        else:
            instructions.append(IRInstruction("call", ["eval_input_int"]))
        return [str(instruction) for instruction in instructions]    
    elif "+" in line:
        add = line.find("+")
        assignment = line.find("=")
        operand1 = line[assignment + 2:line.find(" ", assignment + 2)].strip()
        operand2 = line[add + 2:].strip()
        destination = line[:assignment].strip()

        if operand1.isnumeric() and operand2.isnumeric():
            total = str(int(operand1) + int(operand2))
            instructions.append(IRInstruction("movl", [f"${total}", destination]))
        else:
            if not operand1.replace("-","").isnumeric():
                instructions.append(IRInstruction("movl", [operand1, destination]))
                print(f"op2{operand2}")
                instructions.append(IRInstruction("addl", [f"${operand2}" if operand2.replace("-","").isnumeric() else operand2, destination]))
            else:
                instructions.append(IRInstruction("movl", [operand2, destination]))  
                instructions.append(IRInstruction("addl", [f"${operand1}", destination]))
        return [str(instruction) for instruction in instructions]        
    elif "-" in line and not neg_num:
        minus = line.find("-")
        operand = line[minus + 1:].strip().replace(")","").replace("(","")
        assignment = line.find(" =")
        destination = line[:assignment].strip() if assignment != -1 else "x"
        if operand.isnumeric():
            instructions.append(IRInstruction("movl", ["$" + ("" if minus == -1 else "-") + operand, destination]))
        else:
            instructions.append(IRInstruction("movl", [operand, destination]))
            instructions.append(IRInstruction("negl", [destination]))
        return [str(instruction) for instruction in instructions]
    elif "print" in line:
        operand = line[line.find("(") + 1:line.find(")")].strip()
        instructions.append(IRInstruction("pushl", [operand if not is_special_numeric(operand) else f"${operand}"]))
        #instructions.append(IRInstruction("call", ["print_int_nl"]))
        instructions.append((IRInstruction("call",["print_any"])))
        return [str(instruction) for instruction in instructions]
    elif "==" in line:
        left, right_operand = line.split("==")
        destination, left_operand = left.split("=")
        destination=destination.replace(" ","")
        right_operand = right_operand.replace(" ", "")
        left_operand = left_operand.replace(" ", "")
        if left_operand.isnumeric() and right_operand.isnumeric():
            instructions.append(IRInstruction("movl", [f"${right_operand}", "%eax"]))
            instructions.append(IRInstruction("cmp", [f"${left_operand}","%eax" ]))
        elif left_operand.isnumeric() or right_operand.isnumeric():
            if left_operand.isnumeric():
                instructions.append(IRInstruction("cmp", [ f"${left_operand}",right_operand]))
            else:
                instructions.append(IRInstruction("cmp", [f"${right_operand}",left_operand]))
        else:
            instructions.append(IRInstruction("cmp", [f"${left_operand}" if left_operand.isnumeric() else left_operand, f"${right_operand}" if right_operand.isnumeric() else right_operand]))
        instructions.append(IRInstruction("sete", ["%al"]))
        instructions.append(IRInstruction("movzbl", ["%al", destination]))
        return [str(instruction) for instruction in instructions]
    elif "!=" in line:
        left, right_operand = line.split("!=")
        destination, left_operand = left.split("=")
        destination=destination.replace(" ","")
        right_operand = right_operand.replace(" ", "")
        left_operand = left_operand.replace(" ", "")
        if left_operand.isnumeric() and right_operand.isnumeric():
            instructions.append(IRInstruction("movl", [f"${right_operand}", "%eax"]))
            instructions.append(IRInstruction("cmp", [ f"${left_operand}","%eax"]))
        elif left_operand.isnumeric() or right_operand.isnumeric():
            if left_operand.isnumeric():
                instructions.append(IRInstruction("cmp", [ f"${left_operand}",right_operand]))
            else:
                instructions.append(IRInstruction("cmp", [f"${right_operand}",left_operand]))    
        else:
            instructions.append(IRInstruction("cmp", [f"${left_operand}" if left_operand.isnumeric() else left_operand, f"${right_operand}" if right_operand.isnumeric() else right_operand]))
        instructions.append(IRInstruction("setne", ["%al"]))
        instructions.append(IRInstruction("movzbl", ["%al", destination]))
        return [str(instruction) for instruction in instructions]
    if "is_int" in line:
        # Extract the variable to check
        start = line.find("is_int(") + len("is_int(")
        end = line.find(")", start)
        source = line[start:end].strip()

        # Find the assignment part to determine the destination variable
        assignment_index = line.find("=")
        if assignment_index != -1:
            destination = line[:assignment_index].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Move the source variable into %eax for the function call
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            
            # Call is_int; expects the argument in %eax and sets %eax to 1 (true) or 0 (false)
            instructions.append(IRInstruction("call", ["is_int"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the result from %eax to the destination variable
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        else:
            # Handle error or malformed line
            print("Error: Malformed is_int operation.")
        return [str(instruction) for instruction in instructions]
    elif "is_bool" in line:
        # Extract the variable to check
        start = line.find("is_bool(") + len("is_bool(")
        end = line.find(")", start)
        source = line[start:end].strip()

        # Find the assignment part to determine the destination variable
        assignment_index = line.find("=")
        if assignment_index != -1:
            destination = line[:assignment_index].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Move the source variable into %eax for the function call
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            
            # Call is_int; expects the argument in %eax and sets %eax to 1 (true) or 0 (false)
            instructions.append(IRInstruction("call", ["is_bool"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the result from %eax to the destination variable
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        else:
            # Handle error or malformed line
            print("Error: Malformed is_bool operation.")
        return [str(instruction) for instruction in instructions]    
    elif "is_big" in line:
        start = line.find("is_big(") + len("is_big(")
        end = line.find(")", start)
        source = line[start:end].strip()

        # Find the assignment part to determine the destination variable
        assignment_index = line.find("=")
        if assignment_index != -1:
            destination = line[:assignment_index].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Move the source variable into %eax for the function call
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            
            # Call is_int; expects the argument in %eax and sets %eax to 1 (true) or 0 (false)
            instructions.append(IRInstruction("call", ["is_big"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the result from %eax to the destination variable
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        else:
            # Handle error or malformed line
            print("Error: Malformed is_int operation.") 
        return [str(instruction) for instruction in instructions]
    if "is_function" in line:
        # Extract the variable to check
        start = line.find("is_function(") + len("is_function(")
        end = line.find(")", start)
        source = line[start:end].strip()

        # Find the assignment part to determine the destination variable
        assignment_index = line.find("=")
        if assignment_index != -1:
            destination = line[:assignment_index].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Move the source variable into %eax for the function call
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            
            # Call is_int; expects the argument in %eax and sets %eax to 1 (true) or 0 (false)
            instructions.append(IRInstruction("call", ["is_function"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the result from %eax to the destination variable
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        else:
            # Handle error or malformed line
            print("Error: Malformed is_int operation.")
        return [str(instruction) for instruction in instructions]           
    elif "inject_int" in line:
        # Find the assignment operation to determine the destination variable
        assignment = line.find(" = ")
        destination = line[:assignment].strip()
        # Extract the value to be injected from within the parentheses
        value = line[line.find("(")+1:line.find(")")].strip()
        value=value.replace(" ","")
        destination=destination.replace(" ","")
        # Move the value into %eax before calling 'inject_int'
        #instructions.append(IRInstruction("movl", [f"${value}" if value.isnumeric() else value, "%eax"]))
        instructions.append(IRInstruction("pushl",[f"${value}" if value.isnumeric() else value]))
        # Call 'inject_int', which now expects its argument in %eax
        instructions.append(IRInstruction("call", ["inject_int"]))
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        
        # Move the result from %eax to the destination variable
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    elif "inject_big" in line:
        # Find the assignment operation to determine the destination variable
        assignment = line.find(" = ")
        destination = line[:assignment].strip()
        # Extract the value to be injected from within the parentheses
        value = line[line.find("(")+1:line.find(")")].strip()
        value=value.replace(" ","")
        destination=destination.replace(" ","")
        # Move the value into %eax before calling 'inject_int'
        instructions.append(IRInstruction("pushl",[f"${value}" if value.isnumeric() else value]))
        # Call 'inject_int', which now expects its argument in %eax
        instructions.append(IRInstruction("call", ["inject_big"]))
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        # Move the result from %eax to the destination variable
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    elif "inject_bool" in line:
        # Find the assignment operation to determine the destination variable
        assignment = line.find(" = ")
        destination = line[:assignment].strip()
        # Extract the value to be injected from within the parentheses
        value = line[line.find("(")+1:line.find(")")].strip()
        value=value.replace(" ","")
        destination=destination.replace(" ","")
        # Move the value into %eax before calling 'inject_int'
        if "True" in value:
            instructions.append(IRInstruction("pushl",[f"$1"]))
        elif "False" in value:
            instructions.append(IRInstruction("pushl",[f"$0"]))
        else:
            instructions.append(IRInstruction("pushl",[f"${value}" if value.isnumeric() else value]))        
        # Call 'inject_int', which now expects its argument in %eax
        instructions.append(IRInstruction("call", ["inject_bool"]))
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        # Move the result from %eax to the destination variable
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]    
    elif "project_int" in line:
        assignment = line.find("=")
        if assignment != -1:
            source = line[line.find("(")+1:line.find(")")].strip()
            destination = line[:assignment].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Ensure the value to be projected is in %eax
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            # Call 'project_int'
            instructions.append(IRInstruction("call", ["project_int"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the projected integer (if any) from %eax to the destination
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    elif "project_bool" in line:
        assignment = line.find("=")
        if assignment != -1:
            source = line[line.find("(")+1:line.find(")")].strip()
            destination = line[:assignment].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Ensure the value to be projected is in %eax
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            # Call 'project_int'
            instructions.append(IRInstruction("call", ["project_bool"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the projected integer (if any) from %eax to the destination
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]    
    elif "project_big" in line:
        assignment = line.find("=")
        if assignment != -1:
            source = line[line.find("(")+1:line.find(")")].strip()
            destination = line[:assignment].strip()
            source=source.replace(" ","")
            destination=destination.replace(" ","")
            # Ensure the value to be projected is in %eax
            instructions.append(IRInstruction("pushl",[f"${source}" if source.isnumeric() else source]))
            # Call 'project_int'
            instructions.append(IRInstruction("call", ["project_big"]))
            #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
            # Move the projected integer (if any) from %eax to the destination
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    if "create_list" in line:
        # Extract the size (assuming it's directly provided as an argument)
        size = line[line.find("(")+1:line.find(")")]
        # Push the size onto the stack
        size=size.replace(" ","")
        instructions.append(IRInstruction("pushl", [f"${size}" if size.isnumeric() else size]))
        # Call create_list
        instructions.append(IRInstruction("call", ["create_list"]))
        # Clean up the stack if necessary (depending on calling convention)
        # Assuming callee cleans the stack
        # Store the result from %eax to a variable (assuming left-hand assignment)
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        destination = line.split("=")[0].strip()
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    if "is_true" in line:
        # Extract the size (assuming it's directly provided as an argument)
        size = line[line.find("(")+1:line.find(")")]
        # Push the size onto the stack
        size=size.replace(" ","")
        instructions.append(IRInstruction("pushl", [f"${size}" if size.isnumeric() else size]))
        # Call create_list
        instructions.append(IRInstruction("call", ["is_true"]))
        # Clean up the stack if necessary (depending on calling convention)
        # Assuming callee cleans the stack
        # Store the result from %eax to a variable (assuming left-hand assignment)
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        destination = line.split("=")[0].strip()
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]    
    elif "create_dict" in line:
        # Call create_list
        instructions.append(IRInstruction("call", ["create_dict"]))
        # Clean up the stack if necessary (depending on calling convention)
        # Assuming callee cleans the stack
        # Store the result from %eax to a variable (assuming left-hand assignment)
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        destination = line.split("=")[0].strip()
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    elif "add" in line:
        # Split the line to extract the destination and source variables
        parts = line.split("=")
        destination = parts[0].strip()
        sources = parts[1].split("add")[1].strip("()").split(",")
        source1 = sources[0].strip()
        source2 = sources[1].strip()
        source1=source1.replace(" ","")
        source2=source2.replace(" ","")
        destination=destination.replace(" ","")
        # Push source2 and source1 onto the stack in preparation for the call
        instructions.append(IRInstruction("pushl", [source2 if source2.isnumeric() else source2]))
        instructions.append(IRInstruction("pushl", [source1 if source1.isnumeric() else source1]))
        
        # Call the add function
        instructions.append(IRInstruction("call", ["add"]))
        
        # Assuming the result of the add operation is returned in %eax
        # Store the result from %eax to the destination variable
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    elif "not_equal" in line:
        # Split the line to extract the destination and source variables
        parts = line.split("=")
        destination = parts[0].strip()
        sources = parts[1].split("not_equal")[1].strip("()").split(",")
        source1 = sources[0].strip()
        source2 = sources[1].strip()
        source1=source1.replace(" ","")
        source2=source2.replace(" ","")
        destination=destination.replace(" ","")
        # Push source2 and source1 onto the stack in preparation for the call
        instructions.append(IRInstruction("pushl", [source2 if source2.isnumeric() else source2]))
        instructions.append(IRInstruction("pushl", [source1 if source1.isnumeric() else source1]))
        
        # Call the add function
        instructions.append(IRInstruction("call", ["not_equal"]))
        
        # Assuming the result of the add operation is returned in %eax
        # Store the result from %eax to the destination variable
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]    
    elif "equal" in line:
        # Split the line to extract the destination and source variables
        parts = line.split("=")
        destination = parts[0].strip()
        sources = parts[1].split("equal")[1].strip("()").split(",")
        source1 = sources[0].strip()
        source2 = sources[1].strip()
        source1=source1.replace(" ","")
        source2=source2.replace(" ","")
        destination=destination.replace(" ","")
        # Push source2 and source1 onto the stack in preparation for the call
        instructions.append(IRInstruction("pushl", [source2 if source2.isnumeric() else source2]))
        instructions.append(IRInstruction("pushl", [source1 if source1.isnumeric() else source1]))
        
        # Call the add function
        instructions.append(IRInstruction("call", ["equal"]))
        
        # Assuming the result of the add operation is returned in %eax
        # Store the result from %eax to the destination variable
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions] 
            
    elif "set_subscript" in line:
        parts = line.split(",")
        list_var = parts[0].split("(")[1].strip()
        index = parts[1].strip()
        value = parts[2].split(")")[0].strip()
        # Assuming the destination for the operation is handled elsewhere or not needed
        # Push value, index, and list_var onto the stack in reverse order
        value=value.replace(" ","")
        index=index.replace(" ","")
        list_var=list_var.replace(" ","")
        instructions.append(IRInstruction("pushl", [f"${value}" if value.isnumeric() else value]))
        instructions.append(IRInstruction("pushl", [f"${index}" if index.isnumeric() else index]))
        instructions.append(IRInstruction("pushl", [f"${list_var}" if list_var.isnumeric() else list_var]))
        # Call set_subscript
        instructions.append(IRInstruction("call", ["set_subscript"]))
        # Adjust the stack pointer by 12 to clean up the stack (assuming 32-bit integers, 3 arguments)
        #instructions.append(IRInstruction("addl", ["$12", "%esp"]))
        return [str(instruction) for instruction in instructions]
    if "get_subscript" in line:
        # Split the line to extract list variable and index
        parts = line.split("=")
        destination = parts[0].strip()
        list_var, index = parts[1].split("get_subscript")[1].strip("()").split(",")
        # Push index and list_var onto the stack
        index=index.replace(" ","")
        list_var=list_var.replace(" ","")
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("pushl", [index]))
        instructions.append(IRInstruction("pushl", [list_var]))
        # Call get_subscript
        instructions.append(IRInstruction("call", ["get_subscript"]))
        #instructions.append(IRInstruction("addl", ["$8", "%esp"]))
        # Assuming the function result is in %eax, store it to destination
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    if "create_closure" in line:
        # Split the line to extract list variable and index
        parts = line.split("=")
        destination = parts[0].strip()
        func, list_var = parts[1].split("create_closure")[1].strip("()").split(",")
        # Push index and list_var onto the stack
        func=func.replace(" ","")
        list_var=list_var.replace(" ","")
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("pushl", [list_var]))
        instructions.append(IRInstruction("pushl", [func]))
        # Call get_subscript
        instructions.append(IRInstruction("call", ["create_closure"]))
        #instructions.append(IRInstruction("addl", ["$8", "%esp"]))
        # Assuming the function result is in %eax, store it to destination
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
    if "get_free_vars" in line:
        # Extract the size (assuming it's directly provided as an argument)
        size = line[line.find("(")+1:line.find(")")]
        # Push the size onto the stack
        size=size.replace(" ","")
        instructions.append(IRInstruction("pushl", [f"${size}" if size.isnumeric() else size]))
        # Call create_list
        instructions.append(IRInstruction("call", ["get_free_vars"]))
        # Clean up the stack if necessary (depending on calling convention)
        # Assuming callee cleans the stack
        # Store the result from %eax to a variable (assuming left-hand assignment)
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        destination = line.split("=")[0].strip()
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions] 
    if "get_fun_ptr" in line:
        # Extract the size (assuming it's directly provided as an argument)
        size = line[line.find("(")+1:line.find(")")]
        # Push the size onto the stack
        size=size.replace(" ","")
        instructions.append(IRInstruction("pushl", [f"${size}" if size.isnumeric() else size]))
        # Call create_list
        instructions.append(IRInstruction("call", ["get_fun_ptr"]))
        # Clean up the stack if necessary (depending on calling convention)
        # Assuming callee cleans the stack
        # Store the result from %eax to a variable (assuming left-hand assignment)
        #instructions.append(IRInstruction("addl", ["$4", "%esp"]))
        destination = line.split("=")[0].strip()
        destination=destination.replace(" ","")
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]                             
    if "error_pyobj" in line:
        instructions.append(IRInstruction("pushl", ["error_message"]))
        instructions.append(IRInstruction("call", ["error_pyobj"]))
        return [str(instruction) for instruction in instructions]
    if '(' in line and ')' in line and line.endswith(')'):
        temp = line.split('(')[0].strip()
        function_name = temp.split("=")[1].strip()
        function_name = function_name.replace(" ","")
        params = line[line.find('(') + 1:line.find(')')].split(',')
        destination = line.split("=")[0].strip()
        destination=destination.replace(" ","")
        # Push parameters onto the stack in reverse order
        if len(params) != 0:
            for param in reversed(params):
                if param != "":
                    instructions.append(IRInstruction("pushl", [param.strip()]))
        instructions.append(IRInstruction("call", [function_name]))
        instructions.append(IRInstruction("movl", ["%eax", destination]))
        return [str(instruction) for instruction in instructions]
        # Clean up the stack after the call if it's caller-cleans convention
        #instructions.append(IRInstruction("addl", [f"${len(params) * 4}", "%esp"]))
    if line.startswith("return"):
        _, value = line.split()  
        value = value.strip()
        if value.isnumeric() or is_special_numeric(value):
            value = f"${value}"  
        instructions.append(IRInstruction("movl", [value, "%eax"]))
        return [str(instruction) for instruction in instructions]      
    elif "int(" in line:
        left_operand,right_operand = line.split("=")
        destination = re.search(r'int\((.*?)\)', right_operand)
        destination=destination.group(1)
        destination=destination.replace(" ","")
        left_operand=left_operand.replace(" ","")
        instructions.append(IRInstruction("movl",[destination,left_operand]))
        return [str(instruction) for instruction in instructions]            
    elif "=" in line:
        equals = line.find("=")
        operand = line[equals + 2:].strip()
        destination = line[:equals].strip()
        destination=destination.replace(" ","")
        operand_formatted = f"${operand}" if operand.isnumeric() else operand
        operand_formatted=operand_formatted.replace(" ","")
        instructions.append(IRInstruction("movl", [operand_formatted, destination]))
        return [str(instruction) for instruction in instructions]
        
    return [str(instruction) for instruction in instructions]
def process_function_definition(line, lines, start_index, labels):
    func_name, params = parse_function_def(line)
    print(params)
    stack_len = len(params) * 4
    instructions = [
        IRInstruction("label", [func_name]),
        IRInstruction("pushl", ["%ebp"]),
        IRInstruction("movl", ["%esp", "%ebp"]),
    ]
    instructions.append(IRInstruction("subl", ["error_replace", "%esp"]))
    offset = 8  
    for param in params:
        instructions.append(IRInstruction("movl", [f"%d(%%ebp)" % offset, param]))
        offset += 4  

    # Determine where the function's body starts (next line with increased indent)
    function_body, body_end_index = get_body_lines(start_index, lines)
    
    if not function_body.strip():
        print("Error: No function body found or body parsing failed.")
        return instructions, body_end_index

    # Process the function body
    local_var_lst = params
    local_labels = {}
    body_instructions = process_body(function_body, local_var_lst, local_labels,in_function=True)
    instructions.extend(body_instructions)
    instructions.append(IRInstruction("addl", ["$%d" % (len(params) * 4), "%esp"])) 
    instructions.append(IRInstruction("movl", ["%ebp", "%esp"]))
    instructions.append(IRInstruction("popl", ["%ebp"]))
    instructions.append(IRInstruction("ret", []))
    # Ensure there is a return at the end if not present
    return instructions, body_end_index

def process_body(body_lines, var_lst, labels,in_function=False,main_started=False):
    instructions = []
    lines = body_lines.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("def"):
            # Function definition detected
            func_instructions, next_i = process_function_definition(line, lines, i, labels)
            instructions.extend(func_instructions)
            i = next_i
        else:
            if not in_function and not main_started:
                # Insert the 'main:' label before any global scope code if it's the first statement outside functions
                instructions.append(IRInstruction("text", [".global main"]))
                instructions.append(IRInstruction("label", ["main"]))
                instructions.append(IRInstruction("pushl", ["%ebp"]))
                instructions.append(IRInstruction("movl", ["%esp", "%ebp"]))
                instructions.append(IRInstruction("subl", ["error_replace", "%esp"]))
                main_started=True    
            if line.startswith("if") or line.startswith("while"):
                control_instrs, next_i = process_control_structure(line, var_lst, labels, lines, i,in_function,main_started)
                instructions.extend(control_instrs)
                i = next_i
            else:
                line_instructions = process_line(line, var_lst, labels)
                instructions.extend(line_instructions)
                i += 1
    return instructions       
def get_body_lines(start_index, lines):
    body = ""  
    if start_index >= len(lines):
        return body, start_index

    initial_indent = len(lines[start_index]) - len(lines[start_index].lstrip(' \t'))
    #initial_indent = len(lines[start_index]) - len(lines[start_index].lstrip())
    current_index = start_index + 1

    while current_index < len(lines):
        line = lines[current_index]
        indent = len(line) - len(line.lstrip())

        
        if line.strip() == "" or indent > initial_indent:
            body += line + "\n"  
            current_index += 1
        else:
            break
    return body.rstrip(), current_index  
def parse_function_def(line):
    # Extract function name and parameters from the definition
    parts = line.split('(')
    func_name = parts[0].split()[1]
    params = parts[1].split(')')[0].split(',')
    return func_name.strip(), [param.strip() for param in params]


def process_control_structure(line, var_lst, labels, lines, start_index, in_function=False,main_started=False):
    instructions = []
    control_type = "if" if line.startswith("if") else "while"
    label_end = generate_label(control_type + '_end')

    if control_type == "while":
        label_start = generate_label('while_start')
        instructions.append(IRInstruction("label", [label_start]))
    condition_var = line.split()[1].replace(":","")
    if condition_var.isnumeric():
        instructions.append(IRInstruction("movl", [f"${condition_var}", "%eax"]))
        instructions.append(IRInstruction("cmp", ["$0", "%eax"]))
    else:
        instructions.append(IRInstruction("cmp", ["$0", condition_var]))

    conditional_jump_index = len(instructions)  

   
    body, next_line_index = get_body_lines(start_index, lines)
    body_instructions = process_body(body, var_lst, labels,in_function,main_started)
    instructions.extend(body_instructions)

    has_else = next_line_index < len(lines) and lines[next_line_index].strip().startswith("else")

    if control_type == "if":
        label_else = generate_label('else') if has_else else None
        if has_else:
            instructions.insert(conditional_jump_index, IRInstruction("je", [label_else]))
        else:
            instructions.insert(conditional_jump_index, IRInstruction("je", [label_end]))

        if has_else:
            instructions.append(IRInstruction("jmp", [label_end]))
            instructions.append(IRInstruction("label", [label_else]))
            else_body, next_line_index = get_body_lines(next_line_index, lines)  # Adjust next_line_index to skip 'else'
            else_body_instructions = process_body(else_body, var_lst, labels,in_function,main_started)
            instructions.extend(else_body_instructions)
    else:
        instructions.insert(conditional_jump_index, IRInstruction("je", [label_end]))
        # While loop: jump back to start for another iteration
        instructions.append(IRInstruction("jmp", [label_start]))

    instructions.append(IRInstruction("label", [label_end]))
    return instructions, next_line_index


def flat_to_x86IR(flat_ast):
    var_lst = max_var(flat_ast)
    labels = {}
    lines = flat_ast.split("\n")
    instructions = process_body("\n".join(lines), var_lst, labels)
    return "\n".join([str(instruction) for instruction in instructions])
    
