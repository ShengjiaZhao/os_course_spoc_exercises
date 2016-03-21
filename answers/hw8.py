

class WorkingSet:
    def __init__(self, window_size):
        self.window_size = window_size
        self.history = []
        self.clock = 0

    def access(self, index):
        for i in range(len(self.history)):
            if self.history[i][0] == index:
                del self.history[i]
                break

        self.history.append([index, self.clock])
        while self.clock - self.history[0][1] >= self.window_size:
            del self.history[0]

        for item in self.history:
            print(item[0]),
        print("")
        self.clock += 1


class MissRate:
    def __init__(self, rate):
        pass

    def access(self, index):
        pass


if __name__ == '__main__':
    working_set = WorkingSet(4)
    sequence = ['e', 'd', 'a', 'c', 'c', 'd', 'b', 'c', 'e', 'c', 'e', 'a', 'd']
    for index in sequence:
        working_set.access(index)


