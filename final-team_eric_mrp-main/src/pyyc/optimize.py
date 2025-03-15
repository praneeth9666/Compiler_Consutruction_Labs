#!/usr/bin/env python3.10
import sourceCFG as sCFG

def is_special_numeric(x):
    if "-" in x:
        return x.replace("-", "").isnumeric()
    return x.isnumeric()


def remove_int_function(code):
    lines = code.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if " int(" in line and "print" not in line:
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


def contains_special_char(line):
    ops = ["+", "!=", "==", ">", "<", ">=", "<=", "-", "(", ")", "[", "]", "{", "}", ":", ",", "."]
    splits = line.split(" ")
    for x in splits:
        for y in ops:
            if y in x:
                return True
    return False

def process_code_block(code, prev_lives, live_map, code_len):
    lives = []
    reserved = ["if", "while", "return", "else", "(", ")", "[", "]", "{", "}", ":", ","]
    currset = prev_lives
    for x in range(len(code) - 1, -1, -1):
        if not code[x]:
            continue
        r = set()
        w = set()
        lives.insert(0, currset)
        line = code[x].replace("(", "( ").replace(")", " )").replace("[", " [ ").replace("]", " ] ").replace("}", " }").replace(",", "").strip()
        live_map[code_len - len(live_map)] = currset
        token = line.split(" ")

        if " = " in line:
            for y in range(2, len(token)):
                if not contains_special_char(token[y]) and not is_special_numeric(token[y]) and token[y] not in reserved and token[y]:
                    r.add(token[y])
            w.add(token[0])
        else:
            for y in range(0, len(token)):
                t = token[y]
                if not contains_special_char(t) and not t.isnumeric() and t not in reserved:
                    r.add(t)

        currset = (currset - w) | r
    lives.insert(0, currset)
    return lives

def constant_folding(code_block):
    vals = {}
    lines = code_block
    for line in lines:
        if not line:
            continue
        tokens = line.replace("(", "( ").replace(")", " )").replace("[", " [ ").replace("]", " ] ").replace("}", " }").replace(",", " ,").split(" ")
        if len(tokens) < 2 or "while" in line or "if" in line or "else" in line:
            continue
        for x in range(1, len(tokens)):
            temp = tokens[x].replace(":", "").replace("-", "")
            if temp in vals:
                tokens[x] = tokens[x].replace(temp, vals[temp]).replace("True", "1").replace("False", "0")
        if "=" in tokens[1]:
            if len(tokens) > 3:
                all_nums = True
                for x in range(2, len(tokens), 2):
                    if not is_special_numeric(tokens[x]):
                        all_nums = False
                if all_nums:
                    vals[tokens[0]] = str(eval(" ".join(tokens[2:])))
            else:
                if is_special_numeric(tokens[2]):
                    if tokens[2].count("-") > 1:
                        tokens[2] = tokens[2].replace("-", "")
                    vals[tokens[0].strip()] = tokens[2]
        lines[lines.index(line)] = " ".join(tokens).replace("( ", "(").replace(" )", ")")
    return lines


def process_code(source):
    source = remove_int_function(source)
    blocks = sCFG.generate_CFG(source)
    for block in blocks.get_nodes():
        block.set_code(constant_folding(block.get_code()))
    stack = [blocks.end]
    while stack:
        live = set()
        for x in stack[0].get_children():
            if x.get_liveness():
                live = x.get_liveness()[0] | live
            else:
                live = set() | live
        for x in stack[0].get_parents():
            if x not in stack:
                stack.insert(1, x)
        stack[0].set_liveness(process_code_block(stack[0].get_code(), live, {}, len(stack[0].get_code())))
        if stack[0].get_code() and "while" in stack[0].get_code()[-1]:
            child = stack[0].get_children()[0]
            for x in range(3):
                child.set_liveness(process_code_block(child.get_code(), stack[0].get_liveness()[-1], {}, len(child.get_code())))
                live = child.get_liveness()[0] | live
                stack[0].set_liveness(process_code_block(stack[0].get_code(), live, {}, len(stack[0].get_code())))
        stack.pop(0)
    return eliminate_dead_stores_flat(blocks.get_combined_code(), blocks.get_combined_lives())

def eliminate_dead_stores_flat(code, lives):
    live = []
    for x in lives:
        live.extend(x)
    lines = "\n".join(code)
    lines = lines.split("\n")
    t = []
    for x in lines:
        if x:
            t.append(x)
    lines = t
    res = []
    for x in lines:
        if " = " in x:
            index = lines.index(x)
            tokens = x.strip().split(" ")
            if tokens[0] in live[index]:
                res.append(x)
        else:
            res.append(x)
    return "\n".join(res)




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
