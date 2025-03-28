#!/usr/bin/env python3.10

import ast
from ast import *
import fa
import re

class IRInstruction:
    def __init__(self, opcode, operands=[]):
        self.opcode = opcode
        self.operands = operands

    def __repr__(self):
        operands_str = ", ".join(self.operands)
        if(self.opcode=="label"):
            return f"{operands_str}:"
        return f"{self.opcode} {operands_str}"
label_counter = 0

def generate_label(base, labels):
    if base in labels:
        labels[base] += 1
    else:
        labels[base] = 0
    label = f"{base}_{labels[base]}"
    return label

def max_var(string):
    sanitized = string.rsplit("\n")
    var_lst = []
    for x in sanitized:
        index = x.find(" =")
        temp = x.strip()
        if index == -1:
            continue
        var_name = temp[0:index]
        var_name = var_name.strip()
        if var_name not in var_lst:
            var_lst.append(var_name)    
    return var_lst

def process_line(line, var_lst,labels):
    instructions = []  
    if "eval(input())" in line:
        assignment = line.find(" =")
        if assignment != -1:
            destination = line[:assignment].strip()
            instructions.append(IRInstruction("call", ["eval_input_int"]))
            instructions.append(IRInstruction("movl", ["%eax", destination]))
        else:
            instructions.append(IRInstruction("call", ["eval_input_int"]))

    elif "-" in line:
        minus = line.find("-")
        operand = line[minus + 1:].strip()
        assignment = line.find(" =")
        destination = line[:assignment].strip() if assignment != -1 else "x"
        if operand.isnumeric():
            instructions.append(IRInstruction("movl", [f"${operand}", destination]))
        else:
            instructions.append(IRInstruction("movl", [operand, destination]))
        instructions.append(IRInstruction("negl", [destination]))
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
            if not operand1.isnumeric():
                instructions.append(IRInstruction("movl", [operand1, destination]))
                instructions.append(IRInstruction("addl", [f"${operand2}" if operand2.isnumeric() else operand2, destination]))
            else:
                instructions.append(IRInstruction("movl", [operand2, destination]))  
                instructions.append(IRInstruction("addl", [f"${operand1}", destination]))  

    elif "print" in line:    
        operand = line[line.find("(") + 1:line.find(")")].strip()
        instructions.append(IRInstruction("pushl", [operand if not operand.isnumeric() else f"${operand}"]))
        instructions.append(IRInstruction("call", ["print_int_nl"]))
    elif "==" in line:
        left, right_operand = line.split("==")
        destination, left_operand = left.split("=")
        destination=destination.replace(" ","")
        right_operand = right_operand.replace(" ", "")
        left_operand = left_operand.replace(" ", "")
        if left_operand.isnumeric() and right_operand.isnumeric():
            instructions.append(IRInstruction("movl", [f"${right_operand}", "%eax"]))
            instructions.append(IRInstruction("cmp", [f"${left_operand}","%eax" ]))
        if left_operand.isnumeric() or right_operand.isnumeric():
            if left_operand.isnumeric():
                instructions.append(IRInstruction("cmp", [ f"${left_operand}",right_operand]))
            else:
                instructions.append(IRInstruction("cmp", [f"${right_operand}",left_operand]))
        else:
            instructions.append(IRInstruction("cmp", [f"${left_operand}" if left_operand.isnumeric() else left_operand, f"${right_operand}" if right_operand.isnumeric() else right_operand]))
        instructions.append(IRInstruction("sete", ["%al"]))
        instructions.append(IRInstruction("movzbl", ["%al", destination]))

    elif "!=" in line:
        left, right_operand = line.split("!=")
        destination, left_operand = left.split("=")
        destination=destination.replace(" ","")
        right_operand = right_operand.replace(" ", "")
        left_operand = left_operand.replace(" ", "")
        if left_operand.isnumeric() and right_operand.isnumeric():
            instructions.append(IRInstruction("movl", [f"${right_operand}", "%eax"]))
            instructions.append(IRInstruction("cmp", [ f"${left_operand}","%eax"]))
        if left_operand.isnumeric() or right_operand.isnumeric():
            if left_operand.isnumeric():
                instructions.append(IRInstruction("cmp", [ f"${left_operand}",right_operand]))
            else:
                instructions.append(IRInstruction("cmp", [f"${right_operand}",left_operand]))    
        else:
            instructions.append(IRInstruction("cmp", [f"${left_operand}" if left_operand.isnumeric() else left_operand, f"${right_operand}" if right_operand.isnumeric() else right_operand]))
        instructions.append(IRInstruction("setne", ["%al"]))
        instructions.append(IRInstruction("movzbl", ["%al", destination]))

    elif "int(" in line:
        left_operand,right_operand = line.split("=")
        destination = re.search(r'int\((.*?)\)', right_operand)
        destination=destination.group(1)
        destination=destination.replace(" ","")
        left_operand=left_operand.replace(" ","")
        instructions.append(IRInstruction("movl",[destination,left_operand]))
    elif "=" in line:
        equals = line.find("=")
        operand = line[equals + 2:].strip()
        destination = line[:equals].strip()
        destination=destination.replace(" ","")
        operand_formatted = f"${operand}" if operand.isnumeric() else operand
        operand_formatted=operand_formatted.replace(" ","")
        instructions.append(IRInstruction("movl", [operand_formatted, destination]))

    return [str(instruction) for instruction in instructions]
def process_body(body_lines, var_lst, labels):
    instructions = []
    lines = body_lines.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("if") or line.startswith("while"):
            control_instrs, next_i = process_control_structure(line, var_lst, labels, lines, i)
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

    initial_indent = len(lines[start_index]) - len(lines[start_index].lstrip())
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

def process_control_structure(line, var_lst, labels, lines, start_index):
    instructions = []
    control_type = "if" if line.startswith("if") else "while"
    label_end = generate_label(control_type + '_end', labels)

    if control_type == "while":
        label_start = generate_label('while_start', labels)
        instructions.append(IRInstruction("label", [label_start]))
    condition_var = line.split()[1].replace(":","")
    if condition_var.isnumeric():
        instructions.append(IRInstruction("movl", [f"${condition_var}", "%eax"]))
        instructions.append(IRInstruction("cmp", ["$0", "%eax"]))
    else:
        instructions.append(IRInstruction("cmp", ["$0", condition_var]))

    # Temporarily hold off on adding the conditional jump instruction
    conditional_jump_index = len(instructions)  # Store the index where the jump instruction would be added

    # Process the body immediately to determine the presence of an 'else'
    body, next_line_index = get_body_lines(start_index, lines)
    body_instructions = process_body(body, var_lst, labels)
    instructions.extend(body_instructions)

    has_else = next_line_index < len(lines) and lines[next_line_index].strip().startswith("else")

    if control_type == "if":
        label_else = generate_label('else', labels) if has_else else None
        # Now decide where to jump based on the presence of an 'else' block
        if has_else:
            instructions.insert(conditional_jump_index, IRInstruction("je", [label_else]))
        else:
            instructions.insert(conditional_jump_index, IRInstruction("je", [label_end]))

        if has_else:
            instructions.append(IRInstruction("jmp", [label_end]))
            instructions.append(IRInstruction("label", [label_else]))
            else_body, next_line_index = get_body_lines(next_line_index, lines)  # Adjust next_line_index to skip 'else'
            else_body_instructions = process_body(else_body, var_lst, labels)
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
    
