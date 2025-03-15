#!/usr/bin/env python3.10
import sys

import fa
import interference_graph as ig
import lifeanalysis as la
import x86IR_new as IR
import x86IR_correct as IR2
import optimize as opt
import CFG
import ast
import explicate
import precompute as pc

if len(sys.argv) < 2:
    print("Error: Missing input file")
    quit()

input_file = sys.argv[1]
source = open(input_file, 'r').read()
input_file = input_file.replace(".py", ".s")
output = open(input_file, 'w')


# /0x9 = TAB


def write_line(string, indentation=0):
    global output
    output.write(('\x09' * indentation) + string + '\n')


def check_for_invalid_ops(line):  # Checks for illegal memory to memory operations and
    # breaks it down into multiple lines.
    code = line
    if line.find(",") != -1:
        source = line[line.find(" ") + 1: line.find(",")]
        destination = line[line.find(",") + 2:]
        instruction = line[: line.find(" ")]
        if instruction == "movzbl" and destination.find("(") != -1:
            code = ("movzbl " + source + ", %edi\n")
            code += ("movl %edi, " + destination + "\n")
            return code
        #if instruction == "cmp" and source.find("$")     
        if source.find("(") != -1 and destination.find("(") != -1:
            code = ("movl " + source + ", %edi\n")
            if instruction == "movl":
                code += (instruction + " %edi, " + destination + "\n")
            if instruction == "cmp":
                code += (instruction + " " + destination + ", %edi\n")
            else:
                code += (instruction + " " + destination + ", %edi\n") 
                code += ("movl %edi, " + destination + "\n")
    return code


def py_to_x86(pseudocode, replacements, stack_bytes):
    write_line(".section .data")
    write_line("error_message:")
    write_line('    .string "Type Checking Error"')  
    write_line("\n.section .text")


    write_line(".global main")
    write_line("main:")
    write_line("pushl %ebp", 2)
    write_line("movl %esp, %ebp", 2)
    stack_size = stack_bytes * 4  # Calculates the amount of bytes needed for stack
    if stack_size != 0:  # Checks to see if the stack is even used
        write_line("subl $" + str(stack_size) + ", %esp", 2)
    write_line("")
    for x in replacements:  # Replaces variable names for their correctly assigned register
        if replacements[x].find("%") == -1:  # Checks to see if the replacement is a register
            pseudocode = pseudocode.replace(" " + str(x) + "\n", " %" + replacements[x] + "\n")
            pseudocode = pseudocode.replace(" " + str(x) + ",", " " + "%" + replacements[x] + ",")
        else:  # replacement is a stack memory address
            pseudocode = pseudocode.replace(" " + str(x) + "\n", " " + replacements[x] + "\n")
            pseudocode = pseudocode.replace(" " + str(x) + ",", " " + replacements[x] + ",")
    lines = pseudocode.rsplit("\n")
    for x in lines.copy():  # Makes sure there's no useless variable
        instruction = x[: x.find(" ")]
        if x.find(",") != -1:  # Checks to see if its an instruction with two operands
            source = x[x.find(" ") + 1: x.find(",")]
            destination = x[x.find(",") + 2:]
            if (source.find("$") == -1 and source.find("%") == -1) or (
                    destination.find("$") == -1 and destination.find("%") == -1):
                print("Removing Line: " + x)
                lines.remove(x)

    prevMov = False
    prevSource = None
    destination = None
    cpy = lines.copy()
    i = 0
    while i < len(
            lines):  # Deletes duplicate lines and reduces lines by reducing operations needed (aka unecessary mov instructions)
        line = lines[i]
        instruction = line[:line.find(" ")]
        if instruction == "movl":
            source = line[line.find(" ") + 1: line.find(",")]
            destination = line[line.find(",") + 2:].strip()
            if source == destination:
                lines.pop(i)
                continue
        i += 1

    revision = ""
    fin = True
    for x in lines:
        t = check_for_invalid_ops(x)
        if t == x:
            if not fin:
                fin = True
                revision += "popl %edi\n"
            revision += x + "\n"
        else:
            if fin:
                fin = False
                revision += "pushl %edi\n"
            revision += t
    lines = revision.rsplit("\n")
    for x in lines:
        write_line(x, 2)
        if "print_any" in x or "create_list" in x:
            write_line("addl $4, %esp\n", 2)
        '''if "is_big" in x or "is_int" in x or "inject_int" in x or "inject_big" in x or "inject_bool" in x or "project_int" in x or "project_big" in x:
            write_line("addl $4, %esp\n", 2)
        if "set_subscript" in x:
            write_line("addl $12, %esp\n", 2)
        if "get_subscript" in x or "add" in x:
            write_line("addl $8, %esp\n", 2) '''           
    write_line("movl $0, %eax", 2)
    write_line("leave", 2)
    write_line("ret", 2)


# FOR DEBUG
def print_side_by_side(code1, code2, tab_size=4):
    code1_lines = code1.replace('\t', ' ' * tab_size).split("\n")
    code2_lines = code2.replace('\t', ' ' * tab_size).split("\n")
    max_length_code1 = max(len(line) for line in code1_lines)
    header_padding = max_length_code1 + 3
    print(f"{'pre-optimized':<{header_padding}} | post-optimized")
    for i in range(max(len(code1_lines), len(code2_lines))):
        line1 = code1_lines[i] if i < len(code1_lines) else ""
        line2 = code2_lines[i] if i < len(code2_lines) else ""
        print(f"{line1:<{max_length_code1}}    |    {line2}")


def generate_og_explicate(source):
    fa.temp1 = -1
    fa.tmp_list = []
    tree = ast.parse(source)
    fa.pre_process_temps(source)
    transformer = explicate.ExplicateAdd()
    tree = transformer.visit(tree)
    flattened_code = fa.flattenAST(tree)
    return flattened_code

def generate_optimized_explicate(source):
    fa.temp1 = -1
    fa.tmp_list = []
    processed = fa.post_process_optimizations(source)
    processed = opt.process_code(processed)
    print(processed)
    tree = ast.parse(processed)
    transformer_pc = pc.Compute()
    tree = transformer_pc.visit(tree)
    fa.pre_process_temps(processed)
    transformer = explicate.ExplicateAdd()
    tree = transformer.visit(tree)
    optimized = fa.flattenAST(tree)
    return optimized


flattened_code = generate_og_explicate(source)
#old_code = generate_optimized_explicate(source)
#print_side_by_side(old_code, flattened_code)
print("\n\n\n")
print_side_by_side(source, flattened_code)
print("\n\n\n")
x86ir_unoptimized = IR2.flat_to_x86IR(flattened_code)
x86ir = IR2.flat_to_x86IR(flattened_code)
var_lst = IR.max_var(x86ir)
cfg = CFG.createCFG(x86ir)
la.gen_lives_list(cfg)
la.gen_lives_list(cfg)
la.gen_lives_list(cfg)
#cfg=opt.eliminate_dead_stores(cfg)
#cfg.clear_liveness()
#la.gen_lives_list(cfg)
#la.gen_lives_list(cfg)
#la.gen_lives_list(cfg)
#print(x86ir)
#print("\n\n\n")
res = ig.get_reg_replacements(cfg, var_lst)
#print("\n\n\n")
#print(res)
#print("\n\n\n")

cfg.print_cfg()

print_side_by_side(flattened_code, x86ir)

py_to_x86(x86ir, res[0], res[1])

output.close()
