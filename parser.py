import re

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
            while code_block_lines and code_block_lines[0].strip() == '':
                code_block_lines.pop(0)
            html.append('<pre><code>')
            html.extend([escape_html(line) for line in code_block_lines])
            html.append('</code></pre>')
            code_block_lines.clear()
            in_code_block = False

    def parse_inline(text):
        text = re.sub(r'\\([*#`\[\]])', r'\1', text)

        def repl_code(match):
            return '<code>' + escape_html(match.group(1)) + '</code>'

        text = re.sub(r'``([^`]+)``', repl_code, text)
        text = re.sub(r'`([^`]+)`', repl_code, text)
        text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<em><strong>\1</strong></em>', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
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
        if not line.strip():
            flush_paragraph()
            next_line = lines[idx+1] if idx+1 < len(lines) else ''
            if not re.match(r'^\s*([-*+]\s+|\d+\.\s+)', next_line):
                flush_list()
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            content = heading.group(2).rstrip().rstrip('#').rstrip()
            content = parse_inline(content)
            if not title and level == 1:
                title = re.sub('<.*?>', '', content)
            html.append(f'<h{level}>{content}</h{level}>')
            continue
        paragraph.append(line)
    flush_paragraph()
    flush_list()
    flush_code_block()
    return html, title
