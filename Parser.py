import re

COMMAND = 0

ARG_1 = 1

ARITHMETIC_CMD = 0

ARG_2 = 2

EMPTY_STRING = ''

SPACE = " "
C_PUSH = 'push'
C_POP = 'pop'
C_RETURN = 'return'
C_LABEL = 'label'
C_IF = 'if-goto'
C_GOTO = 'goto'
C_ARITHMETIC = 0
C_FUNCTION = 'function'
ADD = 'add'
SUB = 'sub'
NEG = 'neg'
EQ = 'eq'
GT = 'gt'
LT = 'lt'
AND = 'and'
OR = 'or'
NOT = 'not'
C_CALL = 0
commands_dict = {C_PUSH: C_PUSH, C_POP: C_POP, ADD: C_ARITHMETIC, SUB: C_ARITHMETIC, NEG: C_ARITHMETIC,
                 EQ: C_ARITHMETIC, GT: C_ARITHMETIC, LT: C_ARITHMETIC, AND: C_ARITHMETIC, OR: C_ARITHMETIC,
                 NOT: C_ARITHMETIC}

commentPat = re.compile('^[^/]*')


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the input code. It reads VM commands,
    parses them, and provides convenient access to their components. In addition, it removes all white space and
    comments.
    """

    def __init__(self, file_path):
        """
        Constructor - Opens the input file/stream and gets ready to parse it.
        :param file_path: Input file / stream
        """
        self.file = open(file_path, 'r')
        self._vm_code = self.file.readlines()
        self._vm_code = self.clean_lines(self._vm_code)
        self._curr_index = 0
        self._length = len(self._vm_code)
        self._curr_command = None
        self._curr_command_parts = None

    def has_more_commands(self):
        """
        Are there more commands in the input?
        :return: boolean
        """
        return self._curr_index <= (self._length - 1)

    def advance(self):
        """
        Reads the next command from the input and makes it the current command. Should be called only if hasMoreCommands
        is true. Initially there is no current command.
        """
        self._curr_command = self._vm_code[self._curr_index]
        self._curr_command_parts = self._curr_command.split(SPACE)
        self._curr_index += 1

    def command_type(self):
        """
        Returns the type of the current VM command. C_ARITHMETIC is returned for all the arithmetic commands
        :return: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
        """
        return commands_dict[self._curr_command_parts[COMMAND]]

    def arg1(self):
        """
        Returns the first arg. of the current command. In the case of C_ARITHMETIC, the command itself
        (add, sub, etc.) is returned. Should not be called if the current command is C_RETURN.
        :return: string
        """
        if self.command_type() == C_ARITHMETIC:
            return self._curr_command_parts[ARITHMETIC_CMD]
        return self._curr_command_parts[ARG_1]

    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current
        command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
        :return: int
        """
        return self._curr_command_parts[ARG_2]

    @staticmethod
    def clean_lines(file):
        """
        get an array of lines and clear the whitespaces and comments
        :param file: vm lines array
        :return: cleaned vm lines array
        """
        lines = []
        for line in file:
            # check if start with a comment
            line = re.sub(r'\s+', SPACE, line)
            match = commentPat.match(line)
            line = match.group(0)
            if line == SPACE or line == EMPTY_STRING:
                continue
            lines.append(line.lower())
        return lines
