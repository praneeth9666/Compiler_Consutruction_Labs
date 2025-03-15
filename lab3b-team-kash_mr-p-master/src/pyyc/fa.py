#!/usr/bin/env python3.10
import ast
temp1 = -1

tmp_list = []

def pre_process_temps(source):
    global tmp_list
    code = source.split("\n")
    for x in code:
        index = x.find("temp")
        if index != -1:
            tmp = x[index : x.find(" ", index)]
            if tmp not in tmp_list:
                tmp_list.append(tmp)
                
def check_tmp(tmp):
    global tmp_list
    global temp1
    if tmp in tmp_list:
        temp1 += 1
    
            

def flatten_expr(n):
    global temp1
    global tmp_list

    if isinstance(n, ast.IfExp):
        test, test_code = flatten_expr(n.test)
        body, body_code = flatten_expr(n.body)
        else_body, else_code = flatten_expr(n.orelse)
        if isinstance(n.test, ast.IfExp):
            code = test_code + "if " + test + ":\n\x09"
            code += else_body + " = " + body + "\nelse:\n"
            else_code = "\x09" + else_code.replace("\n", "\n\x09")
            else_code = else_code[0:-1]
            code += else_code
            return else_body, code
        temp1 += 1
        check_tmp("temp" + str(temp1))
        temp = "temp" + str(temp1)
        code = test_code + body_code + else_code
        code += "if " + test + ":\n\x09"
        code += temp + " = " + body + "\n"
        code += "else:\n\x09"
        code += temp + " = " + else_body + "\n\n"
        return temp, code

    if isinstance(n, ast.Constant):
        return str(n.value), ""

    elif isinstance(n, ast.Name):
        return n.id, ""

    elif isinstance(n, ast.BoolOp):
        var, code = zip(*[flatten_expr(x) for x in n.values])
        var = list(var)
        check_tmp("temp" + str(temp1))
        temp = "temp" + str(temp1)
        res = ""
        if isinstance(n.op, ast.Or): #and len(var) == 2:
            for x in range(len(var) - 1):
                temp1 += 1
                check_tmp("temp" + str(temp1))
                temp = "temp" + str(temp1)
                res += ("if " + var[x] + ":\n\x09" + temp + " = " + var[x]
                    + "\nelse\n\x09" + temp + " = " + var[x + 1] + "\n")
                var[x + 1] = temp
            return temp, "".join(x for x in code) + res
        if isinstance(n.op, ast.And):
            for x in range(len(var) - 1):
                temp1 += 1
                check_tmp("temp" + str(temp1))
                temp = "temp" + str(temp1)
                res += ("if " + var[x] + "\n\x09" + temp + " = " + var[x + 1]
                    + "\nelse\n\x09" + temp + " = " + var[x] + "\n")
                var[x + 1] = temp
            return temp, "".join(x for x in code) + res
        return temp, "".join(x for x in code)

    elif isinstance(n, ast.Compare):
        left, left_code = flatten_expr(n.left)
        comps, comparators = zip(*[flatten_expr(x) for x in n.comparators])
        ops = [flattenAST(op) for op in n.ops]
        temp1 += 1
        check_tmp("temp" + str(temp1))
        temp = "temp" + str(temp1)
        string = temp + " = " + str(left)
        for x in range(len(ops)):
            string = string + " " + str(ops[x]) + " " + str(comps[x])
        return temp, left_code + "".join([x for x in comparators]) + string + "\n"

    elif isinstance(n, ast.BinOp):
        left, left_code = flatten_expr(n.left)
        right, right_code = flatten_expr(n.right)
        temp1 += 1
        check_tmp("temp" + str(temp1))
        temp = "temp" + str(temp1)
        op = flattenAST(n.op)
        code = "" + left_code + right_code + temp + " = " + left + " " + op + " " + right + "\n"
        return temp, code

    elif isinstance(n, ast.UnaryOp):
        operand, operand_code = flatten_expr(n.operand)
        temp1 += 1
        check_tmp("temp" + str(temp1))
        temp = "temp" + str(temp1)
        op = flattenAST(n.op)
        if isinstance(n.op, ast.Not):
            code = operand_code + "if " + operand +":\n\x09" + temp + " = 0\nelse\n\x09" + temp + " = 1\n"
            return temp,code
        code = operand_code + temp + " = " + operand + "\n" + temp + " = " + op + temp + "\n"
        return temp, code

    elif isinstance(n, ast.Call):
        if (isinstance(n.func, ast.Name) and n.func.id == "eval" and
                len(n.args) == 1 and isinstance(n.args[0], ast.Call) and
                isinstance(n.args[0].func, ast.Name) and n.args[0].func.id == "input"):
            temp1 += 1
            check_tmp("temp" + str(temp1))
            temp = "temp" + str(temp1)
            code = temp + " = eval(input())\n"
            return temp, code

        args_code = ""
        args_flat = []
        for arg in n.args:
            flat_arg, arg_code = flatten_expr(arg)
            args_code += arg_code
            args_flat.append(flat_arg)
        args_str = ", ".join(args_flat)

        if isinstance(n.func, ast.Name) and n.func.id == "print":
            return "print(" + args_str + ")", args_code
        else:
            temp1 += 1
            check_tmp("temp" + str(temp1))
            temp = "temp" + str(temp1)
            code = args_code + temp + " = " + flattenAST(n.func) + "(" + args_str + ")\n"
            return temp, code
    else:
        raise Exception('Error in unparse: unrecognized AST node: ' + str(n))


