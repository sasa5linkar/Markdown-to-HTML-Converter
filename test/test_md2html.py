import subprocess
import os
import filecmp

# Resolve paths relative to this test file so tests can be run from any
# working directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SCRIPT = os.path.join(BASE_DIR, '..', 'md2html.py')
test_cases = [
    ('example.md', 'example.html'),
    ('edge_cases.md', 'edge_cases.html'),
    ('inline_code_html.md', 'inline_code_html.html'),
]

def run_converter(input_md, output_html):
    input_path = os.path.join(BASE_DIR, input_md)
    output_path = os.path.join(BASE_DIR, output_html)
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        subprocess.run(['python', SCRIPT, input_path], stdout=outfile, check=True)

def test_conversion():
    for md, expected_html in test_cases:
        output_html = 'output_' + md.replace('.md', '.html')
        run_converter(md, output_html)
        output_path = os.path.join(BASE_DIR, output_html)
        expected_path = os.path.join(BASE_DIR, expected_html)
        assert filecmp.cmp(output_path, expected_path, shallow=False), f'{md}: HTML output does not match expected.'
        print(f'Test passed: {md} -> {expected_html}')

if __name__ == '__main__':
    test_conversion()
