class Stack:
    def __init__(self):
        self.lst = []
        self.line_input = 1

    def push(self, value):
        self.lst.append(value)

    def pop(self):
        return self.lst.pop()

    def add(self):
        a = self.lst.pop()
        b = self.lst.pop()
        res = int(a) + int(b)
        self.lst.append(str(res))

    def sub(self):
        a = self.lst.pop()
        b = self.lst.pop()
        res = int(a) - int(b)
        self.lst.append(str(res))

    def mul(self):
        a = self.lst.pop()
        b = self.lst.pop()
        res = int(a) * int(b)
        self.lst.append(str(res))

    def div(self):
        a = self.lst.pop()
        b = self.lst.pop()
        res = int(a) // int(b)
        self.lst.append(str(res))

    def print_st(self):
        with open('output.txt', 'a') as f:
            print(str(self.lst[-1]), file=f)

    def input_st(self):
        with open('input.txt', 'r') as f:
            current_line = 1
            for line in f:
                if current_line == self.line_input:
                    self.lst.append(line.rstrip('\n'))
                    break
                current_line += 1
        self.line_input += 1

    def print_chr(self):
        with open('output.txt', 'a') as f:
            print(chr(int(self.lst[-1])), file=f)

    def cmpj(self, index1, index2, index3):
        if self.lst[-1] > self.lst[-2]:
            return int(index1)
        elif self.lst[-1] == self.lst[-2]:
            return int(index2)
        elif self.lst[-1] < self.lst[-2]:
            return int(index3)


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def run(list_command, index):
    for com in list_command[index:]:
        cmd, *arg = com.split()
        print(f'Команда {cmd} и аргумент {arg}')
        if cmd == 'push':
            if is_number(arg[0]):
                box.push(arg[0])
            else:
                box.push(tmp_dict[arg[0]])
        elif cmd == 'pop':
            tmp_dict[arg[0]] = box.pop()
            print(tmp_dict)
        elif cmd == 'add':
            box.add()
        elif cmd == 'sub':
            box.sub()
        elif cmd == 'mul':
            box.mul()
        elif cmd == 'div':
            box.div()
        elif cmd == 'print':
            box.print_st()
        elif cmd == 'input':
            box.input_st()
        elif cmd == 'print_chr':
            box.print_chr()
        elif cmd == 'cmpj':
            print('Новый номер команды:', box.cmpj(arg[0], arg[1], arg[2]))
            run(list_command, box.cmpj(arg[0], arg[1], arg[2]) - 1)
            break
        print('Состояние стека: ', box.lst)
        print('-------------------------------------------')


box = Stack()
tmp_dict = dict()
command_list = []

with open('code.stack', 'r') as f:
    command_list = f.readlines()

command_list = [i.rstrip('\n') for i in command_list]
run(command_list, 0)
