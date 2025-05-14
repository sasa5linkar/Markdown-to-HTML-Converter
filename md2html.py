"""
md2html.py: Markdown to HTML Converter

Converts a Markdown (.md) file to a basic HTML file supporting core Markdown features.

Usage:
    python md2html.py input.md > output.html

Requirements:
- Headings (# to ######)
- Bold (**bold**)
- Italic (*italic*)
- Inline code (`code`)
- Paragraphs
- Ordered and unordered lists
- Code blocks (```)
- Input validation and error messages

Optional:
- Title tag from first heading
- Links ([text](url))
"""
import sys
import argparse
from md_parser import parse_markdown
from html_builder import build_html

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown (.md) to HTML.')
    parser.add_argument('input', nargs='?', help='Input Markdown file (default: stdin)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: stdout)')
    parser.add_argument('-v', '--version', action='version', version='md2html 1.0')
    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input, encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f'Error reading {args.input}: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()

    html_body, title = parse_markdown(lines)
    output_lines = build_html(html_body, title)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for line in output_lines:
                    f.write(line + '\n')
        except Exception as e:
            print(f'Error writing {args.output}: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        for line in output_lines:
            print(line)

if __name__ == '__main__':
    main()
