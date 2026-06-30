from midshake_tokenizer import Tokenizer
from midshake_parser import Parser
from midshake_compiler import CppCompiler
import os

def main():
    try:
        # 1. Read MidShake source
        file_name = input("Enter .ms file name (without extension): ").strip().strip(".")
        file_extension = input("Choose file extension: ")
        if not file_name:
            raise ValueError("File name cannot be empty.")

        ms_path = os.path.join("examples", f"{file_name}.ms")
        if not os.path.isfile(ms_path):
            raise FileNotFoundError(f"Source file not found: {ms_path}")

        with open(ms_path, "r", encoding="utf-8") as f:
            source = f.read()

        # 2. Tokenize
        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()

        # 3. Parse tokens into AST
        parser = Parser(tokens)
        program = parser.parse()

        # 4. Compile AST → C++
        compiler = CppCompiler()
        cpp_code = compiler.compile_program(program)

        # 5. Write generated C++ file
        cpp_dir = "cpp"
        os.makedirs(cpp_dir, exist_ok=True)
        cpp_path = os.path.join(cpp_dir, f"{file_name}."f"{file_extension}")

        with open(cpp_path, "w", encoding="utf-8") as f:
            f.write(cpp_code)

        print(f"Compilation successful! C++ code saved to: {cpp_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()