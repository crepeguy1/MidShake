#!/usr/bin/env python3
"""Build and verify MidShake's self-hosted compiler bootstrap chain."""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT / "python"
RUNTIME_DIR = ROOT / "selfhost" / "runtime"
BUILD_DIR = ROOT / "build" / "bootstrap"
OUTPUT_DIR = ROOT / "build" / "output"
SOURCE = ROOT / "selfhost" / "codegen.mish"
PARSER_SOURCE = ROOT / "selfhost" / "parser.mish"
SMOKE_TEST = ROOT / "tests" / "test_bootstrap_scope.mish"
CLASS_TEST = ROOT / "tests" / "test_selfhost_classes.mish"
EXCEPTION_TEST = ROOT / "tests" / "test_exception_handling.mish"
UNCAUGHT_EXCEPTION_TEST = ROOT / "tests" / "test_exception_uncaught.mish"
PRIVATE_MODULE_OK_TEST = ROOT / "selfhost" / "fixtures" / "private_module_ok.mish"
PRIVATE_MODULE_DENIED_TEST = ROOT / "selfhost" / "fixtures" / "private_module_denied.mish"
PRIVATE_MODULE_FUNCTION_DENIED_TEST = ROOT / "selfhost" / "fixtures" / "private_module_function_denied.mish"
PRIVATE_MODULE_CLASS_DENIED_TEST = ROOT / "selfhost" / "fixtures" / "private_module_class_denied.mish"
PRIVATE_MODULE_WRITE_DENIED_TEST = ROOT / "selfhost" / "fixtures" / "private_module_write_denied.mish"
PRIVATE_MODULE_GLOBAL_DENIED_TEST = ROOT / "selfhost" / "fixtures" / "private_module_global_denied.mish"

sys.path.insert(0, str(PYTHON_DIR))

from midshake_compiler import CppCompiler
from midshake_parser import Parser
from midshake_tokenizer import Tokenizer


def find_gpp():
    compiler = shutil.which("g++")
    if compiler:
        return compiler
    windows_compiler = Path(r"C:\msys64\mingw64\bin\g++.EXE")
    return str(windows_compiler) if windows_compiler.is_file() else None


def run_checked(command, cwd, label, timeout=180):
    try:
        result = subprocess.run(
            [str(part) for part in command],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        errors = error.stderr or ""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        if isinstance(errors, bytes):
            errors = errors.decode(errors="replace")
        details = (output + errors)[-12000:]
        raise RuntimeError(
            f"{label} timed out after {timeout} seconds:\n{details}"
        ) from error

    if result.returncode != 0:
        details = result.stdout + result.stderr
        raise RuntimeError(f"{label} failed (exit {result.returncode}):\n{details}")
    return result


def compile_native(gpp, cpp_file, executable):
    command = [
        gpp,
        "-std=c++17",
        "-I" + str(RUNTIME_DIR),
        cpp_file,
        RUNTIME_DIR / "midshake_runtime.cpp",
    ]
    if os.name == "nt":
        command.append("-Wl,--stack,8388608")
    command.extend(["-o", executable])
    run_checked(
        command,
        ROOT,
        f"Compiling {cpp_file.name}",
    )


def numeric_output(output, label):
    try:
        return [float(line.strip()) for line in output.splitlines() if line.strip()]
    except ValueError as error:
        raise RuntimeError(f"{label} produced non-numeric output:\n{output}") from error


def compile_with_python(cpp_file, executable):
    source = SOURCE.read_text(encoding="utf-8")
    program = Parser(Tokenizer(source).tokenize()).parse()
    cpp_file.parent.mkdir(parents=True, exist_ok=True)
    cpp_file.write_text(CppCompiler().compile_program(program), encoding="utf-8")
    compile_native(GPP, cpp_file, executable)


def run_self_hosted(executable, source, work_dir, timeout=180):
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "output").mkdir(exist_ok=True)
    result = run_checked(
        [executable, source],
        ROOT,
        f"Running {executable.name} on {source.name}",
        timeout=timeout,
    )
    generated = OUTPUT_DIR / "generated.cpp"
    if not generated.is_file():
        raise RuntimeError(f"{executable.name} did not create {generated}")
    staged = work_dir / "output" / "generated.cpp"
    shutil.copy2(generated, staged)
    return staged, result.stdout


