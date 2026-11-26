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
SMOKE_TEST = ROOT / "tests" / "test_bootstrap_scope.mish"

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
    run_checked(
        [
            gpp,
            "-std=c++17",
            "-I" + str(RUNTIME_DIR),
            cpp_file,
            RUNTIME_DIR / "midshake_runtime.cpp",
            "-o",
            executable,
        ],
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

    print("[1/4] Building the seed compiler with the Python compiler")
    compile_with_python(stage0_cpp, stage0_exe)

    print("[2/4] Compiling the self-hosted compiler with the seed")
    stage1_cpp, _ = run_self_hosted(stage0_exe, SOURCE, BUILD_DIR / "stage0-run")
    compile_native(GPP, stage1_cpp, stage1_exe)

    print("[3/4] Recompiling and comparing the native generations")
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

    print("[4/4] Verifying recursion, local frames, and global updates")
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

    print("Bootstrap verified: two native generations match and the smoke test passed.")
    print(f"Artifacts: {BUILD_DIR}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print(f"Bootstrap failed: {error}", file=sys.stderr)
        sys.exit(1)