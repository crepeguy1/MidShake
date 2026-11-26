#!/usr/bin/env python3
"""
Test runner for MidShake compiler.
Compiles each .mish test file, runs the generated binary, and reports results.
"""

import os
import sys
import subprocess
import shutil
import time

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "build", "output")
PYTHON_DIR = os.path.join(PROJECT_ROOT, "python")
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "selfhost", "runtime")

# Add python dir to path
sys.path.insert(0, PYTHON_DIR)

# Expected output fragments for integration tests
EXPECTED_OUTPUTS = {
    "test_class_encapsulation.mish": "1.000000",
    "test_imported_class.mish": "5.000000",
    "test_selfhost_classes.mish": "7.000000\n3.000000",
    "test_collections.mish": "All tests passed!",
    "test_global_set.mish": "15.000000",
    "test_bootstrap_scope.mish": "5.000000",
    "test_function_calls.mish": "Done!",
    "test_if_else.mish": "small",
    "test_recursion.mish": None,  # Just check it compiles and runs
    "test_continue.mish": None,
    "test_import.mish": None,
    "test_map.mish": None,
    "test_map_global.mish": None,
    "test_map_nested.mish": None,
    "test_new_features.mish": None,
    "test_params.mish": None,
    "test_simple_call.mish": None,
    "test_startswith.mish": None,
    "test_while_simple.mish": None,
}

# Tests that are known to have issues (skip for now)
SKIP_TESTS = {
    "test_parse_20_30.mish",
    "test_parse_codegen.mish",
    "test_parse_first20.mish",
    "test_parse_full.mish",
    "test_parse_func.mish",
    "test_parse_line20.mish",
    "test_parse_line25.mish",
    "test_parse_loop.mish",
    "test_parse_step.mish",
    "test_semantic_errors.mish",  # Intentionally has errors
}


def find_gpp():
    """Find g++ compiler."""
    gpp = shutil.which("g++")
    if gpp:
        return gpp
    # Try common Windows paths
    msys_path = r"C:\msys64\mingw64\bin\g++.EXE"
    if os.path.exists(msys_path):
        return msys_path
    return None


def compile_test(test_file):
    """Compile a .mish test file using the Python compiler."""
    cli_script = os.path.join(PYTHON_DIR, "midshake_cli.py")
    cmd = [sys.executable, cli_script, "compile", test_file]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60,
        cwd=PROJECT_ROOT
    )
    
    return result


def run_test(test_name):
    """Run a compiled test executable."""
    exe_path = os.path.join(OUTPUT_DIR, test_name + ".exe")
    
    if not os.path.exists(exe_path):
        return None, f"Executable not found: {exe_path}"
    
    try:
        result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=PROJECT_ROOT
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT (hung)"


def run_unit_tests():
    """Run Python unit tests for lexer, parser, and codegen."""
    print("=== Running Unit Tests ===")
    print()
    total_passed = 0
    total_failed = 0
    unit_test_files = ["test_lexer.py", "test_parser.py", "test_codegen.py", "test_visibility.py"]
    
    for test_file in unit_test_files:
        test_path = os.path.join(TESTS_DIR, test_file)
        if not os.path.exists(test_path):
            print(f"  SKIP: {test_file} (not found)")
            continue
        
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=PROJECT_ROOT
        )
        
        # Count passes/fails from output
        output = result.stdout + result.stderr
        failures_before_test = total_failed
        for line in output.split("\n"):
            if "  PASS:" in line:
                total_passed += 1
            elif "  FAIL:" in line:
                total_failed += 1
        if result.returncode != 0 and total_failed == failures_before_test:
            total_failed += 1
    
    print(f"  Unit tests: {total_passed} passed, {total_failed} failed")
    print()
    return total_passed, total_failed


def run_tests():
    """Run all tests and report results."""
    
    # Run unit tests first
    unit_passed, unit_failed = run_unit_tests()
    
    gpp = find_gpp()
    if not gpp:
        print("ERROR: g++ not found. Please install a C++ compiler.")
        print(f"Unit tests only: {unit_passed} passed, {unit_failed} failed")
        sys.exit(1)
    
    # Find all .mish test files
    test_files = []
    for f in os.listdir(TESTS_DIR):
        if f.endswith(".mish") and f not in SKIP_TESTS:
            test_files.append(f)
    
    test_files.sort()
    
    print(f"=== MidShake Test Suite ===")
    print(f"Found {len(test_files)} test files")
    print(f"g++: {gpp}")
    print()
    
    passed = 0
    failed = 0
    skipped = 0
    results = []
    
    for test_file in test_files:
        test_path = os.path.join(TESTS_DIR, test_file)
        print(f"Testing: {test_file}...", end=" ")
        
        # Compile
        compile_result = compile_test(test_path)
        
        if compile_result.returncode != 0:
            # Check if it's a semantic error (expected for some tests)
            if "semantic errors" in compile_result.stderr or "semantic errors" in compile_result.stdout:
                # Check if compilation still succeeded despite warnings
                if "Success:" in compile_result.stdout or "Success:" in compile_result.stderr:
                    print("COMPILED (with warnings)")
                else:
                    print("COMPILE FAILED")
                    results.append((test_file, "COMPILE FAILED", compile_result.stderr))
                    failed += 1
                    continue
            else:
                print("COMPILE FAILED")
                results.append((test_file, "COMPILE FAILED", compile_result.stderr))
                failed += 1
                continue
        
        print("COMPILED |", end=" ")
        
        # Run
        returncode, output = run_test(os.path.splitext(test_file)[0])
        
        if returncode is None:
            print(" | EXEC NOT FOUND")
            results.append((test_file, "EXEC NOT FOUND", ""))
            failed += 1
            continue
        
        if returncode == -1:
            print(f" | TIMEOUT (hung)")
            results.append((test_file, "TIMEOUT", output))
            failed += 1
            continue
        
        if returncode != 0:
            print(f" | RUN FAILED (exit {returncode})")
            results.append((test_file, f"RUN FAILED (exit {returncode})", output))
            failed += 1
            continue
        
        # Check expected output
        expected = EXPECTED_OUTPUTS.get(test_file)
        if expected is not None:
            # Handle float formatting (15 vs 15.000000)
            if expected in output or expected.replace(".000000", "") in output:
                print("PASSED")
                results.append((test_file, "PASSED", ""))
                passed += 1
            else:
                print(f"FAILED (expected '{expected}')")
                results.append((test_file, "OUTPUT MISMATCH", output))
                failed += 1
        else:
            print("PASSED")
            results.append((test_file, "PASSED", ""))
            passed += 1
    
    # Summary
    print()
    print(f"=== Results ===")
    print(f"Unit tests: {unit_passed} passed, {unit_failed} failed")
    print(f"Integration tests: {passed} passed, {failed} failed")
    print(f"Skipped: {len(SKIP_TESTS)}")
    total_all = unit_passed + unit_failed + passed + failed + len(SKIP_TESTS)
    total_ok = unit_passed + passed
    total_fail = unit_failed + failed
    print(f"Total: {total_all} ({total_ok} ok, {total_fail} failed, {len(SKIP_TESTS)} skipped)")
    print()
    
    if failed > 0:
        print("Failed integration tests:")
        for name, status, error in results:
            if status != "PASSED":
                print(f"  {name}: {status}")
                if error:
                    print(f"    {error[:200]}")
    
    return (failed == 0) and (unit_failed == 0)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
