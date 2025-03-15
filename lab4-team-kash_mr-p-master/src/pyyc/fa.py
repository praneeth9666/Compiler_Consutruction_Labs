#!/usr/bin/env python3.10
import ast
import explicate

temp1 = -1

tmp_list = []


def pre_process_temps(source):
    global tmp_list
    code = source.split("\n")
    for x in code:
        index = x.find("temp")
        if index != -1:
            tmp = x[index: x.find(" ", index)]
            if tmp not in tmp_list:
                tmp_list.append(tmp)


def check_tmp(tmp):
    global tmp_list
    global temp1
    if tmp in tmp_list:
        temp1 += 1


def get_new_temp():
    global temp1
    temp1 += 1
    check_tmp("temp" + str(temp1))
    return "temp" + str(temp1)


def isTypeCheckFunction(n):
    return (isinstance(n, explicate.CheckIntTag) or isinstance(n, explicate.CheckBigTag) or isinstance(n,
                                                                                                       explicate.CheckBoolTag)
            or isinstance(n, explicate.InjectBool) or isinstance(n, explicate.InjectInt) or isinstance(n,
                                                                                                       explicate.InjectBig)
            or isinstance(n, explicate.UnboxBool) or isinstance(n, explicate.UnboxInt) or isinstance(n,
                                                                                                     explicate.UnboxBig)
            or isinstance(n, explicate.BigAdd) or isinstance(n, explicate.CallError))


