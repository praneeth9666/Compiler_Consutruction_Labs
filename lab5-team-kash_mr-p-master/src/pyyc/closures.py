import ast
import explicate


class ClosureConverter(ast.NodeTransformer):
    class ScopeAnalyzer(ast.NodeTransformer):

        def __init__(self):
            self.scopes = {"global": []}
            self.free_vars = {"global": []}
            self.curr_scope = "global"

        def get_var_states(self, tree):
            self.visit(tree)
            return self.scopes, self.free_vars

        def nodes_to_names(self, nodes):
            return [x.id for x in nodes]

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                self.scopes[self.curr_scope].append(node)
            elif isinstance(node.ctx, ast.Load) and node.id not in self.nodes_to_names(self.scopes[self.curr_scope])\
                    and "fun_" not in node.id:
                self.free_vars[self.curr_scope].append(node)
            self.generic_visit(node)
            return node

        def visit_FunctionDef(self, node):
            self.scopes[self.curr_scope].append(ast.Name(id=node.name, ctx=ast.Store()))
            old_scope = self.curr_scope
            self.scopes[node.name] = []
            for x in node.args.args:
                self.scopes[node.name].append(ast.Name(id=x.arg, ctx=ast.Store()))
            self.free_vars[node.name] = []
            self.curr_scope = node.name
            self.generic_visit(node)
            self.curr_scope = old_scope
            return node

    def __init__(self):
        self._count = 0
        self.ScopeAnalyzer = self.ScopeAnalyzer()
        self._fun_scopes = None
        self._free_vars = None
        self._free_var_counter = 0
        self._curr_free = None
        self._curr_scope = "global"


    def create_closures(self, tree):
        self._fun_scopes, self._free_vars = self.ScopeAnalyzer.get_var_states(tree)
        self.visit(tree)

    def get_free_var_name(self):
        new_name = "free_var_" + str(self._free_var_counter)
        self._free_var_counter += 1
        return new_name

    def detect_and_create_closures(self, tree):
        self._fun_scopes, self._free_vars = self.ScopeAnalyzer.get_var_states(tree)
        self.visit(tree)

    def visit_Return(self, node):
        if isinstance(node.value, ast.Name):
            if "fun_" in node.value.id:
                temp = explicate.InjectBig(ast.Call(
                    func=ast.Name(id="create_closure", ctx=ast.Load()),
                    args=[node.value],
                    keywords=[]))
                temp.value.args.append(ast.List(elts=[], ctx=ast.Load()))
                for x in self._free_vars[node.value.id]:
                    temp.value.args[1].elts.append(ast.Name(id=x.id, ctx=ast.Load()))
                node.value = temp
        self.generic_visit(node)
        return node


    def visit_Subscript(self, node):
        if isinstance(node.value, ast.Name):
            free_vars = self._free_vars[self._curr_scope]
            lst = {}
            for x in free_vars:
                lst[x.id] = None
            lst = list(lst.keys())
            if node.value.id in lst:
                node.value = ast.Subscript(
                    value=ast.Name(id=self._curr_free, ctx=ast.Load()),
                    slice=ast.Constant(value=lst.index(node.value.id)),
                    ctx=node.ctx)
        self.generic_visit(node)
        return node


    def visit_FunctionDef(self, node):
        name = node.name
        scope = self._fun_scopes[name]
        free_vars = self._free_vars[name]
        temp_scope = self._curr_scope
        temp_free = self._curr_free
        if free_vars:
            lst = {}
            for x in free_vars:
                if x in scope:
                    lst[x.id] = None
            lst = list(lst.keys())
            free_var = self.get_free_var_name()
            self._curr_free = free_var
            self._curr_scope = name
            args = ast.arguments(
                posonlyargs=node.args.posonlyargs,
                args=[ast.arg(arg=free_var)] + node.args.args,
                vararg=node.args.vararg,
                kwonlyargs=node.args.kwonlyargs,
                kw_defaults=node.args.kw_defaults,
                kwarg=node.args.kwarg,
                defaults=node.args.defaults,)
            node.args = args
        for x in node.body:
            self.visit(x)
        self._curr_free = temp_free
        self._curr_scope = temp_scope

        return node
