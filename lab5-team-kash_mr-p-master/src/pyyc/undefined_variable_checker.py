#!/usr/bin/env python3.10
import sys

if len(sys.argv) < 2:
    print("Error: Missing input file")
    quit()

input_file = sys.argv[1]
source = open(input_file, 'r').read()

def is_keyword(s):
    return s in ['if', 'else', 'while', 'int', 'not', 'and', 'or'] or s.isdigit() or s == 'True' or s == 'False' or "(" in s or ")" in s or "==" in s or "!=" in s or "<" in s or ">" in s or "<=" in s or ">=" in s or "+" in s or "-" in s or "*" in s or "/" in s or "%" in s or "=" in s

def check(s):
    lines = s.split('\n')
    var_list = []
    for line in lines:
        if '=' in line:
            var_list.append(line.split('=')[0].strip())
        temp = line.replace("(", "( ").replace(")", " )").replace(":", "").replace(",", " ")
        if "\"" in temp:
            temp = temp[:temp.index("\"")] + temp[temp.index("\"", temp.index("\"") + 1) + 1:]
        tokens = temp.split()
        for x in tokens:
            bool1 = not is_keyword(x)
            bool2 = not x in var_list
            if bool1 and bool2:
                index = lines.index(line)
                error = f"Syntax Error: {x} is not defined in line {index + 1}\n{line}\n" + (" " * (line.index(x) + 1) + "^")
                raise Exception(error)
    print("Syntax Check Passed")

check(source)