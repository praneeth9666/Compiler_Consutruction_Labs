#!/usr/bin/env python3.10

def is_special_numeric(x):
    if "-" in x:
        return x.replace("-", "").isnumeric()
    return x.isnumeric()


def remove_int_function(code):
    lines = code.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if "int(" in line and "print" not in line:
            if i > 0:
                prev = lines[i - 1]
                prev_tokens = prev.replace("\t","").split(" ")
                tokens = line.replace("int(", "int( ").replace(")", " )").split(" ")
                if prev_tokens[0] == tokens[3] and prev.count("\t") == line.count("\t"):
                    lines[i] = line.replace(")", "").replace("int(" + prev_tokens[0], prev[prev.find("=") + 2:])
                    del lines[i - 1]
                    i -= 1
        i += 1
    return "\n".join(lines)


def split_into_blocks(code):
    lines = code.split('\n')
    blocks = []
    current_block = []
    indentation = "\t"
    layer = 0
    for line in lines:

        if line and layer == line.count(indentation):
            current_block.append(line)
        else:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
                current_block.append(line)
                layer = line.count(indentation)
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks


def constant_folding(code_block):
    vals = {}
    lines = code_block.split('\n')
    for line in lines:
        if not line:
            continue
        tokens = line.replace("(", "( ").replace(
            ")", " )").split(" ")
        if len(tokens) < 2 or "while" in line or "if" in line:
            continue
        for x in range(1, len(tokens)):
            temp = tokens[x].replace(":", "").replace("-", "")
            if temp in vals:
                tokens[x] = tokens[x].replace(temp, vals[temp]).replace("True", "1").replace("False", "0")
        if "=" in tokens[1]:
            if len(tokens) > 3:
                if is_special_numeric(tokens[2]) and is_special_numeric(tokens[4]):
                    vals[tokens[0]] = str(eval(tokens[2] + tokens[3] + tokens[4]))
            else:
                if is_special_numeric(tokens[2]):
                    if tokens[2].count("-") > 1:
                        tokens[2] = tokens[2].replace("-", "")
                    vals[tokens[0].strip()] = tokens[2]
        lines[lines.index(line)] = " ".join(tokens).replace("( ", "(").replace(" )", ")")
    return "\n".join(lines)


def process_code(source):
    source = remove_int_function(source)
    blocks = split_into_blocks(source)
    optimized_blocks = []
    for block in blocks:
        optimized_blocks.append(constant_folding(block))
    return "\n".join(optimized_blocks)


def eliminate_dead_stores(cfg):
    for node in cfg.nodes:
        for i in range(len(node.code) - 1, -1, -1):
            instruction = node.code[i]
            parts = instruction.split()
            opcode = parts[0]
            operands = parts[1:] if len(parts) > 1 else []
            if opcode in ['movl', 'negl', 'addl']:
                destination = operands[-1]
                source=operands[0].replace(',','')
                if destination not in node.liveness[i]:
                    del node.code[i]
                    print(f"Removed dead store: {instruction}")
    return cfg
