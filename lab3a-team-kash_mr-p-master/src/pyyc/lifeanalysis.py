#!/usr/bin/env python3.10

def process_code_block(code, labels, prev_lives):
    rinst = ["addl", "negl", "movl", "movzbl", "pushl", "cmpl"]  # Instructions that read and write
    winst = ["movl", "addl", "negl", "movzbl", "pushl"]  # Instructions that only write
    lives = [set()]
    currset = prev_lives
    for x in range(len(code) - 1, -1, -1):
        r = set()
        w = set()
        lives.insert(0, currset)
        line = code[x].strip()
        token = line.split(" ")

        # Check if the line is empty or does not have enough parts for processing
        if not line or len(token) < 2:
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
        if instruction in ["cmpl"] and operand2 is not None and not operand2.startswith("$"):
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
    return lives


def gen_lives_list(cfg):
    visited = set()  # Keep track of visited nodes
    queue = [cfg.get_end()]  # Start with the end node
    if cfg.get_end() is None:
        print("Error: CFG end node is not set.")
        return
    while queue:
        curr = queue.pop(0)
        if curr in visited:  # Skip nodes that have already been visited
            continue
        visited.add(curr)  # Mark the current node as visited

        # Calculate the initial set of live variables based on children's liveness
        currset = set()
        for child in curr.get_children():
            if child.get_liveness():
                # Assuming the first set in the list is the relevant one for this context
                currset = currset.union(child.get_liveness()[0])

        # Process the current node's code block and update its liveness
        if curr.get_code() is not None:
            curr.set_liveness(process_code_block(curr.get_code(), cfg.get_labels(), currset))

        # Add parent nodes to the queue for processing, ensuring they are not already visited
        for parent in curr.get_parent():
            if parent not in visited:
                queue.append(parent)

