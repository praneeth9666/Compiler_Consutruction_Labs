import ast

class Unify(ast.NodeTransformer):
    def __init__(self):
        self._count = 0
        self.new_defs = []  # Track new function defs globally
        self.current_function_scope = []  # Track function defs by scope

    def get_new_fun_name(self):
        new_name = "fun_" + str(self._count)
        self._count += 1
        return new_name

    def visit_Lambda(self, node):
        if isinstance(node.body, ast.Lambda):
            node.body = self.visit_Lambda(node.body)
        
        new_func_name = self.get_new_fun_name()
        new_func = ast.FunctionDef(
            name=new_func_name,
            args=node.args,
            body=[ast.Return(value=node.body)],
            decorator_list=[],
            lineno=node.lineno if hasattr(node, 'lineno') else None,
            col_offset=node.col_offset if hasattr(node, 'col_offset') else None
        )
        
        if self.current_function_scope:
            self.current_function_scope[-1].append(new_func)
        else:
            self.new_defs.append(new_func)
        
        return ast.Name(id=new_func_name, ctx=ast.Load())

    def visit_FunctionDef(self, node):
        self.current_function_scope.append([])
        self.generic_visit(node)  
        
        new_defs = self.current_function_scope.pop()
        insertion_index = 0
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.Assign):
                insertion_index = i + 1  

        node.body[insertion_index:insertion_index] = new_defs
        return node

    def visit_Module(self, node):
        self.current_function_scope.append([])
        self.generic_visit(node)  
        new_defs = self.current_function_scope.pop()
        node.body[0:0] = new_defs 
        return node
