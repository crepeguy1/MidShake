from py_compile import main
import sys

def run_midshake(code):
    variables = {}
    lines = code.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # ignore empty lines and comments
        if not line or line.startswith("^"):
            i += 1
            continue

        # LET the variable X BE the number N;
        if line.startswith("LET the variable"):
            parts = line.split()
            name = parts[3]
            value = int(parts[-1].replace(";", ""))
            variables[name] = value
            i += 1
            continue

        # PROCLAIM the value of X;
        if line.startswith("PROCLAIM the value of"):
            parts = line.split()
            name = parts[-1].replace(";", "")
            if name in variables:
                print(variables[name])
            else:
                print(f"Error: Unknown variable '{name}'")
            i += 1
            continue

        # IF the value of X IS the number N THEN
        if line.startswith("IF the value of"):
            parts = line.split()
            var_name = parts[4]
            expected_value = int(parts[-1])  # last word is the number

            condition = variables.get(var_name, None) == expected_value

            # Move to next line
            i += 1

            # If condition is false, skip until END IF;
            if not condition:
                while i < len(lines) and "END IF;" not in lines[i]:
                    i += 1
                i += 1  # skip END IF;
                continue

            # If condition is true, execute inside block
            i += 0
            continue

        # END IF; (just skip it)
        if line == "END IF;":
            i += 1
            continue

        # unknown command
        print(f"Error: Unknown command -> {line}")
        i += 1


if __name__ == "__main__":
    main()
