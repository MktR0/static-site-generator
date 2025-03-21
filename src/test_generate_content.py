import unittest

from generate_content import (
    extract_title,
)


md_1 = """# Tolkien Fan Club             

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""

md_2 = """hello
# still valid
"""

md_3 = """# 
should this be valid
"""


class TestGenerateContent(unittest.TestCase):
    def test_extract_title(self):

        self.assertEqual(extract_title(md_1), "Tolkien Fan Club")

        self.assertEqual(extract_title(md_2), "still valid")

        with self.assertRaises(ValueError):
            extract_title(md_3)


if __name__ == "__main__":
    unittest.main()
