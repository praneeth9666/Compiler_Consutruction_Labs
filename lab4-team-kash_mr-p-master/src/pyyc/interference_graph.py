#!/usr/bin/env python3.10

colors = {   0 : "eax", 
             1 : "ecx", 
             2 : "edx", 
             3 : "edi", 
             4 : "ebx", 
             5 : "esi"}

fun_registers = ["eax", "ecx", "edx"]

    

def color_graph(graph):
    color_assignment = {node: None for node in graph}
    stack_counter = max(colors.keys()) + 1

    for reg in fun_registers:
        reg_color = [color for color, reg_name in colors.items() if reg_name == reg]
        if reg_color:
            color_assignment[reg] = reg_color[0]

    for node in graph:
        if node in fun_registers:
            continue

        available_colors = set(colors.keys()) - set(fun_registers)
        for neighbor in graph[node]:
            if color_assignment[neighbor] in available_colors:
                available_colors.remove(color_assignment[neighbor])

        if available_colors:
            color_assignment[node] = min(available_colors)
        else:
            color_assignment[node] = stack_counter
            colors[color_assignment[node]] = str((stack_counter - 5) * -4) + "(%ebp)"
            stack_counter += 1
    
    return color_assignment

arith_instruct = ["addl", "negl"]

def gen_interference_graph(IR, live_list, var_lst): #Definitely working
    graph = {}
    for x in live_list:
        for y in x:
            if y not in graph.keys():
                graph[y] = set()
    for x in fun_registers:
        graph[x] = set()
    lines = IR.split("\n")
    for x in range(len(lines)):
        line = lines[x]
        instruction = line[:line.find(" ")]
        if instruction == "movl":
            source = line[line.find(" ") + 1 : line.find(",")]
            destination = line[line.find(",") + 2:]
            for t1 in live_list[x:]:
                for t2 in t1:
                    if t2 != source and t2 != destination and destination in graph:
                        graph[destination].add(t2)
        if instruction in arith_instruct:
            desintation = None
            if line.find(",") == -1:
                destination = line[line.find(" ") + 1 :]
            else:
                destination = line[line.find(",") + 2 :]
            for t1 in live_list[x:]:
                for t2 in t1:
                    if t2 != destination:
                        graph[destination].add(t2)
        if instruction == "call": #For connecting caller saved registers to live variables
            for t1 in live_list[x]:
                for reg in fun_registers:
                    graph[reg].add(t1)
                    graph[t1].add(reg)
    return graph
    

def color_to_reg(color_assignment):
    for x in color_assignment:
        color_assignment[x] = colors[color_assignment[x]]
    return color_assignment



def build_interference_graph(cfg,var_lst):
    interference_graph = {}
    for var in var_lst:
        #var= var.replace(" =","")
        if("%" not in var and "error" not in var):
            interference_graph.setdefault(var,set())
    callee_saved_regs = {'eax', 'ecx', 'edx'}

    def add_interference(var1, var2):
        if "%" not in var1 and "%" not in var2 and "error" not in var1 and "error" not in var2:
            print(var1,var2)
            if var1 not in interference_graph:
                interference_graph[var1] = set()
            if var2 not in interference_graph:
                interference_graph[var2] = set()
            interference_graph[var1].add(var2)
            interference_graph[var2].add(var1)

    def interfere_with_callee_saved(live_vars):
        for live_var in live_vars:
            for reg in callee_saved_regs:
                add_interference(live_var, reg)
    def add_move_arith_interference(inst, live_vars):
        parts = inst.split()
        cmd = parts[0]

        if len(parts) >= 3:
            
            if cmd == 'movl':
                _, src, tgt = parts
                for v in live_vars:
                    if v != src and v != tgt and "%" not in tgt:
                        add_interference(tgt, v)
            elif cmd == "negl":
                _, tgt = parts
                for v in live_vars:
                    if v != tgt:
                        add_interference(tgt, v)            
            else:
                _, src, tgt = parts
                for v in live_vars:
                    if v != tgt:
                        add_interference(tgt, v)
    for node in cfg.nodes:
        all_live_vars = set.union(*node.get_liveness()) if node.get_liveness() else set()
        call_in_node = any(line.startswith('call') for line in node.code)
        cmp_in_node = any(line.startswith('cmp') for line in node.code)
        if cmp_in_node:
            for live_var in all_live_vars:
                if live_var != 'eax':
                    #print(f"live_var with eax:{live_var}")
                    add_interference('eax', live_var) 
        if call_in_node:
            interfere_with_callee_saved(all_live_vars)
        for line in node.code:
            if line.startswith('movl') or any(arith_cmd in line for arith_cmd in ['addl', 'negl']):
                add_move_arith_interference(line, all_live_vars)   
        for live_var in all_live_vars:
            for other_live_var in all_live_vars:
                if live_var != other_live_var:
                    add_interference(live_var, other_live_var)
    #print(interference_graph)
    return interference_graph
  


def get_reg_replacements(cfg,var_lst):
    replacements = color_to_reg(color_graph(build_interference_graph(cfg,var_lst)))
    for x in replacements.copy():
        if x in colors.values() or x == "":
            replacements.pop(x)
    return [replacements, len(colors) - 6]    


    
            
                
                
                
            
            
