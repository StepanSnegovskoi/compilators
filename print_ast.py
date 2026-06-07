from nodes import Node


def print_tree(node, prefix="", is_last=True):
    if node is None: return
    connector = "└── " if is_last else "├── "
    name = node.__class__.__name__.replace("Node", "")

    extra = ""
    if hasattr(node, "name"): extra += f" {node.name}"

    if hasattr(node, "value") and not isinstance(node.value, Node) and not isinstance(node.value, list):
        extra += f" = {node.value}"

    if hasattr(node, "op"): extra += f" {node.op}"

    print(prefix + connector + name + extra)

    prefix += "    " if is_last else "│   "

    children = []
    for attr in ["block", "decls", "stmts", "cond", "then_branch", "else_branch", "body", "start", "end", "target",
                 "value", "left", "right", "expr", "index", "args"]:
        if hasattr(node, attr):
            val = getattr(node, attr)
            if isinstance(val, list):
                children.extend(val)
            elif isinstance(val, Node):
                children.append(val)

    for i, child in enumerate(children):
        print_tree(child, prefix, i == len(children) - 1)