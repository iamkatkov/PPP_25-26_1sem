from collections import deque

class Stack:
    def __init__(self):
        self.stack = deque() 

    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def isEmpty(self):
        if len(self.stack) == 0:
            return True
        elif len(self.stack) > 0:
            return False

    def peek(self):
        if len(self.stack) == 0:
            return None
        element = self.stack[-1]
        return element
    
def check_stack(text):
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    for i in range(len(text)):
        ch = text[i]
        if ch in "([{":
            stack.push((ch, i + 1))  
        elif ch in ")]}":
            s = stack.pop()
            if s is None:  
                return i + 1
            if pairs[ch] != s[0]:  
                return i + 1

    if not stack.isEmpty():
        return stack.pop()[1]

    return "ok"

s = str(input())
print(check_stack(s))
