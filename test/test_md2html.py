import subprocess
import os
import sys

# Resolve paths relative to this test file so tests can be run from any
# working directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SCRIPT = os.path.join(BASE_DIR, "..", "md2html.py")
test_cases = [
    ("example.md", "example.html"),
    ("edge_cases.md", "edge_cases.html"),
    ("inline_code_html.md", "inline_code_html.html"),
    ("additional.md", "additional.html"),
]


def run_converter(input_md, output_html):
    input_path = os.path.join(BASE_DIR, input_md)
    output_path = os.path.join(BASE_DIR, output_html)
    with open(output_path, "w", encoding="utf-8", newline="\n") as outfile:
        subprocess.run([sys.executable, SCRIPT, input_path], stdout=outfile, check=True)


def run_converter_stdin(input_md, output_html):
    input_path = os.path.join(BASE_DIR, input_md)
    output_path = os.path.join(BASE_DIR, output_html)
    with open(input_path, "r", encoding="utf-8") as infile, open(
        output_path, "w", encoding="utf-8", newline="\n"
    ) as outfile:
        subprocess.run(
            [sys.executable, SCRIPT], stdin=infile, stdout=outfile, check=True
        )


def run_converter_output_option(input_md, output_path):
    input_path = os.path.join(BASE_DIR, input_md)
    subprocess.run([sys.executable, SCRIPT, input_path, "-o", output_path], check=True)


def test_conversion():
    for md, expected_html in test_cases:
        output_html = "output_" + md.replace(".md", ".html")
        run_converter(md, output_html)
        output_path = os.path.join(BASE_DIR, output_html)
        expected_path = os.path.join(BASE_DIR, expected_html)
        with open(output_path, "rb") as f1, open(expected_path, "rb") as f2:
            got = f1.read().replace(b"\r\n", b"\n")
            exp = f2.read().replace(b"\r\n", b"\n")
        assert got == exp, f"{md}: HTML output does not match expected."
        print(f"Test passed: {md} -> {expected_html}")


def test_stdin_conversion():
    for md, expected_html in test_cases:
        output_html = "output_stdin_" + md.replace(".md", ".html")
        run_converter_stdin(md, output_html)
        output_path = os.path.join(BASE_DIR, output_html)
        expected_path = os.path.join(BASE_DIR, expected_html)
        with open(output_path, "rb") as f1, open(expected_path, "rb") as f2:
            got = f1.read().replace(b"\r\n", b"\n")
            exp = f2.read().replace(b"\r\n", b"\n")
        assert got == exp, f"STDIN: HTML output does not match expected for {md}."
        print(f"Test passed: stdin input: {md} -> {expected_html}")


def test_output_option():
    for md, expected_html in test_cases:
        output_html = "output_option_" + md.replace(".md", ".html")
        output_path = os.path.join(BASE_DIR, output_html)
        run_converter_output_option(md, output_path)
        expected_path = os.path.join(BASE_DIR, expected_html)
        # Normalize line endings before comparison to be cross-platform friendly
        with open(output_path, "rb") as f1, open(expected_path, "rb") as f2:
            got = f1.read().replace(b"\r\n", b"\n")
            exp = f2.read().replace(b"\r\n", b"\n")
        assert got == exp, f"--output: HTML output does not match expected for {md}."
        print(f"Test passed: -o output option: {md} -> {expected_html}")


if __name__ == "__main__":
    test_conversion()
    test_stdin_conversion()
    test_output_option()
