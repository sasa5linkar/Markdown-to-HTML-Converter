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
            html.append('<pre><code>')
            html.extend([escape_html(line) for line in code_block_lines])
            html.append('</code></pre>')
            code_block_lines.clear()
            in_code_block = False

    def parse_inline(text):
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text

    def escape_html(text):
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;'))

    for line in lines:
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
        if not line.strip():
            flush_paragraph()
            flush_list()
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            content = parse_inline(heading.group(2))
            if not title and level == 1:
                title = re.sub('<.*?>', '', content)
            html.append(f'<h{level}>{content}</h{level}>')
            continue
        ul_match = re.match(r'^\s*([-*+])\s+(.*)', line)
        ol_match = re.match(r'^\s*(\d+)\.\s+(.*)', line)
        if ul_match:
            flush_paragraph()
            if not in_list or list_type != 'ul':
                flush_list()
                html.append('<ul>')
                in_list = True
                list_type = 'ul'
            html.append(f'<li>{parse_inline(ul_match.group(2))}</li>')
            continue
        if ol_match:
            flush_paragraph()
            if not in_list or list_type != 'ol':
                flush_list()
                html.append('<ol>')
                in_list = True
                list_type = 'ol'
            html.append(f'<li>{parse_inline(ol_match.group(2))}</li>')
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
    if len(sys.argv) != 2:
        print('Usage: python md2html.py input.md > output.html', file=sys.stderr)
        sys.exit(1)
    input_path = sys.argv[1]
    try:
        with open(input_path, encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f'Error reading {input_path}: {e}', file=sys.stderr)
        sys.exit(1)
    html_body, title = parse_markdown(lines)
    print('<!DOCTYPE html>')
    print('<html lang="en">')
    print('<head>')
    print('  <meta charset="UTF-8">')
    print(f'  <title>{escape_html(title) if title else "Document"}</title>')
    print('</head>')
    print('<body>')
    for line in html_body:
        print(line)
    print('</body>')
    print('</html>')

def escape_html(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

if __name__ == '__main__':
    main()
