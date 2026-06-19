import sys

def run_midshake(code):
    for line in code.splitlines():
        line = line.strip()

        # ignore empty lines and comments
        if not line or line.startswith("^"):
            continue

        # print command
        if line.startswith("print "):
            text = line[6:].strip()
            print(text)
            continue

        # unknown command
        print(f"Error: Unknown command -> {line}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python midshake.py <file.ms>")
        return

    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()

    run_midshake(code)

if __name__ == "__main__":
    main()
