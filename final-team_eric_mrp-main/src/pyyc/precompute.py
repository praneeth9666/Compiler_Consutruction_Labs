import ast


class Compute(ast.NodeTransformer):

    def get_op(self, node):
        if isinstance(node, ast.Add):
            return "+"
        if isinstance(node, ast.USub):
            return "-"

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            return ast.Constant(value=eval(f"{node.left.value} {self.get_op(node.op)} {node.right.value}"))
        return node

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if isinstance(node.operand, ast.Constant) and isinstance(node.op, ast.USub):
            return ast.Constant(value=eval(f"{self.get_op(node.op)}{node.operand.value}"))
        return node
