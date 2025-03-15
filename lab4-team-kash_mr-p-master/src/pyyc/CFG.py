#!/usr/bin/env python3.10

class CFG:
    def __init__(self):
        self.root: Node = None
        self.end: Node = None
        self.nodes = []
        self.live_map = {}

    def set_live_map(self, live_map):
        self.live_map = live_map

    def get_live_map(self):
        return self.live_map

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

    def clear_liveness(self):
        for node in self.nodes:
            node.set_liveness([])
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
    def to_x86IR(self):
        ir_lines = []
        for node in self.nodes:
            if node.code:  
                ir_lines.extend(node.code)
        return '\n'.join(ir_lines)

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

    def set_code(self, code):
        self.code = code

    def set_liveness(self, liveness):
        self.liveness = liveness

    def get_liveness(self):
        return self.liveness

# Control flow instructions
cfi = ["jmp", "je", "jz", "jne", "jnz", "js", "jns", "jg", "jnle", "jge", "nl", "jl", "nge", "jle", "jng", "jc", "jnc",
       "jo", "jno", "ja", "jnbe", "jae", "jnb", "jb", "jnae", "jbe", "jna", "loop", "loope", "loopne", "loopz"]


def createCFG(ir):
    cfg = CFG()
    label_to_node = {}
    current_node = None

    lines = ir.strip().split("\n")
    for line in lines:
        if line.strip() == "":
            continue

        if line.endswith(":"):
            label = line.strip()[:-1]
            if current_node is not None:
                cfg.add_node(current_node)
            current_node = Node()
            current_node.set_label(label)
            label_to_node[label] = current_node
        elif current_node is None:
            current_node = Node()
            cfg.set_root(current_node)
            current_node.set_label("entry")

        if current_node:
            current_node.add_line(line)

    if current_node is not None:
        cfg.add_node(current_node)
        cfg.set_end(current_node)

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

    for i in range(len(cfg.nodes) - 1):
        node = cfg.nodes[i]
        next_node = cfg.nodes[i + 1]
        if not node.get_children() or "if" not in next_node.get_label() and "else" not in next_node.get_label():
            node.add_child(next_node)
            next_node.add_parent(node)

    return cfg