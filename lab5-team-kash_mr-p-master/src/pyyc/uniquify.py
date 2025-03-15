import ast


class Uniquify(ast.NodeTransformer):

    def __init__(self):
        self._count = 0
        self._fun_count = 0
        self._scopes = [dict()]
        self._undefined_names = []

    def run(self, tree):
        self.visit(tree)
        for x in self._undefined_names:
            if x.id in self._scopes[0]:
                x.id = self._scopes[0][x.id]
        return tree

    def get_new_var_name(self):
        new_name = "var_" + str(len(self._scopes) - 1) + "_" + str(self._count)
        self._count += 1
        return new_name

    def get_new_fun_name(self):
        new_name = "fun_" + str(self._fun_count)
        self._fun_count += 1
        return new_name

    def get_var_replacement(self, var):
        for scope in self._scopes:
            if var in scope:
                return scope[var]
        return None

    def visit_Name(self, node):
        new_name = self.get_var_replacement(node.id)
        if new_name is not None and (isinstance(node.ctx, ast.Load) or node.id in self._scopes[0]):
            node.id = new_name
        elif isinstance(node.ctx, ast.Store):
            new_name = self.get_new_var_name()
            self._scopes[0][node.id] = new_name
            node.id = new_name
        else:
            self._undefined_names.append(node)

        return node

    def visit_arg(self, node):
        new_name = self.get_new_var_name()
        self._scopes[0][node.arg] = new_name
        node.arg = new_name
        return node


    def visit_FunctionDef(self, node):
        new_fun_name = self.get_new_fun_name()
        self._scopes[0][node.name] = new_fun_name
        self._scopes.insert(0, dict())
        node.name = new_fun_name

        self.visit(node.args)
        for n in node.body:
            self.visit(n)
        self._scopes.pop(0)

        return node