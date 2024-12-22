class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ''
        html_props = ''
        for (key, value) in self.props.items():
            html_props += f' {key}="{value}"'
        return html_props
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props_to_html() == self.props_to_html():
            return True
        return False
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})'
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('Value is required')
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.props == other.props:
            return True
        return False
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super.__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('Tag is required')
        if not self.children:
            raise ValueError('Parent must have children')