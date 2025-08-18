"""HTML document assembly helpers."""

from html import escape as html_escape


def build_html(html_body, title):
    """Wrap parsed HTML snippets with a minimal document shell."""
    output_lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="UTF-8">',
        f'  <title>{html_escape(title, quote=False) if title else "Document"}</title>',
        "</head>",
        "<body>",
    ]
    output_lines.extend(html_body)
    output_lines.extend(["</body>", "</html>"])
    return output_lines
