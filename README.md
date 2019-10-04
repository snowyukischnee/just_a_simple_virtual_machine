# just_a_simple_virtual_machine

## Introduction
This is a simple virtual machine implementation using Python.

## Quickstart
Import `vm.py` then declare code for VM like this:
```python
    vm0 = VirtualMachine([
        # define function to calculate square of a number
        '"square"', 11, 'function',
        'dup', '"x0"', 'local',
        '"x1"', 'local',
        '"x0"', 'symval', '"x1"', 'symval', 'mul',
        'ret',
        # declare global variable x = 5
        5, '"x"', 'global',
        # feeding x into 'square' function
        # the return value will be assigned to x
        '"x"', 'symval', '"square"', 'call', '"x"', 'global',
        # declare global variable y = 7
        7, '"y"', 'global',
        # calculate x - y
        '"x"', 'symval', '"y"', 'symval', 'minus',
        # then print
        'println'
    ])
    vm0.run()
```
or
```python
    vm1 = VirtualMachine([
        # if 1 = 2 then print 'test1test2' else print 'test2'
        1, 2, 'eq', 
        7, 9, 'if', 
        'jmp',
        '"test1"', 'print',
        '"test2"', 'print',
    ])
    vm1.run()
```
## Opcodes
| Opcode        | Description            | Example   | Ex. Result |
| ------------- |:----------------------:|:---------:|:----------:|
|`add`          |calculate a + b         |`3 5 add`  |`8` (on top of stack)       
|`minus`        |calculate a - b         |`3 5 minus`|`-2` (on top of stack)
|`mul`          |calculate a * b         |`3 5 mul`  |`15` (on top of stack)
|`div`          |calculate a / b         |`8 4 div`  |`2` (on top of stack)
|`mod`          |calculate a mod b       |`8 5 mod`  |`3` (on top of stack)
|`eq`           |test if a == b          |`1 3 eq`   |`False` (on top of stack)
|`neq`          |test if a != b          |`2 4 neq`  |`True` (on top of stack)
|`if`           |jump to statement 1 if test statement is true, statement 2 otherwise|`1 2 eq 7 9 if jmp "test1" print "test2" print` | `test2` (on screen)
|`jmp`          |jump to specific address on stack|`5 jmp`|
|`dup`          |duplicate top stack value|`dup`|
|`print`        |print top stack value|`5 print`| `5` (on screen)
|`println`      |print top stack value with endline|`7 print`| `7` (on screen)
|`global`       |declare global variable|`5 "x" global`|
|`local`        |declare local variable|`4 "x1" local`|
|`function`     |declare function (with number of following ops)|`"fn" 11 function`|
|`call`         |call function|`"fn" call`|
|`ret`          |return from function with value is top stack value |`ret`|
|`symval`       |get value from symbol (variable value or function address)|`"x" symval`|
|`delsym`       |delete variable or function|``"x" delsym``|
|`exit`         |exit kernel||
