#!/usr/bin/env python3.10


def process_code_block(code, prev_lives, live_map, ir_len):
    rinst = ["addl", "negl", "movl", "movzbl", "pushl", "cmpl", "cmp"]  # Instructions that read and write
    winst = ["movl", "addl", "negl", "movzbl", "pushl"]  # Instructions that only write
    lives = [set()]
    currset = prev_lives
    for x in range(len(code) - 1, -1, -1):
        r = set()
        w = set()
        lives.insert(0, currset)
        line = code[x].strip()
        live_map[ir_len - len(live_map)] = currset
        token = line.split(" ")

        # Check if the line is empty or does not have enough parts for processing
        if not line or len(token) < 2:
            continue
        if "jmp" in line:
            if "mov" in code[x - 1]:
                tokens = code[x - 1].split(" ")
                currset.add(tokens[-1])
            continue

        instruction = token[0]
        operand1 = token[1] if len(token) > 1 else None
        operand2 = token[2] if len(token) > 2 else None
        
        if operand1.count(",") > 0:
            operand1 = operand1[:-1]
        operand2 = None
        if len(token) > 2:
            operand2 = token[2]
        if instruction in rinst and not operand1.startswith("$") and not operand1.startswith("%"):
            r.add(operand1)
        if instruction in ["cmpl", "cmp"] and operand2 is not None and not operand2.startswith("$"):
            r.add(operand2)
        if instruction in winst:
            if operand2 is not None and not operand2.startswith("$") and not operand2.startswith("%"):
                if instruction in ["addl"]:
                    w.add(operand2)
                    r.add(operand2)
                else:
                    w.add(operand2)
            elif not operand1.startswith("$"):
                w.add(operand1)
                r.add(operand1)
        currset = (currset - w) | r
    return lives, live_map


def gen_lives_list(cfg):
    labels = cfg.nodes
    labels.reverse()
    live_map = {}
    ir_len = cfg.to_x86IR().count("\n")
    next = None
    loops = 0
    prev = None
    label_count = 0
    while label_count < len(labels):
        x = labels[label_count]
        currset = set()
        if prev is not None:
            if loops > 2:
                label_count = next
                prev = None
                continue
            currset = prev
            loops +=1
        else:
            currset = set()
            for y in x.get_children():
                if len(y.get_liveness()) > 0:
                    currset = currset | y.get_liveness()[0]
        res = process_code_block(x.get_code(), currset, live_map, ir_len)
        x.set_liveness(res[0])
        if "while_start" in x.get_label():
            while_num = x.get_label().split("_")[-1]
            next = label_count + 1
            for y in labels:
                if y.get_label() == "while_end_" + while_num:
                    label_count = labels.index(y)
                    break
            prev = x.get_liveness()[0]
        label_count += 1
    cfg.set_live_map(live_map)
    labels.reverse()
    ir = cfg.to_x86IR()
    ir = ir.split("\n")
    line = -1
    for x in cfg.nodes:
        live = x.get_liveness()
        for y in live:
            if line == -1 or line >= len(ir) - 1:
                print(" | " + str(y))
            else:
                print(ir[line] + " | " + str(y))
            line += 1




