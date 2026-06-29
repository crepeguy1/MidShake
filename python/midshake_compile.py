from midshake_parser import parse
from midshake_compiler import CppCompiler

source = open("examples/full.ms").read()
program = parse(source)

compiler = CppCompiler()
cpp_code = compiler.compile_program(program)

open("cpp/full.cpp", "w").write(cpp_code)