def flatten_expr(n, var=None):
    global temp1
    global tmp_list

    if isinstance(n, ast.IfExp):
        if isinstance(n.test, ast.BoolOp):
            # Type checking code VVVVVVVVV
            if isTypeCheckFunction(n.test.values[0]):
                if not var:
                    var = get_new_temp()
                test, test_code = flatten_expr(n.test)
                test_operands = test.split(" ")
                temp2 = get_new_temp()
                code = test_code + "\n" + temp2 + " = " + test_operands[0] + "\n"
                body, body_code = flatten_expr(n.body, var)
                else_body, else_code = flatten_expr(n.orelse, var)
                code += "if " + temp2 + ":\n\x09"
                body = "\n" + body
                code += body.replace("\n", "\n\x09\x09") + "\nelse:\n"
                code += "\x09" + else_code.replace("\n", "\n\x09") + "\n"
                return var, code
        test, test_code = flatten_expr(n.test)
        body, body_code = flatten_expr(n.body)
        else_body, else_code = flatten_expr(n.orelse)
        if isinstance(n.test, ast.IfExp):
            temp3 = get_new_temp()
            test_code += ((temp3 + " = is_true(" + test + ")\n") if "is_" not in test else "")
            code = test_code + "if " + (temp3 if "is_" not in test else test) + ":\n\x09"
            code += else_body + " = " + body + "\nelse:\n"
            else_code = "\x09" + else_code.replace("\n", "\n\x09")
            else_code = else_code[0:-1]
            code += else_code
            return else_body, code
        temp = get_new_temp()
        temp3 = get_new_temp()
        else_code += ((temp3 + " = is_true(" + test + ")\n") if "is_" not in test else "")
        code = test_code + body_code + else_code
        code += "if " + (temp3 if "is_" not in test else test) + ":\n\x09"
        code += temp + " = " + body + "\n"
        code += "else:\n\x09"
        code += temp + " = " + else_body.replace("\n", "\n\x09").replace("temp_replace_me", temp)[0:-1]
        return temp, code

    if isinstance(n, ast.Constant):
        return str(n.value), ""

    elif isinstance(n, explicate.Let):
        var = n.var.id
        if isinstance(n.value, ast.List):
            value, value_code = flatten_expr(n.value, var)
            value_code = value_code + flatten_expr(n.var)[1] + var + " = " + value
            body, body_code = flatten_expr(n.body)
            code = value_code + body_code + "\n"
            value = get_new_temp()
            var_name = flatten_expr(n.var)[0]
            if code.find(var_name) != -1:
                code = code.replace(var_name, value)
        else:
            value, value_code = flatten_expr(n.value)
            value = value.replace("temp_replace_me", var)
            body, body_code = flatten_expr(n.body)
            code = value_code + body_code + "\n"
            if "inject" in value:
                # index = code.find(var) - 18
                # if index < 0:
                #    index = 0
                # preamble = index + code[index:].find("\n")
                # if preamble != -1:
                temp = get_new_temp()
                # temp4 = code[0: preamble + 1]
                # temp2 = code[preamble + 1:]
                code = temp + " = " + value + "\n" + code
                code = code.replace(var, temp)
            else:
                code = code.replace(var, value)
        return body, code

    elif isinstance(n, ast.List):
        if not var:
            var = "temp_replace_me"
        length = len(n.elts)
        temp = get_new_temp()
        preamble = temp + " = " + "inject_int(" + str(length) + ")\n"
        code = "create_list(" + temp + ")\n" + var + " = " + "inject_big(" + var + ")\n"
        tmp = 0
        for x in n.elts:
            temp = get_new_temp()
            temp3 = flatten_expr(x, temp)
            preamble += temp3[1]
            code += temp + " = " + temp3[0] + "\n"
            temp2 = get_new_temp()
            code += temp2 + " = " + "inject_int(" + str(tmp) + ")" + "\n"
            code += "set_subscript(" + var + "," + temp2 + "," + temp + ")\n"
            tmp += 1
        return code, preamble

    elif isinstance(n, explicate.InjectInt):
        if isinstance(n.value, ast.BinOp) or isTypeCheckFunction(n.value):
            ret = flatten_expr(n.value)
            return ret[1] + var + " = " + "inject_int(" + str(ret[0]) + ")", ""
        return "inject_int(" + str(n.value) + ")", ""

    elif isinstance(n, explicate.InjectBig):
        if isinstance(n.value, ast.BinOp) or isTypeCheckFunction(n.value):
            ret = flatten_expr(n.value)
            temp = get_new_temp()
            return ret[1] + temp + " = " + str(ret[0]) + "\n" + var + " = " + "inject_big(" + temp + ")", ""
        return "inject_big(" + str(n.value) + ")", ""

    elif isinstance(n, explicate.InjectBool):
        if isinstance(n.value, ast.BinOp) or isTypeCheckFunction(n.value) or isinstance(n.value, ast.Compare):
            ret = flatten_expr(n.value)
            return ret[1] + var + " = " + "inject_bool(" + str(ret[0]) + ")", ""
        return "inject_bool(" + str(n.value) + ")", ""

    elif isinstance(n, explicate.CheckIntTag):
        return "is_int(" + str(flatten_expr(n.value)[0]) + ")", ""

    elif isinstance(n, explicate.CheckBigTag):
        return "is_big(" + str(flatten_expr(n.value)[0]) + ")", ""

    elif isinstance(n, explicate.CheckBoolTag):
        return "is_bool(" + str(flatten_expr(n.value)[0]) + ")", ""

    elif isinstance(n, explicate.UnboxInt):
        return "project_int(" + str(flatten_expr(n.value)[0]) + ")", ""

    elif isinstance(n, explicate.UnboxBig):
        return "project_big(" + str(flatten_expr(n.value)[0]) + ")", ""

    elif isinstance(n, explicate.UnboxBool):
        return "project_bool(" + str(flatten_expr(n.value)[0]) + ")", ""

    elif isinstance(n, ast.Dict):
        if not var:
            var = "temp_replace_me"
        code = "create_dict()\n" + var + " = " + "inject_big(" + var + ")\n"
        for x, y in zip(n.keys, n.values):
            temp = get_new_temp()
            code += temp + " = " + flatten_expr(x)[0] + "\n"
            temp2 = get_new_temp()
            code += temp2 + " = " + flatten_expr(y)[0] + "\n"
            code += "set_subscript(" + var + ", " + temp + ", " + temp2 + ")\n"
        return code, ""

    elif isinstance(n, ast.Subscript):
        var1, var_code = flatten_expr(n.value)
        index, index_code = flatten_expr(n.slice)
        preamble = ""
        if isinstance(n.value, ast.Call) or isTypeCheckFunction(n.value):
            temp = get_new_temp()
            preamble += temp + " = " + var + "\n"
            var1 = temp
        if isinstance(n.slice, ast.Call) or isTypeCheckFunction(n.slice):
            temp = get_new_temp()
            preamble += temp + " = " + index + "\n"
            index = temp
        if isinstance(n.ctx, ast.Load):
            temp2 = get_new_temp()
            return temp2, preamble + var_code + index_code + temp2 + " = " + "get_subscript(" + var1 + ", " + index + ")\n"
        if isinstance(n.ctx, ast.Store):
            return "set_subscript(" + var1 + ", " + index + ", ", preamble + var_code + index_code

    elif isinstance(n, explicate.BigAdd):
        left = None
        right = None
        preamble = ""
        if isinstance(n.left, ast.expr) or isTypeCheckFunction(n.left):
            left = flatten_expr(n.left)[0]
            temp2 = get_new_temp()
            preamble += temp2 + " = " + left + "\n"
            left = temp2
        if isinstance(n.right, ast.Expr) or isTypeCheckFunction(n.right):
            temp3 = get_new_temp()
            right = flatten_expr(n.right)[0]
            preamble += temp3 + " = " + right + "\n"
            right = temp3
        return "add(" + str(left) + ", " + str(right) + ")", preamble

    elif isinstance(n, explicate.CallError):
        error_msg = "Type Checking Error"
        return "", "error_pyobj(\"" + error_msg + "\")"


    elif isinstance(n, ast.Name):
        return n.id, ""


    elif isinstance(n, ast.BoolOp):
        var1, code = zip(*[flatten_expr(x) for x in n.values])
        var1 = list(var1)
        check_tmp("temp" + str(temp1))
        temp = "temp" + str(temp1)
        res = ""
        if isinstance(n.op, ast.Or):  # and len(var) == 2:
            for x in range(len(var1) - 1):
                temp = get_new_temp()
                res += ("if " + var1[x] + ":\n\x09" + temp + " = " + var1[x]
                        + "\nelse\n\x09" + temp + " = " + var1[x + 1] + "\n")
                var1[x + 1] = temp
            return temp, "".join(x for x in code) + res
        if isinstance(n.op, ast.And):  # and not isTypeCheckFunction(n.values[0]):

            for x in range(len(var1) - 1):
                temp = get_new_temp()
                temp2 = get_new_temp()
                if isinstance(n.values[x], ast.List) or isinstance(n.values[x], ast.Dict):
                    temp3 = get_new_temp()
                    string = (temp2 + " = " + var1[
                        x] + (("\n" + temp3 + " = is_true(" + temp2 + ")") if "is_" not in var1[x] else "") + "\nif " + (temp3 if "is_" not in var1[x] else temp2) + "\n\x09" + temp + " = " + var1[
                                  x + 1]
                              + "\nelse\n\x09" + temp + " = " + temp2 + "\n")
                    string = string.replace("temp_replace_me", temp2)
                    res += string
                else:
                    temp3 = get_new_temp()
                    res += (temp2 + " = " + var1[
                        x] + (("\n" + temp3 + " = is_true(" + temp2 + ")") if "is_" not in var1[x] else "") + "\nif " + (temp3 if "is_" not in var1[x] else temp2) + "\n\x09" + temp + " = " + var1[
                                x + 1]
                            + "\nelse\n\x09" + temp + " = " + var1[x] + "\n")
                var1[x + 1] = temp
            return temp, "".join(x for x in code) + res
        # elif isTypeCheckFunction(n.values[0]):
        #    test = "".join(x + " " + flattenAST(n.op) + " " for x in var)
        #    test = test[0:-5]
        #    return test, "".join(x for x in code)
        return temp, "".join(x for x in code)

    elif isinstance(n, ast.Compare):
        left, left_code = flatten_expr(n.left)
        comps, comparators = zip(*[flatten_expr(x) for x in n.comparators])
        ops = []
        for op in n.ops:
            if not (isinstance(n, ast.Eq) or isinstance(n, ast.NotEq)):
                ops.append(flattenAST(op))
            else:
                ops.append(flatten_expr(n)[0])
        temp = get_new_temp()
        temps = [temp]
        string = temp + " = " + str(left)
        for x in comps:
            tempt = get_new_temp()
            temps.append(tempt)
            string = string + "\n" + tempt + " = " + str(x)
        rightc = temps[1]
        for x in range(len(ops)):
            if "(" in ops[x]:
                string = string + "\n" + temp + " = " + ops[x].replace("()", "(") + temp + "," + rightc + ")"
            else:
                string = string + "\n" + temp + " = " + temp + " " + ops[x] + " " + rightc
            if x + 2 < len(temps):
                rightc = temps[x + 2]
        return temp, left_code + "".join([x for x in comparators]) + string + "\n"

    elif isinstance(n, ast.BinOp):
        left, left_code = flatten_expr(n.left)
        right, right_code = flatten_expr(n.right)
        left_call = isinstance(n.left, ast.Call) or isinstance(n.left, explicate.UnboxInt) or isinstance(n.left,
                                                                                                         explicate.UnboxBool)
        right_call = isinstance(n.right, ast.Call) or isinstance(n.right, explicate.UnboxInt) or isinstance(n.right,
                                                                                                            explicate.UnboxBool)
        code = ""
        temp = get_new_temp()
        if left_call or right_call:
            temp2 = left
            temp3 = right
            if left_call:
                temp2 = get_new_temp()
                code += left_code + temp2 + " = " + left + "\n"
            if right_call:
                temp3 = get_new_temp()
                code += right_code + temp3 + " = " + right + "\n"
            code += "" + left_code + right_code + temp + " = " + temp2 + " + " + temp3 + "\n"
        else:
            op = flattenAST(n.op)
            code += "" + left_code + right_code + temp + " = " + left + " " + op + " " + right + "\n"
        return temp, code

    elif isinstance(n, ast.UnaryOp):
        operand, operand_code = flatten_expr(n.operand)
        temp = get_new_temp()
        op = flattenAST(n.op)
        if isinstance(n.op, ast.Not):
            temp_assign = get_new_temp()
            operand = operand.replace("temp_replace_me", temp_assign)
            temp3 = get_new_temp()
            code = (operand_code + temp_assign + " = " + operand +
                    (("\n" + temp3 + " = is_true(" + temp_assign + ")") if "is_" not in operand else "")
                                                        + "\nif " + (temp3 if "is_" not in operand else temp_assign) + ":\n\x09"
                                                        + temp + " = inject_bool(False)\nelse\n\x09"
                                                        + temp + " = inject_bool(True)\n")
            return temp, code
        if isinstance(n.op, ast.USub):
            temp = get_new_temp()
            temp2 = get_new_temp()
            temp3 = get_new_temp()
            temp4 = get_new_temp()
            prep = temp2 + " = is_int(" + temp + ")\n"
            prep += "if " + temp2 + ":\n\x09"
            prep += temp + " = project_int(" + temp + ")\n\x09"
            prep += temp + " = -" + temp + "\n\x09"
            prep += temp + " = inject_int(" + temp + ")\n"
            prep += "else:\n\x09"
            prep += temp3 + " = is_bool(" + temp + ")\n\x09"
            prep += "if " + temp3 + ":\n\x09\x09"
            prep += temp + " = project_bool(" + temp + ")\n\x09\x09"
            prep += temp + " = -" + temp + "\n\x09\x09"
            prep += temp + " = inject_bool(" + temp + ")\n\x09"
            prep += "else:\n\x09\x09"
            prep += temp4 + " = is_big(" + temp + ")\n\x09\x09"
            prep += "if " + temp4 + ":\n\x09\x09\x09"
            prep += temp + " = project_big(" + temp + ")\n\x09\x09\x09"
            prep += temp + " = -" + temp + "\n\x09\x09\x09"
            prep += temp + " = inject_big(" + temp + ")\n\x09\x09"
            prep += "else:\n\x09\x09\x09"
            prep += "error_pyobj(\"Type Checking Error\")\n"
            code = operand_code + temp + " = " + operand + "\n" + prep
            return temp, code
        code = operand_code + temp + " = " + operand + "\n" + temp + " = " + op + temp + "\n"
        return temp, code

    elif isinstance(n, ast.Call):
        if (isinstance(n.func, ast.Name) and n.func.id == "eval" and
                len(n.args) == 1 and isinstance(n.args[0], ast.Call) and
                isinstance(n.args[0].func, ast.Name) and n.args[0].func.id == "input"):
            temp = get_new_temp()
            code = temp + " = eval_input_pyobj()\n"
            return temp, code

        args_code = ""
        args_flat = []
        preamble = ""
        for arg in n.args:
            temp = get_new_temp()
            flat_arg, arg_code = flatten_expr(arg, temp)
            preamble += temp + " = " + flat_arg + "\n"
            flat_arg = temp
            args_code += arg_code
            args_flat.append(flat_arg)
        args_str = ", ".join(args_flat)

        if isinstance(n.func, ast.Name) and n.func.id == "print_any":
            return "print_any(" + args_str + ")\n", args_code + preamble
        elif isinstance(n.func, ast.Name) and n.func.id == "int":
            temp = get_new_temp()
            temp2 = get_new_temp()
            temp3 = get_new_temp()
            temp4 = get_new_temp()
            prep = temp2 + " = is_int(" + args_str + ")\n"
            prep += "if " + temp2 + ":\n\x09"
            prep += args_str + " = project_int(" + args_str + ")\n"
            prep += "else:\n\x09"
            prep += temp3 + " = is_bool(" + args_str + ")\n\x09"
            prep += "if " + temp3 + ":\n\x09\x09"
            prep += args_str + " = project_bool(" + args_str + ")\n\x09"
            prep += "else:\n\x09\x09"
            prep += temp4 + " = is_big(" + args_str + ")\n\x09\x09"
            prep += "if " + temp4 + ":\n\x09\x09\x09"
            prep += args_str + " = project_big(" + args_str + ")\n\x09\x09"
            prep += "else:\n\x09\x09\x09"
            prep += "error_pyobj(\"Type Checking Error\")\n"
            prep += temp + " = inject_int(" + args_str + ")\n"
            return temp, args_code + preamble + prep

        else:
            temp = get_new_temp()
            code = args_code + preamble + temp + " = " + flattenAST(n.func) + "(" + args_str + ")\n"
            return temp, code


    else:
        raise Exception('Error in unparse: unrecognized AST node: ' + str(n))


