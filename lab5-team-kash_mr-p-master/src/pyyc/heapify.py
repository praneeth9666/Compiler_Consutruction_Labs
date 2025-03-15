import ast
import builtins

def get_free_variables(tree):
    """
    Given a Python code snippet, return the list of free variables in the code.
    Ignores built-in functions, variables, and local function definitions.
    """
    # Parse the code to get the AST
   
    
    # Keep track of the bound variables and function names for each scope
    bound_vars_stack = [set(dir(builtins))]
    function_names = set()

    # Recursive function to traverse the AST and collect free variables
    def collect_free_vars(node, bound_vars_stack, function_names):
        free_vars = set()
        
        if isinstance(node, ast.FunctionDef):
            # Add the function name to the function names set
            function_names.add(node.name)
            
            # Add function parameters and defaults to bound variables for the new scope
            new_bound_vars = set(arg.arg for arg in node.args.args)
            new_bound_vars.update(function_names)
            bound_vars_stack.append(new_bound_vars)
            
            # Recursively process the function body and defaults
            for default in node.args.defaults:
                free_vars.update(collect_free_vars(default, bound_vars_stack, function_names))
            
            for body_node in node.body:
                free_vars.update(collect_free_vars(body_node, bound_vars_stack, function_names))
            
            # Pop the function scope before returning to the caller
            bound_vars_stack.pop()
        
        elif isinstance(node, ast.Assign):
            # Process the value side of the assignment first
            free_vars.update(collect_free_vars(node.value, bound_vars_stack, function_names))
            
            # Then add targets to bound variables for this scope
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bound_vars_stack[-1].add(target.id)
        
        elif isinstance(node, ast.Name):
            # Check if it's a variable reference, not a function, and not bound in the current scope
            if (node.id not in bound_vars_stack[-1] and 
                node.id not in function_names and 
                node.id not in dir(builtins)):
                free_vars.add(node.id)
        elif isinstance(node, ast.Call):
            # Check function call; this should not be counted as a free variable
            if isinstance(node.func, ast.Name):
                if node.func.id not in function_names:
                    pass
                    #free_vars.add(node.func.id)  # The function itself is free if not defined
            for arg in node.args:
                free_vars.update(collect_free_vars(arg, bound_vars_stack, function_names))
            for keyword in node.keywords:
                free_vars.update(collect_free_vars(keyword.value, bound_vars_stack, function_names))

        else:
            # Generic handler for all other node types
            for field, value in ast.iter_fields(node):
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, ast.AST):
                            free_vars.update(collect_free_vars(item, bound_vars_stack, function_names))
                elif isinstance(value, ast.AST):
                    free_vars.update(collect_free_vars(value, bound_vars_stack, function_names))
        
        return free_vars
    
    # Collect the free variables from the entire AST
    return list(collect_free_vars(tree, bound_vars_stack, function_names))
class TransformVariableAccess(ast.NodeTransformer):
    def __init__(self, free_vars):
        self.free_vars = free_vars

    def visit_Assign(self, node):
        # Transform the assignment of free variables into list assignments
        if isinstance(node.targets[0], ast.Name) and node.targets[0].id in self.free_vars:
            node.value = ast.List(elts=[node.value], ctx=ast.Load())
            return node
        return self.generic_visit(node)

    def visit_Name(self, node):
        # Replace all accesses of free variables with list index access
        if node.id in self.free_vars and isinstance(node.ctx, ast.Load):
            return ast.copy_location(
                ast.Subscript(
                    value=ast.Name(id=node.id, ctx=ast.Load()),
                    slice=ast.Index(value=ast.Constant(value=0)),
                    ctx=node.ctx
                ),
                node
            )
        return node
def transform_code(tree):
    free_vars = get_free_variables(tree)
    print(free_vars)
    transformer = TransformVariableAccess(free_vars)
    new_tree = transformer.visit(tree)
    return ast.unparse(new_tree)