def verify_imported_private_denial(stage2_exe, source, label, expected_message):
    work_dir = BUILD_DIR / f"{label}-run"
    generated_cpp, _ = run_self_hosted(stage2_exe, source, work_dir)
    generated_source = generated_cpp.read_text(encoding="utf-8")
    if expected_message not in generated_source:
        raise RuntimeError(f"Self-hosted generation omitted the {label} access check.")

    extension = ".exe" if os.name == "nt" else ""
    native_exe = BUILD_DIR / (label + extension)
    compile_native(GPP, generated_cpp, native_exe)
    native_result = subprocess.run(
        [str(native_exe)], cwd=str(ROOT), capture_output=True, text=True, timeout=30
    )
    if native_result.returncode == 0 or "MidShake Access Error" not in (
        native_result.stdout + native_result.stderr
    ):
        raise RuntimeError(f"Native {label} access was not denied at runtime.")

    interpreted_result = subprocess.run(
        [sys.executable, ROOT / "python" / "midshake_cli.py", "run", source],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if interpreted_result.returncode == 0 or "MidShake Access Error" not in (
        interpreted_result.stdout + interpreted_result.stderr
    ):
        raise RuntimeError(f"Interpreter {label} access was not denied at runtime.")


def phase_log(output):
    markers = (
        "Compiling:",
        "EXPAND ENTER",
        "EXPAND EXIT",
        "PARSING DONE",
        "CLASSIFICATION DONE",
        "FUNCTIONS DONE",
        "MAIN DONE",
        "AST SIZE",
        "FUNCTION COUNT",
        "MAIN COUNT",
        "PARSE POS",
        "EXPANDED SOURCE LENGTH",
        "PARSED LINE COUNT",
        "G LINE COUNT",
        "EXPANDED LIST SIZE",
        "JOINED SOURCE LENGTH",
        "Generated C++ code written",
        "Compilation complete!",
        "stdlib/stdlib.mish",
        "selfhost/parser.mish",
    )
    selected = []
    include_next = False
    for line in output.splitlines():
        if include_next:
            selected.append(line)
            include_next = False
        if any(marker in line for marker in markers):
            selected.append(line)
            include_next = True
    return "\n".join(selected)


def main():
    global BUILD_DIR, GPP
    GPP = find_gpp()
    if not GPP:
        raise RuntimeError("g++ was not found; install GCC/MinGW and add it to PATH")

    os.chdir(ROOT)
    extension = ".exe" if os.name == "nt" else ""
    BUILD_DIR = BUILD_DIR / str(time.time_ns())
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stage0_cpp = BUILD_DIR / "stage0.cpp"
    stage0_exe = BUILD_DIR / ("stage0" + extension)
    stage1_exe = BUILD_DIR / ("stage1" + extension)
    stage2_exe = BUILD_DIR / ("stage2" + extension)

    print("[1/8] Building the seed compiler with the Python compiler")
    compile_with_python(stage0_cpp, stage0_exe)

    print("[2/8] Compiling the self-hosted compiler with the seed")
    stage1_cpp, _ = run_self_hosted(stage0_exe, SOURCE, BUILD_DIR / "stage0-run")
    compile_native(GPP, stage1_cpp, stage1_exe)

    print("[3/8] Recompiling and comparing the native generations")
    stage2_cpp, stage1_output = run_self_hosted(
        stage1_exe, SOURCE, BUILD_DIR / "stage1-run", timeout=180
    )
    first = stage1_cpp.read_text(encoding="utf-8").splitlines()
    second = stage2_cpp.read_text(encoding="utf-8").splitlines()
    if first != second:
        first_mismatch = next(
            (index for index, pair in enumerate(zip(first, second), start=1) if pair[0] != pair[1]),
            min(len(first), len(second)) + 1,
        )
        start = max(0, first_mismatch - 4)
        end = min(len(first), first_mismatch + 3)
        mismatch_context = "\n".join(
            f"{line_number + 1}: stage1={first[line_number]!r} | stage2={second[line_number]!r}"
            for line_number in range(start, end)
        )
        raise RuntimeError(
            f"Bootstrap generations differ at line {first_mismatch} "
            f"(stage 1: {len(first)} lines, stage 2: {len(second)} lines).\n"
            + mismatch_context
            + "\nStage 1 phases:\n"
            + phase_log(stage1_output)
        )
    compile_native(GPP, stage2_cpp, stage2_exe)

    print("[4/8] Compiling parser.mish with both native generations")
    parser_stage1_cpp, _ = run_self_hosted(
        stage1_exe, PARSER_SOURCE, BUILD_DIR / "parser-stage1-run"
    )
    parser_stage2_cpp, _ = run_self_hosted(
        stage2_exe, PARSER_SOURCE, BUILD_DIR / "parser-stage2-run"
    )
    if parser_stage1_cpp.read_text(encoding="utf-8") != parser_stage2_cpp.read_text(encoding="utf-8"):
        raise RuntimeError("Native compiler generations produced different C++ for parser.mish.")
    parser_exe = BUILD_DIR / ("parser" + extension)
    compile_native(GPP, parser_stage2_cpp, parser_exe)
    run_checked(
        [parser_exe], BUILD_DIR / "parser-stage2-run", "Running compiled parser module"
    )

    print("[5/8] Verifying recursion, local frames, and global updates")
    smoke_cpp, _ = run_self_hosted(stage2_exe, SMOKE_TEST, BUILD_DIR / "smoke-run")
    smoke_exe = BUILD_DIR / ("smoke" + extension)
    compile_native(GPP, smoke_cpp, smoke_exe)
    result = run_checked([smoke_exe], BUILD_DIR / "smoke-run", "Running bootstrap smoke test")
    native_values = numeric_output(result.stdout, "Native bootstrap smoke test")
    interpreted = run_checked(
        [sys.executable, ROOT / "python" / "midshake_cli.py", "run", SMOKE_TEST],
        ROOT,
        "Running interpreter smoke test",
    )
    interpreted_values = numeric_output(interpreted.stdout, "Interpreter smoke test")
    expected_values = [120.0, 5.0]
    if native_values != expected_values or interpreted_values != expected_values:
        raise RuntimeError(
            "Scope smoke test output mismatch. "
            f"Native: {native_values}; interpreter: {interpreted_values}; "
            f"expected: {expected_values}."
        )

    print("[6/8] Verifying self-hosted class construction and member access")
    class_cpp, _ = run_self_hosted(stage2_exe, CLASS_TEST, BUILD_DIR / "class-run")
    generated_class_source = class_cpp.read_text(encoding="utf-8")
    private_method_registration = (
        'register_class_method("SpecialCounter", "internalTally", AccessLevel::Private,'
    )
    if private_method_registration not in generated_class_source:
        raise RuntimeError("An unmodified class method was not emitted as Private.")
    class_exe = BUILD_DIR / ("classes" + extension)
    compile_native(GPP, class_cpp, class_exe)
    class_result = run_checked(
        [class_exe], BUILD_DIR / "class-run", "Running self-hosted class test"
    )
    native_class_values = numeric_output(class_result.stdout, "Native class test")
    interpreted_class = run_checked(
        [sys.executable, ROOT / "python" / "midshake_cli.py", "run", CLASS_TEST],
        ROOT,
        "Running interpreter class test",
    )
    interpreted_class_values = numeric_output(interpreted_class.stdout, "Interpreter class test")
    expected_class_values = [7.0, 3.0]
    if native_class_values != expected_class_values or interpreted_class_values != expected_class_values:
        raise RuntimeError(
            "Class test output mismatch. "
            f"Native: {native_class_values}; interpreter: {interpreted_class_values}; "
            f"expected: {expected_class_values}."
        )

    print("[7/8] Verifying imported module privacy")
    private_ok_cpp, _ = run_self_hosted(
        stage2_exe, PRIVATE_MODULE_OK_TEST, BUILD_DIR / "private-module-ok-run"
    )
    private_ok_exe = BUILD_DIR / ("private-module-ok" + extension)
    compile_native(GPP, private_ok_cpp, private_ok_exe)
    private_ok_result = run_checked(
        [private_ok_exe],
        ROOT,
        "Running self-hosted imported-private module test",
    )
    interpreted_private_ok = run_checked(
        [sys.executable, ROOT / "python" / "midshake_cli.py", "run", PRIVATE_MODULE_OK_TEST],
        ROOT,
        "Running interpreted imported-private module test",
    )
    expected_private_values = [42.0, 7.0, 8.0]
    if numeric_output(private_ok_result.stdout, "Native imported-private module test") != expected_private_values:
        raise RuntimeError("Native imported-private module returned an unexpected value.")
    if numeric_output(interpreted_private_ok.stdout, "Interpreted imported-private module test") != expected_private_values:
        raise RuntimeError("Interpreted imported-private module returned an unexpected value.")

    private_denied_cpp, _ = run_self_hosted(
        stage2_exe, PRIVATE_MODULE_DENIED_TEST, BUILD_DIR / "private-module-denied-run"
    )
    private_denied_source = private_denied_cpp.read_text(encoding="utf-8")
    denied_symbols = (
        "Variable 'secretValue' is Private in an imported file.",
        "Function 'getSecretValue' is Private in an imported file.",
        "Class 'HiddenCounter' is Private in an imported file.",
    )
    if any(message not in private_denied_source for message in denied_symbols):
        raise RuntimeError("Self-hosted code generation omitted an imported-private access check.")
    for source, label, expected_message in (
        (
            PRIVATE_MODULE_DENIED_TEST,
            "private-module-variable-denied",
            "Variable 'secretValue' is Private in an imported file.",
        ),
        (
            PRIVATE_MODULE_FUNCTION_DENIED_TEST,
            "private-module-function-denied",
            "Function 'getSecretValue' is Private in an imported file.",
        ),
        (
            PRIVATE_MODULE_CLASS_DENIED_TEST,
            "private-module-class-denied",
            "Class 'HiddenCounter' is Private in an imported file.",
        ),
        (
            PRIVATE_MODULE_WRITE_DENIED_TEST,
            "private-module-write-denied",
            "Variable 'secretValue' is Private in an imported file.",
        ),
        (
            PRIVATE_MODULE_GLOBAL_DENIED_TEST,
            "private-module-global-denied",
            "Variable 'secretValue' is Private in an imported file.",
        ),
    ):
        verify_imported_private_denial(stage2_exe, source, label, expected_message)

    print("[8/8] Verifying thrown-value propagation and uncaught diagnostics")
    exception_stage1_cpp, _ = run_self_hosted(
        stage1_exe, EXCEPTION_TEST, BUILD_DIR / "exception-stage1-run"
    )
    exception_stage2_cpp, _ = run_self_hosted(
        stage2_exe, EXCEPTION_TEST, BUILD_DIR / "exception-stage2-run"
    )
    if exception_stage1_cpp.read_text(encoding="utf-8") != exception_stage2_cpp.read_text(encoding="utf-8"):
        raise RuntimeError("Native compiler generations produced different C++ for exception handling.")

    exception_exe = BUILD_DIR / ("exceptions" + extension)
    compile_native(GPP, exception_stage2_cpp, exception_exe)
    native_exception = run_checked(
        [exception_exe], ROOT, "Running native exception test"
    )
    interpreted_exception = run_checked(
        [sys.executable, ROOT / "python" / "midshake_cli.py", "run", EXCEPTION_TEST],
        ROOT,
        "Running interpreter exception test",
    )
    expected_exception_output = ["caught across a function call", "execution continued"]
    if native_exception.stdout.splitlines() != expected_exception_output:
        raise RuntimeError("Native exception test did not catch and continue as expected.")
    if interpreted_exception.stdout.splitlines() != expected_exception_output:
        raise RuntimeError("Interpreter exception test did not catch and continue as expected.")

    uncaught_cpp, _ = run_self_hosted(
        stage2_exe, UNCAUGHT_EXCEPTION_TEST, BUILD_DIR / "uncaught-exception-run"
    )
    uncaught_exe = BUILD_DIR / ("uncaught-exception" + extension)
    compile_native(GPP, uncaught_cpp, uncaught_exe)
    native_uncaught = subprocess.run(
        [str(uncaught_exe)], cwd=str(ROOT), capture_output=True, text=True, timeout=30
    )
    uncaught_message = "Uncaught MidShake exception: uncaught payload"
    if native_uncaught.returncode == 0 or uncaught_message not in (
        native_uncaught.stdout + native_uncaught.stderr
    ):
        raise RuntimeError("Native uncaught throw did not produce the expected diagnostic.")
    interpreted_uncaught = subprocess.run(
        [sys.executable, ROOT / "python" / "midshake_cli.py", "run", UNCAUGHT_EXCEPTION_TEST],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if interpreted_uncaught.returncode == 0 or uncaught_message not in (
        interpreted_uncaught.stdout + interpreted_uncaught.stderr
    ):
        raise RuntimeError("Interpreter uncaught throw did not produce the expected diagnostic.")

    print("Bootstrap verified: generations, parser, scope, classes, module privacy, and exceptions passed.")
    print(f"Artifacts: {BUILD_DIR}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print(f"Bootstrap failed: {error}", file=sys.stderr)
        sys.exit(1)