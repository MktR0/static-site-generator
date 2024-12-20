class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This funcionality is not implemented yet.")

    def props_to_html(self):
        if self.props == None:
            return ""
        html_props = ""
        for prop in self.props.keys():
            html_props += f' {prop}="{self.props[prop]}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
# TODO 