def flattenAST(n):
    global temp1
    global tmp_list
    if isinstance(n, ast.Module):
        return "".join([flattenAST(x) for x in n.body])

    elif isinstance(n, ast.Assign):
        targets = ""
        for x in n.targets:
            if isinstance(x, ast.Subscript):
                if isinstance(x.ctx, ast.Store):
                    res = flatten_expr(x)
                    targets += res[1] + res[0] + "\n"
                    continue
                else:
                    targets += flatten_expr(x.value)[0] + ", "
                    continue
            targets += flattenAST(x) + ", "
        targets = targets[0:-2]
        rhs, rhs_code = flatten_expr(n.value, targets)
        if isinstance(x, ast.Subscript):
            if isinstance(x.ctx, ast.Store):
                temp = get_new_temp()
                code = temp + " = " + rhs + "\n"
                return rhs_code + code + targets + " " + temp + ")\n"
        return "" + rhs_code + (targets + " = " + rhs) + "\n"

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
        temp3 = get_new_temp()
        test_code += ((temp3 + " = is_true(" + test + ")\n") if "is_" not in test else "")
        if isinstance(n, ast.While):
            return test_code + str(type(n).__name__).lower() + " " + temp3 + ":\n" + body_code + (
                ("else:\n" + else_code) if len(else_code) != 0 else "") + "\x09" + test_code.replace("\n", "\n\x09")[
                                                                                   0:-1]

        return test_code + str(type(n).__name__).lower() + " " + temp3 + ":\n" + body_code + (
            ("else:\n" + else_code) if len(else_code) != 0 else "")

    elif isinstance(n, ast.Add):
        return "+"

    elif isinstance(n, ast.USub):
        return "-"

    elif isinstance(n, ast.Name):
        return n.id

    elif isinstance(n, explicate.IsEqual):
        return "equal()"

    elif isinstance(n, explicate.IsNotEqual):
        return "not_equal()"

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