def flattenAST(n):
    global temp1
    global tmp_list
    if isinstance(n, ast.Module):
        return "".join([flattenAST(x) for x in n.body])

    elif isinstance(n, ast.Assign):
        rhs, rhs_code = flatten_expr(n.value)
        targets = ""
        for x in n.targets:
            targets += flattenAST(x) + ", "
        targets = targets[0:-2]
        return "" + rhs_code + targets + " = " + rhs + "\n"

    elif isinstance(n, ast.Expr):
        expr, expr_code = flatten_expr(n.value)
        return "" + expr_code + expr + "\n"

    elif isinstance(n, ast.If) or isinstance(n, ast.While):
        test, test_code = flatten_expr(n.test)
        body_code = "".join([flattenAST(x) for x in n.body])
        else_code = "".join([flattenAST(x) for x in n.orelse]) if n.orelse else ''
        body_code = "\x09" + body_code.replace("\n", "\n\x09")
        body_code = body_code[0:-1]
        if len(else_code) != 0:
            else_code = "\x09" + else_code.replace("\n", "\n\x09")
            else_code = else_code[0:-1]

        if isinstance(n, ast.While):
            return test_code + str(type(n).__name__).lower() + " " + test + ":\n" + body_code + (
            ("else:\n" + else_code) if len(else_code) != 0 else "") + "\x09" + test_code.replace("\n", "\n\x09")[0:-1]

        return test_code + str(type(n).__name__).lower() + " " + test + ":\n" + body_code + (
            ("else:\n" + else_code) if len(else_code) != 0 else "")

    elif isinstance(n, ast.Add):
        return "+"

    elif isinstance(n, ast.USub):
        return "-"

    elif isinstance(n, ast.Name):
        return n.id

    elif isinstance(n, ast.Eq):
        return "=="

    elif isinstance(n, ast.NotEq):
        return "!="

    elif isinstance(n, ast.Not):
        return "not"

    elif isinstance(n, ast.And):
        return "and"

    elif isinstance(n, ast.Or):
        return "or"

    elif isinstance(n, ast.Lt):
        return "<"

    elif isinstance(n, ast.LtE):
        return "<="

    elif isinstance(n, ast.Gt):
        return ">"

    elif isinstance(n, ast.GtE):
        return ">="

    elif isinstance(n, ast.Break):
        return "break\n"

    elif isinstance(n, ast.Continue):
        return "continue\n"

    else:
        raise Exception('Error in flattenAST: unrecognized AST node: ' + str(n))


def contains_op(line):
    ops = ["+"]
    splits = line.split(" ")
    for x in splits:
        if x in ops:
            return True
    return False

def post_process_optimizations(code):
    lines = code.split("\n")
    code = list()
    x = 0
    while x < len(lines) - 1:
        line = lines[x]
        next_line = lines[x + 1]
        if next_line.find("=") != -1:
            if not contains_op(next_line):
                if contains_op(line):
                    splits = line.split(" ")
                    next_splits = next_line.split(" ")
                    if splits[0] in next_line and next_splits[0] not in splits:
                        next_line = next_line.replace(splits[0], line[line.find("=") + 2:])
                        code.append(next_line)
                        x += 2
                        continue
        code.append(line)
        x += 1
    return "\n".join(code)







