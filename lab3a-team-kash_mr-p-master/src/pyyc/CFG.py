#!/usr/bin/env python3.10

class CFG:
    def __init__(self):
        self.root: Node = None
        self.end: Node = None
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def set_root(self, node):
        self.root = node

    def print_cfg(self):
        for node in self.nodes:
            string = node.get_label() + ": ["
            for child in node.get_children():
                string += child.get_label() + ", "
            string = string[:-2] if string.count(",") > 0 else string
            string += "]"

            stringp = " Parent: ["
            for parent in node.get_parent():
                stringp += parent.get_label() + ", "
            stringp = stringp[:-2] if stringp.count(",") > 0 else stringp
            stringp += "]"
            print(string + stringp)

    def get_labels(self):
        string = []
        for node in self.nodes:
            string.append(node.get_label())
        return string

    def get_root(self):
        return self.root

    def get_end(self):
        return self.end

    def set_end(self, node):
        self.end = node


class Node:
    def __init__(self):
        self.children = []
        self.parent = []
        self.code = []
        self.label = ""
        self.liveness = []

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

    def add_child(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children

    def add_parent(self, node):
        self.parent.append(node)

    def get_parent(self):
        return self.parent

    def __str__(self):
        return self.label

    def add_line(self, line):
        self.code.append(line)

    def get_code(self):
        return self.code

    def set_liveness(self, liveness):
        self.liveness = liveness

    def get_liveness(self):
        return self.liveness

# Control flow instructions
cfi = ["jmp", "je", "jz", "jne", "jnz", "js", "jns", "jg", "jnle", "jge", "nl", "jl", "nge", "jle", "jng", "jc", "jnc",
       "jo", "jno", "ja", "jnbe", "jae", "jnb", "jb", "jnae", "jbe", "jna", "loop", "loope", "loopne", "loopz"]


def createExecutionPath(cfg):
    for node in cfg.nodes:
        # Ensure sequential flow if no children
        idx = cfg.nodes.index(node)
        if idx + 1 < len(cfg.nodes) and not node.get_children():
            next_node = cfg.nodes[idx + 1]
            node.add_child(next_node)
            next_node.add_parent(node)

        for line in node.get_code():
            instruction = line.split()[0]
            if instruction in cfi:
                label = line.split()[-1]
                for n in cfg.nodes:
                    if n.get_label() == label:
                        if n not in node.get_children():
                            node.add_child(n)
                        if node not in n.get_parent():
                            n.add_parent(node)
                        break



def createCFG(ir):
    cfg = CFG()
    label_to_node = {}  # Map labels to nodes for easy reference
    current_node = None

    lines = ir.strip().split("\n")
    for line in lines:
        if line.strip() == "":
            continue

        # Start a new node for labels (marks potential jump targets)
        if line.endswith(":"):
            label = line.strip()[:-1]
            if current_node is not None:
                cfg.add_node(current_node)  # Add the current node before starting a new one
            current_node = Node()
            current_node.set_label(label)
            label_to_node[label] = current_node  # Map label to new node
        elif current_node is None:
            # Initialize the first node if not already done
            current_node = Node()
            cfg.set_root(current_node)
            current_node.set_label("entry")

        if current_node:
            current_node.add_line(line)

    # Ensure the last node is added to the CFG
    if current_node is not None:
        cfg.add_node(current_node)
        cfg.set_end(current_node)

    # Now, establish the control flow based on CFIs and labels
    for node in cfg.nodes:
        for line in node.get_code():
            tokens = line.split()
            instruction = tokens[0]
            if instruction in cfi:
                target_label = tokens[-1]
                target_node = label_to_node.get(target_label)
                if target_node:
                    node.add_child(target_node)
                    target_node.add_parent(node)

    # Special handling for sequential flow if no explicit jump is found at the end of a node
    for i in range(len(cfg.nodes) - 1):
        node = cfg.nodes[i]
        next_node = cfg.nodes[i + 1]
        # If a node doesn't end with a jump, link it to the next node
        if not node.get_children():
            node.add_child(next_node)
            next_node.add_parent(node)

    return cfg
'''
def createCFG(ir):
    cfg = CFG()
    lines = ir.strip().split("\n")
    curr = Node()
    cfg.set_root(curr)
    curr.set_label("entry")
    for line in lines:
        if line.strip() == "":
            continue
        if line.strip()[-1] == ":":  # label
            cfg.add_node(curr)
            curr = Node()
            curr.set_label(line.strip()[:-1])
            continue

        curr.add_line(line)
    cfg.add_node(curr)
    cfg.set_end(curr)
    createExecutionPath(cfg)
    return cfg'''
