from collections import deque

class Stack(deque):
    push = deque.append

    @property
    def top(self):
        return self[-1]
