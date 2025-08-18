"""CLI for converting Markdown to HTML."""

import argparse
import sys
from pathlib import Path

from md_parser import parse_markdown
from html_builder import build_html

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown (.md) to HTML.')
    parser.add_argument('input', nargs='?', type=Path, help='Input Markdown file (default: stdin)')
    parser.add_argument('-o', '--output', type=Path, help='Output HTML file (default: stdout)')
    parser.add_argument('-v', '--version', action='version', version='md2html 1.0')
    args = parser.parse_args()

    if args.input:
        try:
            lines = args.input.read_text(encoding='utf-8').splitlines(keepends=True)
        except Exception as e:  # pragma: no cover - defensive
            print(f'Error reading {args.input}: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()

    html_body, title = parse_markdown(lines)
    output_lines = build_html(html_body, title)

    if args.output:
        try:
            args.output.write_text('\n'.join(output_lines) + '\n', encoding='utf-8')
        except Exception as e:  # pragma: no cover - defensive
            print(f'Error writing {args.output}: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        for line in output_lines:
            print(line)

if __name__ == '__main__':
    main()
