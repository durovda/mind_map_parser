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


class Command:
    def __init__(self, index, line, stack, commands, args_list):
        self._index = index
        self._cmd, *self.args = line.split()
        self._stack = stack
        self._commands = commands
        self._args_list = args_list

    def run(self):
        print(self)
        if self._cmd == 'cmpj':
            next_command_index = self._stack.cmpj(self.args[0], self.args[1], self.args[2])
            print('Новый номер команды:', next_command_index)
            self._run_command_by_index(next_command_index)
        else:
            if self._cmd == 'push':
                if self._is_number(self.args[0]):
                    self._stack.push(self.args[0])
                else:
                    self._stack.push(self._args_list[self.args[0]])
            elif self._cmd == 'pop':
                self._args_list[self.args[0]] = self._stack.pop()
                print(self._args_list)
            elif self._cmd == 'add':
                self._stack.add()
            elif self._cmd == 'sub':
                self._stack.sub()
            elif self._cmd == 'mul':
                self._stack.mul()
            elif self._cmd == 'div':
                self._stack.div()
            elif self._cmd == 'print':
                self._stack.print_st()
            elif self._cmd == 'input':
                self._stack.input_st()
            elif self._cmd == 'print_chr':
                self._stack.print_chr()

            self._print_stack_state()
            self._run_next_command()

    def __repr__(self):
        if len(self.args) > 0:
            return f'Команда {self._cmd} и аргументы {self.args}'
        else:
            return f'Команда {self._cmd}'

    def _print_stack_state(self):
        print('Состояние стека: ', self._stack.lst)
        print('-------------------------------------------')

    def _run_next_command(self):
        next_command = self._commands.get(self._index + 1)
        if next_command is not None:
            next_command.run()

    def _run_command_by_index(self, index):
        self._commands.get(index).run()

    @staticmethod
    def _is_number(text):
        try:
            float(text)
            return True
        except ValueError:
            return False


class Application:
    def __init__(self):
        self._commands = dict()
        self._args_list = dict()
        self._stack = Stack()

    def _make_commands(self):
        with open('code.stack', 'r') as f:
            lines = [i.rstrip('\n') for i in f.readlines()]
        index = 0
        for line in lines:
            index += 1
            command = Command(index, line, self._stack, self._commands, self._args_list)
            self._commands[index] = command

    def start(self):
        self._make_commands()
        self._commands[1].run()


Application().start()
