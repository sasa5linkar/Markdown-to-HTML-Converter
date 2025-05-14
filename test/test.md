# Testing Documentation for Markdown-to-HTML Converter

This directory contains automated tests and reference files for the Markdown-to-HTML converter (`md2html.py`).

## Files

- `example.md` / `example.html`: A basic Markdown file and its expected HTML output. This covers standard Markdown features such as headings, bold, italic, inline code, lists, code blocks, paragraphs, and links.
- `edge_cases.md` / `edge_cases.html`: Markdown and expected HTML output for a variety of edge cases, including:
  - Empty files
  - Code blocks only
  - Lists with blank lines between items
  - Nested lists (should be flattened)
  - Inline code with backticks
  - Bold and italic together
  - Unclosed formatting
  - Headings with trailing hashes
  - Links with titles
  - Escaped markdown characters
- `output_example.html`, `output_edge_cases.html`, `output.html`: Generated outputs from running the converter. Used for comparison during testing.
- `test_md2html.py`: Automated test script. Runs the converter on the Markdown files and compares the output to the expected HTML. If the outputs match, the test passes; otherwise, it fails and reports the difference.

## How to Run Tests

From the `test` directory, run:

```sh
python test_md2html.py
```

This will check both the standard and edge case Markdown files. All tests should pass if the converter is working correctly.

## Purpose

These tests ensure that the Markdown-to-HTML converter:
- Correctly implements the required Markdown features
- Handles edge cases and malformed input gracefully
- Produces consistent, predictable HTML output

You can add more Markdown/HTML pairs to expand test coverage as needed.
