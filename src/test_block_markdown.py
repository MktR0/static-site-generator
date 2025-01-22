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

        with open("helper_test_log.txt", "w") as file:
            file.write(f"{'~'*50}\n")
            file.write("Logger for my Helper Function Test\n")
            file.write(f"{'~'*50}\n\n")

        for i, test_doc in enumerate(test_docs):
            test_case = format_test_block(test_doc)
            function = functions[i]
            expected_result = expected_results[i]

            with open("helper_test_log.txt", "+a") as file:
                file.write(f"[~{('_'.join((func_names[i]).split('_')[:2]))}~]\n\n")

            check = " "
            for n, block in enumerate(test_case):
                actual_result = function(block)
                self.assertEqual(expected_result[n], actual_result)
                check = "✓"
                with open("helper_test_log.txt", "+a") as file:
                    length = len(f"< Test Case: {n+1} >\n")
                    file.write(f"{'='*length}\n")
                    file.write(f"< Test Case: {n+1} >\n")
                    file.write(f"{'='*length}\n")
                    file.write(f"{'-'*50}\n")
                    file.write(f"Test Block = '''{block}'''\n")
                    file.write(f"[{check}] Actual = {actual_result}\n")
                    file.write(f"[{check}] Expected = {expected_result[n]}\n")
                    file.write(f"{'-'*50}\n\n")


if __name__ == "__main__":
    unittest.main()
