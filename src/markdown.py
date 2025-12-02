from enum import Enum
from htmlnode import HTMLNode, text_to_textnodes, text_node_to_html_node, ParentNode, LeafNode
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks  

def block_to_block_type(block):
    match block:
        case b if "# " in b[0:6]:
            block_type = BlockType.HEADING
        case b if b.startswith("```") and b.strip().endswith("```"):
            block_type = BlockType.CODE
        case b if b[0] == ">":
            block_type = BlockType.QUOTE
        case b if b[0:2] == "- ":
            block_type = BlockType.UL
        case b if b[0].isnumeric() and b[1] == ".":
            block_type = BlockType.OL
        case _:
            block_type = BlockType.PARAGRAPH                   
    
    return block_type    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
        if type == BlockType.QUOTE:
            block_list = [bk.lstrip("> ").strip() for bk in block.split("\n")]
            block = "\n".join(block_list)
        if type == BlockType.HEADING:
            count = len(block) - len(block.lstrip("#"))
            block = block.lstrip("#").strip()
        if(type != BlockType.CODE):
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
        else:
            block = block.strip("```").lstrip("\n")
            html_nodes = [text_node_to_html_node(TextNode(block, TextType.TEXT))]      
        

        match type:
            case BlockType.PARAGRAPH:
                child_nodes.append(ParentNode("p", html_nodes))
            case BlockType.HEADING:
                child_nodes.append(ParentNode(f"h{count}", html_nodes))
            case BlockType.CODE:
                child_nodes.append(ParentNode("pre", [ParentNode("code", [LeafNode(None, block)])]))
            case BlockType.QUOTE:
                child_nodes.append(ParentNode("blockquote", html_nodes))
            case BlockType.UL:
                li_nodes = []
                for line in block.split("\n"):
                    temp = []
                    for node in text_to_textnodes(line.lstrip("- ").strip()):
                        temp.append(text_node_to_html_node(node))
                    li_nodes.append(ParentNode("li", temp))

                child_nodes.append(ParentNode("ul", li_nodes))
            case BlockType.OL:
                li_nodes = []
                for line in block.split("\n"):
                    temp = []
                    ind = line.find(".")
                    for node in text_to_textnodes(line[ind + 1:].strip()):
                        temp.append(text_node_to_html_node(node))
                    li_nodes.append(ParentNode("li", temp))
                child_nodes.append(ParentNode("ol", li_nodes))
            case _:
                child_nodes.append(ParentNode("p", html_nodes))

    return ParentNode("div", child_nodes)

def extract_title(markdown):
    for line in markdown.split("\n\n"):
        if line.find("# ") != -1:
            return line.lstrip("# ")
    return "Uh oh, Title not found."        