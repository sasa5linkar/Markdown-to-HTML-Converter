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
import re
import argparse

# --- Markdown Parser ---
def parse_markdown(lines):
    html = []
    in_list = False
    list_type = None
    in_code_block = False
    code_block_lines = []
    title = None
    paragraph = []

    def flush_paragraph():
        if paragraph:
            html.append('<p>' + parse_inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            html.append(f'</{list_type}>')
            in_list = False
            list_type = None

    def flush_code_block():
        nonlocal in_code_block
        if in_code_block:
            # Remove leading blank line if present
            while code_block_lines and code_block_lines[0].strip() == '':
                code_block_lines.pop(0)
            html.append('<pre><code>')
            html.extend([escape_html(line) for line in code_block_lines])
            html.append('</code></pre>')
            code_block_lines.clear()
            in_code_block = False

    def parse_inline(text):
        # Handle escaped markdown (\* \# etc)
        text = re.sub(r'\\([*#`\[\]])', r'\1', text)
        # Inline code (handle double backticks and single)
        text = re.sub(r'``([^`]+)``', r'<code>\1</code>', text)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold+italic (***text***)
        text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<em><strong>\1</strong></em>', text)
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # Links with optional title (ignore title for now)
        text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', r'<a href="\2">\1</a>', text)
        return text

    def escape_html(text):
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;'))

    prev_list_type = None
    for idx, line in enumerate(lines):
        line = line.rstrip('\n')
        if in_code_block:
            if line.strip().startswith('```'):
                flush_code_block()
            else:
                code_block_lines.append(line)
            continue
        if line.strip().startswith('```'):
            flush_paragraph()
            flush_list()
            in_code_block = True
            continue
        # List item detection
        ul_match = re.match(r'^\s*([-*+])\s+(.*)', line)
        ol_match = re.match(r'^\s*(\d+)\.\s+(.*)', line)
        if ul_match or ol_match:
            flush_paragraph()
            curr_type = 'ul' if ul_match else 'ol'
            if not in_list or list_type != curr_type:
                flush_list()
                html.append(f'<{curr_type}>')
                in_list = True
                list_type = curr_type
            item_text = ul_match.group(2) if ul_match else ol_match.group(2)
            html.append(f'<li>{parse_inline(item_text)}</li>')
            prev_list_type = curr_type
            continue
        # Allow blank lines between list items (do not flush list)
        if not line.strip():
            flush_paragraph()
            # Only flush list if next non-blank line is not a list item
            next_line = lines[idx+1] if idx+1 < len(lines) else ''
            if not re.match(r'^\s*([-*+]\s+|\d+\.\s+)', next_line):
                flush_list()
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            # Remove trailing hashes for ATX-style headings
            content = heading.group(2).rstrip().rstrip('#').rstrip()
            content = parse_inline(content)
            if not title and level == 1:
                title = re.sub('<.*?>', '', content)
            html.append(f'<h{level}>{content}</h{level}>')
            continue
        # Otherwise, treat as paragraph text
        paragraph.append(line)
    # Final flush
    flush_paragraph()
    flush_list()
    flush_code_block()
    return html, title

# --- Main Function ---
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
    output_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="UTF-8">',
        f'  <title>{escape_html(title) if title else "Document"}</title>',
        '</head>',
        '<body>'
    ]
    output_lines.extend(html_body)
    output_lines.append('</body>')
    output_lines.append('</html>')

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

def escape_html(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

if __name__ == '__main__':
    main()
