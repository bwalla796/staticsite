import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from markdown import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(True, True)

    def test_props(self):
        node = HTMLNode(props={"test1": "test2"})
        string = ' test1="test2"'
        
        self.assertEqual(node.props_to_html(), string)

    def test_eq3(self):
        self.assertEqual(True, True)  

    #def test_leaf_to_html_p(self):
    #    node = LeafNode("p", "Hello, world!")
    #    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")    

    def test_parent_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")    

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")  

    def test_text_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )          
              
    def test_block_type(self):
        text = """
 This is **bolded** paragraph

 This is another paragraph with _italic_ text and `code` here
 This is the same paragraph on a new line

 - This is a list
 - with items
        """
        blocks = markdown_to_blocks(text)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UL)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()