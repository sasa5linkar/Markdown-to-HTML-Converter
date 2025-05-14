def build_html(html_body, title):
    def escape_html(text):
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;'))
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
    return output_lines
