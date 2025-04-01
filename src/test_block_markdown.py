import re
import unittest

from block_markdown import (
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_olist,
    block_type_paragraph,
    block_type_quote,
    block_type_ulist,
    is_code_block,
    is_heading,
    is_olist,
    is_quote_block,
    is_ulist_block,
    markdown_to_blocks,
    markdown_to_html_node,
)

is_heading_expected_results = [True, True, True, True, True, True, False, False]
is_code_expected_results = [True, True, True, True, False, False, False, False]
is_quote_expected_results = [True, True, False, False, True]
is_ulist_expected_results = [False, True, False, False, True]
is_olist_expected_results = [True, True, False, False, False, False, False, True]

test_heading_doc = """# 1 This is an example heading
sample text, to be ignored as a non header

## 2 This is an example heading
sample text, to be ignored as a non header

### 3 This is an example heading
sample text, to be ignored as a non header

####  4 This is an example heading
sample text, to be ignored as a non header

#####  \t\t5 This is an example heading
sample text, to be ignored as a non header

######  6 This is an example heading
sample text, to be ignored as a non header

######## not as many

######2######################## way too many
"""


test_code_doc = """```print("hello world!") # single line```

``` # multi line
print("hello world!")
```

```while True: # multiline with tabs
        print("hello world!")```

``` while True: # with leading and trailing whitespace
        print("hello world!") ```

``` while True: # missing backtick
        print("hello world!") ``

while True: # missing backticks
        print("hello world!")```

` print("hello world!") # missing backtick `

`` print("hello world!") # missing backtick ``
"""


test_quote_doc = """>hello

> quote block
>> nested quote block
>>>>>> very nested quote block

This is non quote block

>this starts off okay
But what are we thinking here
Or Here

> spaces without affecting output of quote block
"""


test_olist_doc = """1. hello

1. \t ordered list block
2. \t\tnested list block
3. >  ordered list block

This is non list block

1 this starts off kind of correct but who knows
2. But It tries here
3, But not Here

2.   a whole lot of spaces without affecting output of list block

9. Item
10. Item
11. Item

01. Item
02. Item
03. Item

1. This 2. should still be valid
"""


test_ulist_doc = """*hello

-\tlist block
*  \t\tnested list block
- >  block

This is non list block

\t* this starts off wrong but who knows
- But It tries here
* Or Here

-   a whole lot of spaces without affecting output of list block
"""


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        """Test that multiple consecutive newlines are handled correctly"""
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_non_standard_spacing_cases(self):
        """
        Because windows and people who use tabs instead of spaces

        Tests handling of various whitespace scenarios including:
        - Windows-style line endings
        - Tab indentation
        - Excessive spacing
        """
        cases = [
            "Spaced first line\nSecond line\n\nNew block",
            "First block\n\tIndented with tab\n\nSecond block",
            "First block\r\n\r\nSecond block",
            "First block\n\nSecond block\n\n\n",
        ]

        expected_results = [
            ["Spaced first line\nSecond line", "New block"],
            ["First block\n\tIndented with tab", "Second block"],
            ["First block", "Second block"],
            ["First block", "Second block"],
        ]

        for n, case in enumerate(cases):
            blocks = markdown_to_blocks(case)
            self.assertListEqual(blocks, expected_results[n])

    def test_block_to_block_type(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_all_block_helper_functions(self):
        """Tests all block_to_block_type helper functions against known test cases.

        Tests include:
            - Heading detection (1-6 #'s)
            - Code block detection (triple backticks)
            - Quote block detection (> prefix)
            - Unordered list detection (* or -)
            - Ordered list detection (numbers)

            Each test case includes valid and invalid formats,
            edge cases, and nested structures.
            Includes log file for debugging
        """
        test_docs = [
            test_heading_doc,
            test_code_doc,
            test_quote_doc,
            test_ulist_doc,
            test_olist_doc,
        ]

        functions = [
            is_heading,
            is_code_block,
            is_quote_block,
            is_ulist_block,
            is_olist,
        ]

        expected_results = [
            is_heading_expected_results,
            is_code_expected_results,
            is_quote_expected_results,
            is_ulist_expected_results,
            is_olist_expected_results,
        ]

        func_names = [
            "is_heading_expected_results",
            "is_code_expected_results",
            "is_quote_expected_results",
            "is_ulist_expected_results",
            "is_olist_expected_results",
        ]

        def format_test_block(doc):
            # add handling windows endline \r\n
            normalized_doc = re.sub(r"\r\n", "\n", doc)
            blocks = re.split("\n\n+", normalized_doc)
            blocks = list(filter(lambda a: a != "", blocks))
            return blocks

        for i, test_doc in enumerate(test_docs):
            test_case = format_test_block(test_doc)
            function = functions[i]
            expected_result = expected_results[i]

            for n, block in enumerate(test_case):
                actual_result = function(block)
                self.assertEqual(expected_result[n], actual_result)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_full_example(self):
        md = """# Markdown syntax guide

## Headers

# This is a Heading h1

## This is a Heading h2

###### This is a Heading h6

## Emphasis

*This text will be italic*  
*This will also be italic*

**This text will be bold**  
**This will also be bold**

*You can* **combine them**

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b


### Ordered

1. Item 1
2. Item 2
3. Item 3


## Images

![This is an alt text.](/image/sample.webp)

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.

> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.


## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.
"""
        expected_output = """<div><h1>Markdown syntax guide</h1>
<h2>Headers</h2>
<h1>This is a Heading h1</h1>
<h2>This is a Heading h2</h2>
<h6>This is a Heading h6</h6>
<h2>Emphasis</h2>
<p><i>This text will be italic</i><i>This will also be italic</i></p>
<p><b>This text will be bold</b><b>This will also be bold</b></p>
<p><i>You can</i><b>combine them</b></p>
<h2>Lists</h2>
<h3>Unordered</h3>
<ul>
<li>Item 1</li>
<li>Item 2</li>
<li>Item 2a</li>
<li>Item 2b</li>
</ul>
<h3>Ordered</h3>
<ol>
<li>Item 1</li>
<li>Item 2</li>
<li>Item 3</li>
</ol>
<h2>Images</h2>
<p><imgsrc="/image/sample.webp"alt="Thisisanalttext."></img></p>
<h2>Links</h2>
<p>You may be using <a href="https://markdownlivepreview.com/">Markdown Live Preview</a>.</p>
<h2>Blockquotes</h2>
<blockquote>
Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
</blockquote>
<blockquote>
Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.
</blockquote>
<h2>Blocks of code</h2>
<pre><code>let message = 'Hello world';
alert(message);
</code></pre>
<h2>Inline code</h2>
<p>This web site is using <code>markedjs/marked</code>.</p>
</div>"""

        # self.maxDiff = None

        def format_test_block(html: str) -> str:
            return "".join(html.split())

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(format_test_block(html), format_test_block(expected_output))


if __name__ == "__main__":
    unittest.main()
