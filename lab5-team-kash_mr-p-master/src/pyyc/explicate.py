import ast


class InjectInt(ast.AST):
    _fields = ('value',)


class InjectBig(ast.AST):
    _fields = ('value',)


class InjectBool(ast.AST):
    _fields = ('value',)


class CheckIntTag(ast.AST):
    _fields = ('value',)


class CheckBigTag(ast.AST):
    _fields = ('value',)


class CheckBoolTag(ast.AST):
    _fields = ('value',)


class CheckFunTag(ast.AST):
    _fields = ('value',)


class IsTrue(ast.AST):
    _fields = ('value',)


class IsEqual(ast.AST):
    _fields = ('left', 'right')


class IsNotEqual(ast.AST):
    _fields = ('left', 'right')


class UnboxInt(ast.AST):  # project_int
    _fields = ('value',)


class UnboxBig(ast.AST):  # project_big
    _fields = ('value',)


class UnboxBool(ast.AST):  # project_bool
    _fields = ('value',)


class BigAdd(ast.AST):
    _fields = ('left', 'right')


class CallError(ast.AST):
    _fields = ()


class Let(ast.AST):
    _fields = ('var', 'value', 'body')


class GetFunc(ast.AST):
    _fields = ('value',)


class GetFrees(ast.AST):
    _fields = ('value',)


