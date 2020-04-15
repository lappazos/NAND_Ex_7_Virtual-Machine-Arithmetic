import os
import sys

import CodeWriter
import Parser

FILE_LOCATION = 1

VM = ".vm"

ASM = ".asm"


def translate_files(file_path):
    """
    handle dir & path
    :param file_path: path of file or dir
    """
    files_list = []
    full_file_path = None
    if os.path.isdir(file_path):
        dir_name = os.path.split(file_path)[1]
        full_file_path = os.path.join(file_path, dir_name + ASM)
        for file in os.listdir(file_path):
            file_explicit_name, file_extension = os.path.splitext(file)
            if file_extension == VM:
                files_list.append(file)
    elif os.path.isfile(file_path):
        file_explicit_name, file_extension = os.path.splitext(file_path)
        if file_extension == VM:
            files_list.append(os.path.split(file_path)[1])
            full_file_path = os.path.join(file_explicit_name+ASM)
    handle_files(files_list, full_file_path)


def handle_files(files_list, full_file_path):
    """
    Main func go over the lines of the files
    :param files_list: list of files in the dir
    :param full_file_path : path to save to
    """
    if full_file_path is None:
        return
    code_writer = CodeWriter.CodeWriter(full_file_path)
    for file_name in files_list:
        parser = Parser.Parser(
            os.path.join(os.path.split(full_file_path)[0], file_name))
        code_writer.set_file_name(file_name.replace(VM, ""))
        while parser.has_more_commands():
            parser.advance()
            command = parser.command_type()
            if command == Parser.C_POP or command == Parser.C_PUSH:
                code_writer.write_push_pop(command, parser.arg1(),
                                           parser.arg2())
            else:
                code_writer.write_arithmetic(parser.arg1())
    code_writer.close()


if __name__ == '__main__':
    filePath = sys.argv[FILE_LOCATION]
    translate_files(filePath)
