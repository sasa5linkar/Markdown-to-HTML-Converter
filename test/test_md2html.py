import subprocess
import os
import filecmp

# Paths
script = os.path.join('..', 'md2html.py')
test_cases = [
    ('example.md', 'example.html'),
    ('edge_cases.md', 'edge_cases.html'),
]

def run_converter(input_md, output_html):
    with open(input_md, 'r', encoding='utf-8') as infile, open(output_html, 'w', encoding='utf-8') as outfile:
        subprocess.run(['python', script, input_md], stdout=outfile, check=True)

def test_conversion():
    for md, expected_html in test_cases:
        output_html = 'output_' + md.replace('.md', '.html')
        run_converter(md, output_html)
        assert filecmp.cmp(output_html, expected_html, shallow=False), f'{md}: HTML output does not match expected.'
        print(f'Test passed: {md} -> {expected_html}')

if __name__ == '__main__':
    test_conversion()
