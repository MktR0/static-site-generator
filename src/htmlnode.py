class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        html_props = ""
        for prop in self.props.keys():
            html_props += f' {prop}="{self.props[prop]}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __setattr__(self, name, value):
        if name == "children" and hasattr(self,"children"):
            raise AttributeError("LeafNode cannot have a children")
        super().__setattr__(name, value)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leafnode must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __setattr__(self, name, value):
        if name == "value" and hasattr(self, "value"):
            raise AttributeError("ParentNode cannot have a value")
        super().__setattr__(name, value)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        # ensure that an empty list is counted as having no children 
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

