

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

        print("Access " + str(index) + ":"),
        for item in self.history:
            print(item[0]),
        print("")
        self.clock += 1


class MissRate:
    def __init__(self, target_rate):
        self.target_rate = target_rate
        self.previous_miss = 0
        self.memory = []
        self.clock = 0
        self.history = []

    def access(self, index):
        self.history.append(index)
        if len(self.history) > self.target_rate + 1:
            del self.history[0]
        self.clock += 1

        if index not in self.memory:
            miss_interval = self.clock - self.previous_miss
            self.previous_miss = self.clock

            if miss_interval <= self.target_rate:
                self.memory.append(index)
            else:
                new_memory = []
                for item in self.memory:
                    if item in self.history:
                        new_memory.append(item)
                self.memory = new_memory
                self.memory.append(index)

        print("Access " + str(index) + ":"),
        for item in self.memory:
            print(item),
        print("")


if __name__ == '__main__':

    sequence = ['e', 'd', 'a', 'c', 'c', 'd', 'b', 'c', 'e', 'c', 'e', 'a', 'd']

    print("By working set algorithm:")
    working_set = WorkingSet(4)
    for index in sequence:
        working_set.access(index)

    print("By miss rate algorithm: ")
    miss_rate = MissRate(2)
    for index in sequence:
        miss_rate.access(index)

