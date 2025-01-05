import subprocess
import os
import argparse


def run_test(scheme_file, input_file, output_file, interpreter="src/scheme.py"):
    """
    Run a single Scheme test file and compare its output.

    Args:
        scheme_file (str): Path to the Scheme file to test.
        input_file (str): Path to the input file for the test.
        output_file (str): Path to the expected output file for the test.
        interpreter (str): Path to the Scheme interpreter script.
    """
    with open(input_file, "r") as infile:
        test_input = infile.read()
    with open(output_file, "r") as outfile:
        expected_output = outfile.read()
    
    result = subprocess.run(
        ["python", interpreter, scheme_file],
        input=test_input,
        text=True,
        capture_output=True
    )

    # Compare the result with the expected output
    actual_output = result.stdout.strip()
    expected_output = expected_output.strip()

    if actual_output == expected_output:
        print(f"PASS: {scheme_file}")
        return True
    else:
        print(f"FAIL: {scheme_file}")
        print(f"Expected:\n{expected_output}\n")
        print(f"Got:\n{actual_output}\n")
        return False


def run_all_tests(test_dir, interpreter="src/scheme.py"):
    """
    Run all Scheme tests in the specified directory.

    Args:
        test_dir (str): Path to the directory containing test files.
        interpreter (str): Path to the Scheme interpreter script.
    """
    test_files = [
        f for f in os.listdir(test_dir) if f.endswith(".scm")
    ]
    passed, failed = 0, 0

    for test_file in test_files:
        # Derive corresponding .in and .out file paths
        base_name = os.path.splitext(test_file)[0]
        input_file = os.path.join(test_dir, f"{base_name}.in")
        output_file = os.path.join(test_dir, f"{base_name}.out")
        scheme_file = os.path.join(test_dir, test_file)

        # Run the test
        if os.path.exists(input_file) and os.path.exists(output_file):
            if run_test(scheme_file, input_file, output_file, interpreter):
                passed += 1
            else:
                failed += 1
        else:
            print(f"SKIP: {scheme_file} (missing .in or .out file)")

    print(f"\nSummary: {passed} passed, {failed} failed")


def run_single_test(scheme_file, interpreter="src/scheme.py"):
    """
    Run a single Scheme test file.

    Args:
        scheme_file (str): Path to the Scheme file to test.
        interpreter (str): Path to the Scheme interpreter script.
    """
    base_name = os.path.splitext(os.path.basename(scheme_file))[0]
    test_dir = os.path.dirname(scheme_file)
    input_file = os.path.join(test_dir, f"{base_name}.in")
    output_file = os.path.join(test_dir, f"{base_name}.out")

    if not os.path.exists(input_file) or not os.path.exists(output_file):
        print(f"Missing .in or .out file for {scheme_file}")
        return

    if run_test(scheme_file, input_file, output_file, interpreter):
        print("\nTest Passed!")
    else:
        print("\nTest Failed!")


def main():
    """
    Main function to parse arguments and run tests.
    """
    parser = argparse.ArgumentParser(description="Run Scheme tests")
    parser.add_argument(
        "file", nargs="?", help="Run a specific Scheme test file (.scm)", default=None
    )
    args = parser.parse_args()

    test_dir = "tests/test_files"
    interpreter = "src/scheme.py"

    if args.file:
        run_single_test(args.file, interpreter)
    else:
        run_all_tests(test_dir, interpreter)


if __name__ == "__main__":
    main()
