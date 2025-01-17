import unittest
from block_markdown import markdown_to_blocks  


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
                '    Spaced first line\nSecond line\n\nNew block', 
                'First block\n\tIndented with tab\n\nSecond block', 
                'First block\r\n\r\nSecond block', 
                'First block\n\nSecond block\n\n\n'

                ]

        expected_results = [
                
                [ "Spaced first line\nSecond line", "New block"],
                ["First block\n\tIndented with tab", "Second block"],
                ["First block", "Second block"], 
                ["First block","Second block"]

                ]


        for n, case in enumerate(cases):
            blocks = markdown_to_blocks(case)
            self.assertListEqual(blocks, expected_results[n]) 





if __name__ == "__main__":
    unittest.main()
