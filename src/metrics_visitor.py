import ast
from collections import defaultdict


class MetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.scope_stack = []

        self.metrics = defaultdict(lambda: {
            "assignments": 0,
            "statements": 0,
            "expressions": 0,
        })

    def current_scope(self):
        return ".".join(self.scope_stack) or "<module>"
    
    def visit(self, node):
        scope = self.current_scope()

        if isinstance(node, ast.stmt):
            self.metrics[scope]["statements"] += 1
        
        if isinstance(node, ast.expr):
            self.metrics[scope]["expressions"] += 1
        
        super().visit(node)

    def visit_ClassDef(self, node):
        self.scope_stack.append(f"{node.name}:{node.lineno}")
        self.generic_visit(node)
        self.scope_stack.pop()
    
    def visit_FunctionDef(self, node):
        self.scope_stack.append(f"{node.name}:{node.lineno}")
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_Assign(self, node):
        scope = self.current_scope()
        self.metrics[scope]["assignments"] += 1
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node):
        scope = self.current_scope()
        self.metrics[scope]["assignments"] += 1
        self.generic_visit(node)
