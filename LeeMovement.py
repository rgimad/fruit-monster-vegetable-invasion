import queue
import threading
import time

class Field(object):

    def __init__(self, rows, cols, start, finish, barriers):
        self.row = rows
        self.col = cols
        self.start = start
        self.finish = finish
        self.barriers = barriers
        self.field = None
        self.build()

    def __call__(self, *args, **kwargs):
        self.show()

    def __getitem__(self, item):
        return self.field[item]

    def build(self):
        self.field = [[0 for i in range(self.col)] for i in range(self.row)]
        for b in self.barriers:
            self[b[0]][b[1]] = -1
        self[self.start[0]][self.start[1]] = 1

    def emit(self):
        q = queue.Queue()
        q.put(self.start)
        while not q.empty():
            index = q.get()
            l = (index[0]-1, index[1])
            r = (index[0]+1, index[1])
            u = (index[0], index[1]-1)
            d = (index[0], index[1]+1)

            if l[0] >= 0 and self[l[0]][l[1]] == 0:
                self[l[0]][l[1]] += self[index[0]][index[1]] + 1
                q.put(l)
            if r[0] < self.row and self[r[0]][r[1]] == 0:
                self[r[0]][r[1]] += self[index[0]][index[1]] + 1
                q.put(r)
            if u[1] >= 0 and self[u[0]][u[1]] == 0:
                self[u[0]][u[1]] += self[index[0]][index[1]] + 1
                q.put(u)
            if d[1] < self.col and self[d[0]][d[1]] == 0:
                self[d[0]][d[1]] += self[index[0]][index[1]] + 1
                q.put(d)

    def get_path(self):
        # if self[self.finish[0]][self.finish[1]] == 0 or \
        #         self[self.finish[0]][self.finish[1]] == -1:
        #     raise print("!")

        path = []
        item = self.finish
        while not path.append(item) and item != self.start:
            l = (item[0]-1, item[1])
            if l[0] >= 0 and self[l[0]][l[1]] == self[item[0]][item[1]] - 1:
                item = l
                continue
            r = (item[0]+1, item[1])
            if r[0] < self.col and self[r[0]][r[1]] == self[item[0]][item[1]] - 1:
                item = r
                continue
            u = (item[0], item[1]-1)
            if u[1] >= 0 and self[u[0]][u[1]] == self[item[0]][item[1]] - 1:
                item = u
                continue
            d = (item[0], item[1]+1)
            if d[1] < self.row and self[d[0]][d[1]] == self[item[0]][item[1]] - 1:
                item = d
                continue
        return path

    def update(self):
        self.field = [[0 for i in range(self.col)] for i in range(self.row)]

    def show(self):
        for i in self:
            for j in i:
                print(j)
            print()
