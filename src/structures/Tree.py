class TreeNode():
    def __init__(self):
        self._element = None
        self._parent: TreeNode = None
        self._children: list[TreeNode] = []

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    @property
    def children(self):
        return self._children
    
    @children.setter
    def children(self, value):
        self._children = value
        
    @property
    def element(self):
        return self._element
    
    @element.setter
    def element(self, value):
        self._element = value
        
    def add_child(self, node):
        node.parent = self
        self.children.append(node)
        
    def is_root(self) -> bool:
        return self._parent is None

    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def __eq__(self, other) -> bool:
        return self == other
    
    def __ne__(self, other) -> bool:
        return self != other

class Tree(object):
    def __init__(self):
        self._root: TreeNode = None
    
    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self, value):
        self._root = value
    
    def is_empty(self):
        return self._root == None
    
    def depth(self, node: TreeNode) -> int:
        if node.is_root():
            return 0
        return 1 + self.depth(node.parent)
    
    def __height(self, node: TreeNode) -> int:
        if node.is_leaf():
            return 0
        else:
            return 1 + max(self.__height(child) for child in node.children)
    
    def height(self):
        return self._height(self.root)
    
    def preorder(self, func):
        self._preorder(self._root, func)
    
    def postorder(self, func):
        self.__postorder(self._root, func)
    
    def __preorder(self, node: TreeNode, func):
        func(node)
        for child in node.children:
            self.__preorder(child)
            
    def __postorder(self, node: TreeNode, func):
        for child in node.children:
            self._postorder(child)
        func(node)
    

