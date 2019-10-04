import sys
from symbol import Symbol

def op_add(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    assert (isinstance(x0, int) or isinstance(x0, float)) and \
        (isinstance(x1, int) or isinstance(x1, float)), \
        'ADD: data are not number'
    machine.data_stack.push(x1 + x0)

def op_minus(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    assert (isinstance(x0, int) or isinstance(x0, float)) and \
        (isinstance(x1, int) or isinstance(x1, float)), \
        'MINUS: data are not number'
    machine.data_stack.push(x1 - x0)

def op_mul(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    assert (isinstance(x0, int) or isinstance(x0, float)) and \
        (isinstance(x1, int) or isinstance(x1, float)), \
        'MUL: data are not number'
    machine.data_stack.push(x1 * x0)

def op_div(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    assert (isinstance(x0, int) or isinstance(x0, float)) and \
        (isinstance(x1, int) or isinstance(x1, float)), \
        'DIV: data are not number'
    assert x0 != 0, 'DIV: can not divide by zero'
    machine.data_stack.push(x1 / x0)

def op_mod(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    assert (isinstance(x0, int) or isinstance(x0, float)) and \
        (isinstance(x1, int) or isinstance(x1, float)), \
        'MOD: data are not number'
    assert x0 != 0, 'MOD: can not mod zero'
    machine.data_stack.push(x1 % x0)

def op_eq(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    machine.data_stack.push(x1 == x0)

def op_neq(machine):
    x0 = machine.data_stack.pop()
    x1 = machine.data_stack.pop()
    machine.data_stack.push(x1 != x0)

def op_if(machine):
    false_st = machine.data_stack.pop()
    true_st = machine.data_stack.pop()
    test = machine.data_stack.pop()
    assert isinstance(test, bool), 'IF: test statement is not boolean'
    machine.data_stack.push(true_st if test is True else false_st)


def op_jmp(machine):
    addr = machine.data_stack.pop()
    assert isinstance(addr, int), 'JMP: jump address is not number'
    if addr in range(len(machine.code)):
        machine.instruction_ptr = addr
    else:
        raise RuntimeError('JMP: jump address is not valid')

def op_dup(machine):
    machine.data_stack.push(machine.data_stack.top)

def op_print(machine):
    x0 = machine.data_stack.pop()
    sys.stdout.write(str(x0))
    sys.stdout.flush()

def op_println(machine):
    x0 = machine.data_stack.pop()
    sys.stdout.write('{}\n'.format(str(x0)))
    sys.stdout.flush()

def op_global(machine):
    var_name = machine.data_stack.pop()
    var_val = machine.data_stack.pop()
    var_name_w_ctx = '{}.{}'.format(machine.ctx, var_name)
    symbol = Symbol(var_name_w_ctx, 'variable', var_val)
    machine.symbols[var_name_w_ctx] = symbol

def op_local(machine):
    var_name = machine.data_stack.pop()
    var_val = machine.data_stack.pop()
    var_name_w_ctx = '{}.{}.{}'.format(machine.ctx, '.'.join(list(machine.ret_ctx_stack)), var_name) 
    symbol = Symbol(var_name_w_ctx, 'variable', var_val)
    machine.symbols[var_name_w_ctx] = symbol

def op_function(machine):
    fun_pad = machine.data_stack.pop()
    fun_name = machine.data_stack.pop()
    fun_name_w_ctx = '{}.{}'.format(machine.ctx, fun_name)
    symbol = Symbol(fun_name_w_ctx, 'function', machine.instruction_ptr, fun_pad)
    machine.symbols[fun_name_w_ctx] = symbol
    machine.instruction_ptr = machine.instruction_ptr + fun_pad

def op_call(machine):
    fun_name = machine.data_stack.pop()
    fun_name_w_ctx = '{}.{}'.format(machine.ctx, fun_name)
    symbol = machine.symbols[fun_name_w_ctx]
    current_ip = machine.instruction_ptr
    machine.instruction_ptr = symbol.value
    machine.ret_addr_stack.push(current_ip)
    machine.ret_ctx_stack.push(fun_name)

def op_ret(machine):
    len_ctx = len(machine.ret_ctx_stack) + 2
    for symbol in list(machine.symbols):
        if len(machine.symbols[symbol].name.split('.')) == len_ctx:
            del machine.symbols[symbol]
    machine.instruction_ptr = machine.ret_addr_stack.pop()
    machine.ret_ctx_stack.pop()

def op_symval(machine):
    var_name = machine.data_stack.pop()
    if machine.ret_ctx_stack: 
        var_name_w_ctx = '{}.{}.{}'.format(machine.ctx, '.'.join(list(machine.ret_ctx_stack)), var_name)
    else:
        var_name_w_ctx = '{}.{}'.format(machine.ctx, var_name)
    assert var_name_w_ctx in machine.symbols, 'symbol {} not exists'.format(var_name_w_ctx)
    machine.data_stack.push(machine.symbols[var_name_w_ctx].value)

def op_delsym(machine):
    var_name = machine.data_stack.pop()
    if machine.ret_ctx_stack: 
        var_name_w_ctx = '{}.{}.{}'.format(machine.ctx, '.'.join(list(machine.ret_ctx_stack)), var_name)
    else:
        var_name_w_ctx = '{}.{}'.format(machine.ctx, var_name)
    assert var_name_w_ctx in machine.symbols, 'symbol {} not exists'.format(var_name_w_ctx)
    del machine.symbols[var_name_w_ctx]

def op_exit(machine):
    sys.exit(0)

InstructionSet = {
    'add': op_add,
    'minus': op_minus,
    'mul': op_mul,
    'div': op_div,
    'mod': op_mod,
    'eq': op_eq,
    'neq': op_neq,
    'if': op_if,
    'jmp': op_jmp,
    'dup': op_dup,
    'print': op_print,
    'println': op_println,
    'global': op_global,
    'local': op_local,
    'function': op_function,
    'call': op_call,
    'ret': op_ret,
    'symval': op_symval,
    'delsym': op_delsym,
    'exit': op_exit
}