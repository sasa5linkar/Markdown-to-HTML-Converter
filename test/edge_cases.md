# Edge Case Tests for Markdown-to-HTML

## Empty file


## Only code block

```
code only
```

## List with blank lines between items

- Item 1

- Item 2

- Item 3

## Nested lists (should not be nested in output)
- Parent
    - Child
- Parent 2

## Inline code with backticks: `` `code` ``

## Bold and italic together: ***bolditalic***

## Unclosed formatting
**bold
*italic

## Heading with trailing hashes
### Heading ###

## Link with title
[Google](https://google.com "Google Homepage")

## Escaped markdown
\*not italic\*
\# not heading
