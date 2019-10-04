from stack import Stack
from instructions import InstructionSet

class VirtualMachine:
    def __init__(self, code):
        self.data_stack = Stack()
        self.instruction_ptr = 0
        self.code = code
        self.instruction_set = InstructionSet
        self.ret_addr_stack = Stack()
        self.ret_ctx_stack = Stack()
        self.symbols = {}
        self.ctx = '_global'
    
    def run(self):
        try:
            while self.instruction_ptr < len(self.code):
                op = self.code[self.instruction_ptr]
                # print(self.ret_addr_stack, self.data_stack, '[{}, {}]'.format(self.instruction_ptr, op))
                self.instruction_ptr += 1
                self.dispatch(op)
        except Exception as e:
            raise RuntimeError(str(e))

    def dispatch(self, op):
        if op in self.instruction_set:
            self.instruction_set[op](self)
        elif isinstance(op, int) or isinstance(op, float):
            self.data_stack.push(op)
        elif isinstance(op, str) and op[0] == op[-1] == '"':
            self.data_stack.push(op[1:-1])
        else:
            raise RuntimeError('Unkown opcode {}'.format(op))
    

if __name__ == "__main__":
    vm0 = VirtualMachine([
        '"square"', 11, 'function',
        'dup', '"x0"', 'local',
        '"x1"', 'local',
        '"x0"', 'symval', '"x1"', 'symval', 'mul',
        'ret',

        5, '"x"', 'global',

        '"x"', 'symval', '"square"', 'call', '"x"', 'global',

        7, '"y"', 'global',

        '"x"', 'symval', '"y"', 'symval', 'minus',
        
        'println'
    ])
    vm1 = VirtualMachine([
        1, 2, 'eq', 
        7, 9, 'if', 
        'jmp',
        '"test1"', 'print',
        '"test2"', 'print',
    ])
    vm1.run()
    # print(vm.ret_addr_stack)
    # print(vm.data_stack)
    