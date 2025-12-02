from textnode import TextType, TextNode
import re

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {"| ".join(self.children)}, {self.props})"    

    def to_html(self):
        raise NotImplementedError("This method has not been implemented")   

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        props_string = ""
        for prop in self.props:
            props_string += f' {prop}="{self.props[prop]}"'     

        return props_string    

      
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        string = ""
        if self.tag is None:
            string = f"{self.value}"
        else:
            string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"    
        return string        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have children")    
        string = ""
       
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()    
        string = f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"  
        return string   

def text_node_to_html_node(text_node):
    props = None
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
            text = text_node.text
        case TextType.BOLD:
            tag = "b"
            text = text_node.text
        case TextType.ITALIC:
            tag = "i"
            text = text_node.text
        case TextType.CODE:
            tag = "code"
            text = text_node.text
        case TextType.LINK:
            tag = "a"
            text = text_node.text
            props = {"href": text_node.url}
        case TextType.IMAGE:
            tag = "img"
            text = ""
            props = {"src": text_node.url, "alt": text_node.text}
        case _:
            raise Exception("Error: could not convert text node to html node. Invalid text type.")

    new_leaf = LeafNode(tag, text, props)
    return new_leaf       

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        old_node = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif old_node.count(delimiter) == 0:
            new_nodes.append(node)
        elif old_node.count(delimiter) % 2 != 0:
            raise Exception(f"Error: text_node_to_html_node({old_node}) Invalid Markdown")
        else:
            temp = old_node.split(delimiter)
            i = 0
            for segment in temp:
                if segment == "":
                    i += 1
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(segment, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(segment, text_type))
            
                i += 1
                
    return new_nodes  

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes      

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    code_split = split_nodes_delimiter(nodes, "`", TextType.CODE)
    img_split = split_nodes_image(code_split)
    link_split = split_nodes_link(img_split)
    bold_split = split_nodes_delimiter(link_split, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)

    return italic_split    

      