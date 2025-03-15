class sNode:
    def __init__(self):
        self.parents = []
        self.children = []
        self.code = None
        self.liveness = None
        self.layer = 0

    def set_layer(self, layer):
        self.layer = layer

    def get_layer(self):
        return self.layer

    def add_parent(self, node):
        self.parents.append(node)

    def add_child(self, node):
        self.children.append(node)

    def set_liveness(self, liveness):
        self.liveness = liveness

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def get_liveness(self):
        return self.liveness

    def get_parents(self):
        return self.parents

    def get_children(self):
        return self.children

class sCFG:

    def __init__(self):
        self.nodes = []
        self.start = None
        self.end = None

    def get_combined_lives(self):
        lives = []
        for x in self.nodes:
            if x.get_liveness():
                x.get_liveness().pop(0)
                lives.append(x.get_liveness())
        return lives

    def get_combined_code(self):
        code = []
        for x in self.nodes:
            for y in x.get_code():
                code.append(y)
        return code


    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def set_start_and_end(self):
        self.start = self.nodes[0]
        self.end = self.nodes[-1]

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


def link_nodes(cfg: sCFG):
    nodes = cfg.get_nodes()
    jumps = []
    for x in range(len(nodes)):
        code = nodes[x].get_code()
        if code:
            if "if" in code[-1] or "while" in code[-1]:
                jumps.append(1)
                continue
            if jumps:
                if jumps[-1] == 1:  # body
                    nodes[x - 1].add_child(nodes[x])
                    nodes[x].add_parent(nodes[x - 1])
                    jumps[-1] += 1
                    continue
                if jumps[-1] == 2:
                    nodes[x - 2].add_child(nodes[x])
                    nodes[x].add_parent(nodes[x - 2])
                    if x + 1 < len(nodes) and "else" in code[0]:
                        nodes[x].add_child(nodes[x + 1])
                        nodes[x + 1].add_parent(nodes[x])
                        nodes[x - 1].add_child(nodes[x + 1])
                        nodes[x + 1].add_parent(nodes[x - 1])
                    elif "else" not in code[0]:
                        nodes[x].add_parent(nodes[x - 1])
                        nodes[x - 1].add_child(nodes[x])
                    jumps.pop()

def generate_CFG(code):
    lines = code.split('\n')
    blocks = []
    indentation = ""
    current_block = []
    curr_node = sNode()
    layer = 0
    for line in lines:
        if not line:
            continue
        if line[0] == " " and not indentation:
            for x in line:
                if x == " " or x == "\t":
                    indentation += x
                else:
                    break
        if "if" in line or "while" in line:
            current_block.append(line)
            blocks.append(curr_node)
            blocks[-1].set_code(current_block)
            blocks[-1].set_layer(layer)
            current_block = []
            curr_node = sNode()
            layer = layer + 1
            continue
        if "else" in line:
            blocks.append(curr_node)
            blocks[-1].set_code(current_block)
            blocks[-1].set_layer(layer)
            current_block = []
            curr_node = sNode()
            current_block.append(line)
            continue
        if indentation:
            if layer != line.count(indentation):
                blocks.append(curr_node)
                blocks[-1].set_code(current_block)
                blocks[-1].set_layer(layer)
                layer = line.count(indentation)
                current_block = []
                curr_node = sNode()
        current_block.append(line)
    blocks.append(curr_node)
    blocks[-1].set_code(current_block)
    blocks[-1].set_layer(layer)
    cfg = sCFG()
    for x in blocks:
        cfg.add_node(x)
    link_nodes(cfg)
    cfg.set_start_and_end()
    return cfg