from typing import List, Dict

# Python runtime version

class Int:
    def __init__(self, value):
        self.value = value


class Bool:
    def __init__(self, value):
        self.value = value

class Function:
    def __init__(self):
        self.value = None
        self.free_vars = None


class Big:
    def __init__(self, value):
        self.value = value


def is_int(val):
    return isinstance(val.value, int)


def is_bool(val):
    return isinstance(val.value, bool)


def is_big(val):
    return isinstance(val.value, object)


def inject_int(val: int):
    return Int(val)


def inject_bool(val: bool):
    return Bool(val)


def inject_big(val: object):
    return Big(val)


def project_int(val):
    if not is_int(val):
        raise Exception("Type Error")
    return val.value


def project_bool(val):
    if not is_bool(val):
        raise Exception("Type Error")
    return val.value


def project_big(val):
    if not is_big(val):
        raise Exception("Type Error")
    return val.value


def error_pyobj(val):
    raise Exception(val)


def is_true(val):
    if isinstance(val, Int):
        return val.value != 0
    elif isinstance(val, Bool):
        return val.value
    elif isinstance(val, Big):
        if isinstance(val, List) or isinstance(val, Dict):
            return len(val.value) != 0
        return val.value != 0

def is_function(val):
    return int(isinstance(val, Big) and isinstance(val.value, Function))


def not_equal(val1, val2):
    return val1.value != val2.value


def equal(val1, val2):
    return val1.value == val2.value


def add(val1, val2):
    return val1.value + val2.value

def create_list(len):
    lst = []
    for x in range(len.value):
        lst.append(None)
    return lst

def create_dict():
    return {}

def set_subscript(val, key, value):
    val.value[key.value] = value
    return val

def get_subscript(val, key):
    return val.value[key.value]

def create_closure(fun_ptr, free_vars):
    fun = Function()
    fun.value = fun_ptr
    fun.free_vars = free_vars
    return Big(fun)

def get_fun_ptr(pyobj):
    if isinstance(pyobj, Big) and isinstance(pyobj.value, Function):
        return pyobj.value.value
    raise Exception("Type Error")

def get_free_vars(pyobj):
    if isinstance(pyobj, Big) and isinstance(pyobj.value, Function):
        return pyobj.value.free_vars
    raise Exception("Type Error")

def set_free_vars(pyobj, free_vars):
    if isinstance(pyobj, Function):
        pyobj.free_vars = free_vars
        return pyobj
    raise Exception("Type Error")

def print_any(val):
    print(val.value)

def eval_input_pyobj():
    x = eval(input())
    if isinstance(x, int):
        return inject_int(x)
    elif isinstance(x, bool):
        return inject_bool(x)
    else:
        return inject_big(x)