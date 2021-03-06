def cpp_comment(text):
    return '// ' + text

def cpp_top_level_items(item_list):
    str = ""
    for item in item_list:
        str += item + "\n\n"
    return str

def cpp_include(name):
    return "#include \"" + name + "\""

def cpp_using(name):
    return "using namespace " + name + ";"

def cpp_enum(enum_name, field_names):
    str = "enum " + enum_name + " {\n"
    for name in field_names:
        str += "\t" + name + ",\n"
    str += "};"
    return str

def cpp_formal_param(param_type, param_name):
    return param_type + " " + param_name

def cpp_function(return_type, name, template_params, args, body):
    str = return_type + " " + name + "(" + cpp_param_list(args) + ")"
    str += "{\n" + cpp_stmt_list(1, body) + "}"
    return str

def cpp_assign(lhs, rhs):
    return lhs + ' = ' + rhs

def cpp_funcall(name, template_params, args):
    str = name
    if len(template_params) > 0:
        str += "<" + cpp_param_list(template_params) + ">"
    str += "(" + cpp_param_list(args) + ")"
    return str

def cpp_block(cpp_stmts):
    return "{ " + cpp_stmt_list(0, cpp_stmts) + "}"
    
def cpp_stmt_list(n, cpp_stmts):
    str = ""
    for stmt in cpp_stmts:
        str += indent(n) + stmt + ";\n"
    return str

def indent(n):
    if n == 0:
        return ""
    else:
        return "\t" + indent(n - 1)

def cpp_param_list(formal_params):
    if len(formal_params) == 0:
        return ""
    elif len(formal_params) == 1:
        return formal_params[0]
    else:
        return formal_params[0] + ", " + cpp_param_list(formal_params[1:])

def cpp_const(cpp_type):
    return "const " + cpp_type

def cpp_ref(cpp_type):
    return cpp_type + "&"

def cpp_ptr(cpp_type):
    return cpp_type + "*"

def cpp_var(name):
    return name

def cpp_void():
    return "void"

def cpp_int():
    return "int"

def cpp_char():
    return "char"
