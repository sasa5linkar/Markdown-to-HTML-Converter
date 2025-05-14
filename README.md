# Markdown-to-HTML Converter

A simple Python script to convert Markdown (.md) files to HTML, supporting a core subset of Markdown features.

## Features

- Headings (# to ######)
- Bold (**bold**)
- Italic (*italic*)
- Inline code (`code`)
- Paragraphs
- Ordered and unordered lists
- Code blocks (```) with `<pre><code>`
- Title tag from first heading
- Links ([text](url))

## Usage

```sh
python md2html.py input.md > output.html
```

- `input.md`: Path to your Markdown file
- Output is written to standard output (redirect to a file as shown above)

## Requirements

- Python 3.x
- No external dependencies (uses only the Python standard library)

## Example

Given `example.md`:

```markdown
# My Document

This is a **bold** and *italic* example with `inline code`.

- Item 1
- Item 2

1. First
2. Second

````markdown

Code block here

````

[Link to Python](https://python.org)
```

Run:

```sh
python md2html.py example.md > example.html
```

## Notes

- Only a subset of Markdown is supported (see Features).
- For advanced Markdown, consider using a full-featured library.

## License

MIT
