#!/usr/bin/env python

# 题目描述，用两个栈实现一个队列


class TwoStackQueue():
    def __init__(self):
        self.stack1, self.stack2 = [], []

    def __len__(self):
        return len(self.stack1) + len(self.stack2)

    def push(self, value):
        self.stack1 += [value]

    def pop(self):
        if not self:
            raise ValueError('Queue is empty')
        if self.stack2:
            return self.stack2.pop()

        while self.stack1:
            self.stack2 += [self.stack1.pop()]

        return self.stack2.pop()



if __name__ == '__main__':
    queue = TwoStackQueue()
    queue.push(1)
    queue.push(2)
    queue.push(3)
    print(queue.pop())
    print(queue.pop())
    queue.push(4)
    queue.push(5)
    print(queue.pop())
    while queue:
        print(queue.pop())

    queue.pop()
