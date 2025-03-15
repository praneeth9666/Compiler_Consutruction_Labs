#!/usr/bin/env python3.10
import sys

import fa
import interference_graph as ig
import lifeanalysis as la
import x86IR_new as IR
import x86IR_correct as IR2
import CFG
import ast

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
        if instruction == "movzbl":
            code = ("movzbl " + source + ", %eax\n")
            code += ("movl %eax, " + destination + "\n")
            return code
        if source.find("(") != -1 and destination.find("(") != -1:
            code = ("movl " + source + ", %eax\n")
            if instruction == "movl":
                code += (instruction + " %eax, " + destination + "\n")
            else:
                code += (instruction + " " + destination + ", %eax\n")
                code += ("movl %eax, " + destination + "\n")
    return code


def py_to_x86(pseudocode, replacements, stack_bytes):
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
    print(pseudocode)
    for x in lines.copy():  # Makes sure there's no useless variable
        instruction = x[: x.find(" ")]
        if x.find(",") != -1:  # Checks to see if its an instruction with two operands
            source = x[x.find(" ") + 1: x.find(",")]
            destination = x[x.find(",") + 2:]
            if (source.find("$") == -1 and source.find("%") == -1) or (
                    destination.find("$") == -1 and destination.find("%") == -1):
                lines.remove(x)

    prevMov = False
    prevSource = None
    destination = None
    cpy = lines.copy()
    i = 0
    while i < len(lines):  # Deletes duplicate lines and reduces lines by reducing operations needed (aka unecessary mov instructions)
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
                revision += "popl %eax\n"
            revision += x + "\n"
        else:
            if fin:
                fin = False
                revision += "pushl %eax\n"
            revision += t
    lines = revision.rsplit("\n")
    for x in lines:
        write_line(x, 2)
        if "print_int_nl" in x:
            write_line("addl $4, %esp\n", 2)
    write_line("movl $0, %eax", 2)
    write_line("leave", 2)
    write_line("ret", 2)


tree = ast.parse(source)
print(fa.pre_process_temps(source))
print("\n\n")
flattened_code = fa.flattenAST(tree)
print(flattened_code)
var_lst=IR.max_var(flattened_code)
x86ir = IR2.flat_to_x86IR(flattened_code)
print("IR")
print(x86ir)
cfg = CFG.createCFG(x86ir)
la.gen_lives_list(cfg)
res = ig.get_reg_replacements(cfg,var_lst)
cfg.print_cfg()
print(res)
py_to_x86(x86ir, res[0], res[1])


output.close()
