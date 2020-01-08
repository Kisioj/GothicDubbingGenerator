import antlr4

import sys

from grammar.DaedalusLexer import DaedalusLexer
from grammar.DaedalusParser import DaedalusParser
from src_helper import SrcHelper
from syntax_error_listener import SyntaxErrorListener


def parse(path):
    input_stream = antlr4.FileStream(path, encoding='windows-1250')
    lexer = DaedalusLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = DaedalusParser(token_stream)

    listener = SyntaxErrorListener()
    parser.addErrorListener(listener)
    parser.daedalusFile()
    if listener.errors_count:
        msg = f"{listener.errors_count} syntax error generated"
        print(msg, file=sys.stderr)
        return


def main():
    _, src_path = sys.argv

    src_helper = SrcHelper(src_path)
    files_paths = src_helper.get_daedalus_files()
    for i, file_path in enumerate(files_paths):
        print(f'\r{i}/{len(files_paths)} {file_path}')
        parse(file_path)


if __name__ == '__main__':
    main()