class ExplicateAdd(ast.NodeTransformer):

    def __init__(self):
        self.temp_counter = 0
        self.lambdas = 0

    def get_new_temp(self):
        self.temp_counter += 1
        return "explicate_temp" + str(self.temp_counter - 1)

    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            return InjectBool(value=node.value)
        if isinstance(node.value, int):
            return InjectInt(value=node.value)
        return InjectBig(value=node.value)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Name):
            if "fun_" in node.value.id:
                new_val = InjectBig(ast.Call(
                    func=ast.Name(id="create_closure", ctx=ast.Load()),
                    args=[node.value, ast.List(elts=[], ctx=ast.Load())],
                    keywords=[]))
                node.value = new_val
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        new_args = [self.visit(arg) for arg in node.args]
        if isinstance(node.func, ast.Name) and not (node.func.id == 'print') and not (
                node.func.id == "eval") and not (node.func.id == "input") and not (node.func.id == "create_closure") and not (node.func.id == "int"):
            transformed_func = self.visit(node.func)
            transformed_args = new_args
            check_res = self.get_new_temp()
            call_res = self.get_new_temp()
            new_node = Let(var=ast.Name(id=check_res, ctx=ast.Store()),
                           value=CheckFunTag(transformed_func),
                           body=ast.IfExp(
                               test=ast.Name(id=check_res, ctx=ast.Load()),
                               body=Let(
                                   var=ast.Name(id=call_res, ctx=ast.Store()),
                                      value=ast.Call(
                                            func=ast.Call(
                                                func=ast.Name(id='get_fun_ptr', ctx=ast.Load()),
                                                args=[ast.Name(id=transformed_func.id)],
                                                keywords=[],
                                            ),
                                        args=[ast.Call(
                                                        func=ast.Name(id='get_free_vars', ctx=ast.Load()),
                                                        args=[ast.Name(id=transformed_func.id, ctx=ast.Load())],
                                                        keywords=[]
                                                    )
                                                ] + transformed_args,
                                        keywords=[]
                                      ),
                                   body=ast.Name(id=call_res, ctx=ast.Load())
                               ),
                                orelse=ast.Call(
                                func=ast.Name(id=transformed_func.id, ctx=ast.Load()),
                                args=transformed_args,
                                keywords=[]
                                )
                               #orelse=CallError()
                           )
                        )
            return new_node
        
        elif isinstance(node.func, ast.Attribute):
            transformed_func = self.visit(node.func)
            transformed_args = [self.visit(arg) for arg in node.args]
            return ast.Call(
                func=transformed_func,
                args=transformed_args,
                keywords=[]
            )
        elif isinstance(node.func, ast.Call):
            transformed_func = self.visit(node.func)
            transformed_args = [self.visit(arg) for arg in node.args]
            return ast.Call(
                func=transformed_func,
                args=transformed_args,
                keywords=[]
            )    

        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            node.func.id = 'print_any'
        node.args = new_args
        return node
    # def visit_Return(self, node):
    #    node.value = self.visit(node.value)
    #    node = ast.Return(value=Let(var=ast.Name(id='return_temp', ctx=ast.Store()), value=node.value, body=ast.IfExp(
    #        test=CheckIntTag(value=ast.Name(id='return_temp', ctx=ast.Load())),
    #        body=UnboxInt(value=ast.Name(id='return_temp', ctx=ast.Load())),
    #        orelse=ast.IfExp(
    #            test=CheckBoolTag(value=ast.Name(id='return_temp', ctx=ast.Load())),
    #            body=UnboxBool(value=ast.Name(id='return_temp', ctx=ast.Load())),
    #            orelse=ast.IfExp(
    #                test=CheckBigTag(value=ast.Name(id='return_temp', ctx=ast.Load())),
    #                body=UnboxBig(value=ast.Name(id='return_temp', ctx=ast.Load())),
    #                orelse=CallError()
    #            )
    #        )
    #    )))
    #    return node

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(node.op, ast.Add):
            return Let(var=ast.Name(id='result_temp', ctx=ast.Store()),
                       value=left,
                       body=Let(var=ast.Name(id='left_temp', ctx=ast.Store()),
                                value=right,
                                body=ast.IfExp(
                                    test=ast.BoolOp(op=ast.And(), values=[
                                        CheckIntTag(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                        CheckIntTag(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                    ]),
                                    body=InjectInt(value=ast.BinOp(
                                        left=UnboxInt(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                        op=ast.Add(),
                                        right=UnboxInt(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                    )),
                                    orelse=ast.IfExp(
                                        test=ast.BoolOp(op=ast.And(), values=[
                                            CheckBoolTag(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                            CheckBoolTag(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                        ]),
                                        body=InjectBool(value=ast.BinOp(
                                            left=UnboxBool(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                            op=ast.Add(),
                                            right=UnboxBool(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                        )),
                                        orelse=ast.IfExp(
                                            test=ast.BoolOp(op=ast.And(), values=[
                                                CheckBoolTag(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                                CheckIntTag(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                            ]),
                                            body=InjectInt(value=ast.BinOp(
                                                left=UnboxBool(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                                op=ast.Add(),
                                                right=UnboxInt(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                            )),
                                            orelse=ast.IfExp(
                                                test=ast.BoolOp(op=ast.And(), values=[
                                                    CheckIntTag(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                                    CheckBoolTag(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                                ]),
                                                body=InjectInt(value=ast.BinOp(
                                                    left=UnboxInt(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                                    op=ast.Add(),
                                                    right=UnboxBool(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                                )),
                                                orelse=ast.IfExp(
                                                    test=ast.BoolOp(op=ast.And(), values=[
                                                        CheckBigTag(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                                        CheckBigTag(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                                    ]),
                                                    body=InjectBig(value=BigAdd(
                                                        left=UnboxBig(value=ast.Name(id='result_temp', ctx=ast.Load())),
                                                        right=UnboxBig(value=ast.Name(id='left_temp', ctx=ast.Load()))
                                                    )),
                                                    orelse=CallError()
                                                )
                                            )
                                        )
                                    )
                                )))
        return node

    def visit_Compare(self, node):
        left = self.visit(node.left)
        comparator_temps = []
        for comparator in node.comparators:
            temp_comparator = self.get_new_temp()
            comparator_temps.append((temp_comparator, self.visit(comparator)))
        result_temp = self.get_new_temp()
        comparisons = []
        for i, op in enumerate(node.ops):
            if isinstance(op, ast.Eq) or isinstance(op, ast.NotEq):
                if isinstance(op, ast.Eq):
                    comp_op = ast.Eq()
                    big_op = IsEqual()
                else:
                    comp_op = ast.NotEq()
                    big_op = IsNotEqual()
                temp_left = ast.Name(id=result_temp, ctx=ast.Load()) if i == 0 else ast.Name(
                    id=comparator_temps[i - 1][0], ctx=ast.Load())
                temp_right = ast.Name(id=comparator_temps[i][0], ctx=ast.Load())
                comparison = ast.IfExp(
                    test=ast.BoolOp(
                        op=ast.And(),
                        values=[CheckIntTag(value=temp_left), CheckIntTag(value=temp_right)]
                    ),
                    body=InjectBool(value=ast.Compare(
                        left=UnboxInt(value=temp_left),
                        ops=[comp_op],
                        comparators=[UnboxInt(value=temp_right)]
                    )),
                    orelse=ast.IfExp(
                        test=ast.BoolOp(
                            op=ast.And(),
                            values=[CheckBoolTag(value=temp_left), CheckBoolTag(value=temp_right)]
                        ),
                        body=InjectBool(value=ast.Compare(
                            left=UnboxBool(value=temp_left),
                            ops=[comp_op],
                            comparators=[UnboxBool(value=temp_right)]
                        )),
                        orelse=ast.IfExp(
                            test=ast.BoolOp(
                                op=ast.And(),
                                values=[CheckIntTag(value=temp_left), CheckBoolTag(value=temp_right)]
                            ),
                            body=InjectBool(value=ast.Compare(
                                left=UnboxInt(value=temp_left),
                                ops=[comp_op],
                                comparators=[UnboxBool(value=temp_right)]
                            )),
                            orelse=ast.IfExp(
                                test=ast.BoolOp(
                                    op=ast.And(),
                                    values=[CheckBoolTag(value=temp_left), CheckIntTag(value=temp_right)]
                                ),
                                body=InjectBool(value=ast.Compare(
                                    left=UnboxBool(value=temp_left),
                                    ops=[comp_op],
                                    comparators=[UnboxInt(value=temp_right)]
                                )),
                                orelse=ast.IfExp(
                                    test=ast.BoolOp(
                                        op=ast.And(),
                                        values=[CheckBigTag(value=temp_left), CheckBigTag(value=temp_right)]
                                    ),
                                    body=InjectBool(value=ast.Compare(
                                        left=UnboxBig(value=temp_left),
                                        ops=[big_op],
                                        comparators=[UnboxBig(value=temp_right)]
                                    )),

                                    orelse=CallError())))))
                comparisons.append((result_temp if i == len(node.ops) - 1 else self.get_new_temp(), comparison))

            if isinstance(op, ast.Is):
                temp_left = ast.Name(id=result_temp, ctx=ast.Load()) if i == 0 else ast.Name(
                    id=comparator_temps[i - 1][0], ctx=ast.Load())
                temp_right = ast.Name(id=comparator_temps[i][0], ctx=ast.Load())
                comparison = ast.IfExp(
                    test=ast.BoolOp(
                        op=ast.And(),
                        values=[CheckIntTag(value=temp_left), CheckIntTag(value=temp_right)]
                    ),
                    body=InjectBool(value=ast.Compare(
                        left=UnboxInt(value=temp_left),
                        ops=[ast.Eq()],
                        comparators=[UnboxInt(value=temp_right)]
                    )),
                    orelse=ast.IfExp(
                        test=ast.BoolOp(
                            op=ast.And(),
                            values=[CheckBoolTag(value=temp_left), CheckBoolTag(value=temp_right)]
                        ),
                        body=InjectBool(value=ast.Compare(
                            left=UnboxBool(value=temp_left),
                            ops=[ast.Eq()],
                            comparators=[UnboxBool(value=temp_right)]
                        )),
                        orelse=ast.IfExp(
                            test=ast.BoolOp(
                                op=ast.And(),
                                values=[CheckIntTag(value=temp_left), CheckBoolTag(value=temp_right)]
                            ),
                            body=InjectBool(value=ast.Compare(
                                left=temp_left,
                                ops=[ast.Eq()],
                                comparators=[temp_right]
                            )),
                            orelse=ast.IfExp(
                                test=ast.BoolOp(
                                    op=ast.And(),
                                    values=[CheckBoolTag(value=temp_left), CheckIntTag(value=temp_right)]
                                ),
                                body=InjectBool(value=ast.Compare(
                                    left=temp_left,
                                    ops=[ast.Eq()],
                                    comparators=[temp_right]
                                )),
                                orelse=ast.IfExp(
                                    test=ast.BoolOp(
                                        op=ast.And(),
                                        values=[CheckBigTag(value=temp_left), CheckBigTag(value=temp_right)]
                                    ),
                                    body=InjectBool(value=ast.Compare(
                                        left=temp_left,
                                        ops=[ast.Eq()],
                                        comparators=[temp_right]
                                    )),
                                    orelse=ast.IfExp(
                                        test=ast.BoolOp(
                                            op=ast.And(),
                                            values=[CheckBigTag(value=temp_left), CheckIntTag(value=temp_right)]
                                        ),
                                        body=InjectBool(value=ast.Compare(
                                            left=temp_left,
                                            ops=[ast.Eq()],
                                            comparators=[temp_right]
                                        )),
                                        orelse=ast.IfExp(
                                            test=ast.BoolOp(
                                                op=ast.And(),
                                                values=[CheckIntTag(value=temp_left), CheckBigTag(value=temp_right)]
                                            ),
                                            body=InjectBool(value=ast.Compare(
                                                left=temp_left,
                                                ops=[ast.Eq()],
                                                comparators=[temp_right]
                                            )),

                                            orelse=CallError())))))))
                comparisons.append((result_temp if i == len(node.ops) - 1 else self.get_new_temp(), comparison))
        body = comparisons[-1][1]
        for var, comp in reversed(comparisons[:-1]):
            body = Let(var=ast.Name(id=var, ctx=ast.Store()), value=comp, body=body)
        for var, comp in reversed(comparator_temps):
            body = Let(var=ast.Name(id=var, ctx=ast.Store()), value=comp, body=body)

        return Let(var=ast.Name(id=result_temp, ctx=ast.Store()), value=left, body=body)
