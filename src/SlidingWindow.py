from collections import deque


class SlidingWindow:
    def __init__(self, size):
        self.window = deque()
        self.size = size
        self.sum = 0

    def add(self, i):
        if len(self.window) == self.size:
            left_val = self.window.popleft()
            self.sum -= left_val
        self.sum += i
        self.window.append(i)

    def mean(self):
        return self.sum / self.size
