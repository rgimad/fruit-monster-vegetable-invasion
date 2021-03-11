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
        self.path = None
        self.field = None
        self.build()

    def build(self):
        self.field = [[0 for i in range(self.col)] for i in range(self.row)]
        for b in self.barriers:
            self.field[b[0]][b[1]] = -1
        self.field[self.start[0]][self.start[1]] = 1

    def emit(self):
        q = queue.Queue()
        q.put(self.start)
        while not q.empty():
            index = q.get()
            u = (index[0]-1, index[1])
            d = (index[0]+1, index[1])
            l = (index[0], index[1]-1)
            r = (index[0], index[1]+1)

            if l[1] >= 0 and self.field[l[0]][l[1]] == 0:
                self.field[l[0]][l[1]] += self.field[index[0]][index[1]] + 1
                q.put(l)
            if r[1] < self.col and self.field[r[0]][r[1]] == 0:
                self.field[r[0]][r[1]] += self.field[index[0]][index[1]] + 1
                q.put(r)
            if u[0] >= 0 and self.field[u[0]][u[1]] == 0:
                self.field[u[0]][u[1]] += self.field[index[0]][index[1]] + 1
                q.put(u)
            if d[0] < self.row and self.field[d[0]][d[1]] == 0:
                self.field[d[0]][d[1]] += self.field[index[0]][index[1]] + 1
                q.put(d)

    def get_path(self):
        if self.field[self.finish[0]][self.finish[1]] == 0 or \
                self.field[self.finish[0]][self.finish[1]] == -1:
            raise print("!")

        path = []
        item = self.finish
        while not path.append(item) and item != self.start:
            l = (item[0], item[1] - 1)
            if l[1] >= 0 and self.field[l[0]][l[1]] == self.field[item[0]][item[1]] - 1:
                item = l
                continue
            r = (item[0], item[1] + 1)
            if r[1] < self.col and self.field[r[0]][r[1]] == self.field[item[0]][item[1]] - 1:
                item = r
                continue
            u = (item[0] - 1, item[1])
            if u[0] >= 0 and self.field[u[0]][u[1]] == self.field[item[0]][item[1]] - 1:
                item = u
                continue
            d = (item[0] + 1, item[1])
            if d[0] < self.row and self.field[d[0]][d[1]] == self.field[item[0]][item[1]] - 1:
                item = d
                continue
        self.path = path
        return path

    def update(self):
        self.field = [[0 for i in range(self.col)] for i in range(self.row)]

    def show(self):
        f = open("map11.txt", "w")
        field2 = [[0 for i in range(self.col)] for i in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                # field2[i][j] = self.field[i][j]
                if self.field[i][j] == -1:
                    field2[i][j] = 2
                else:
                    field2[i][j] = 0
        for x in self.path:
            f.write("({}, {}), ".format(x[0], x[1]))
            field2[x[0]][x[1]] = 1
        f.write("\n")
        for i in range(self.row):
            for j in range(self.col):
                f.write(str(field2[i][j]))
            f.write("\n")
        f.write(str(self.barriers))
        f.write("\n" + str(self.field[self.start[0]][self.start[1]]) + \
            " " + str(self.field[self.finish[0]][self.finish[1]]) + \
            " " + str(self.row) + " " + str(self.col))
        f.close()
        