#!/usr/bin/env python

from collections import deque

class TreeNode(object):
    def __init__(self,key,val,left=None,right=None,parent=None):
        self.key = key
        self.val = val
        if isinstance(left, TreeNode):
            if left.key <= self.key:
                self.leftChild = left
        else: self.leftChild = None
        if isinstance(right, TreeNode):
            if right.key > self.key:
                self.rightChild = right
        else: self.rightChild = None
        self.parent = parent

    def hasLeftChild(self): return self.leftChild

    def hasRightChild(self): return self.rightChild

    def isLeftChild(self):
        if self.parent: return self.parent.leftChild == self
        return False

    def isRightChild(self):
        if self.parent: return self.parent.rightChild == self
        return False

    def isRoot(self): return not self.parent

    def isLeaf(self): return not (self.rightChild or self.leftChild)

    #def hasChildren(self):
    #    return self.rightChild and self.leftChild
    
    def setParentChild(self, newNode):
        '''Sets self node's parent's relation to a new child node newNode'''
        if self.parent:
            if self.isLeftChild(): self.parent.leftChild = newNode
            elif self.isRightChild(): self.parent.rightChild = newNode
    
    def removeParent(self, newParent, otherNode=None):
        # Sets self node's parents point to the otherNode
        self.setParentChild(otherNode)
        # Sets self node' parent to newParent
        self.parent = newParent
    
    
    def reassignParent(self, otherParent, otherNode):
        ''' 
            - Set otherNode' Parents to self's Parents
            - Remove self node's Parents.
            - Connect self Node to some otherParent node.
            For instance, 
            when swapping two nodes, forming right parent connections.
        '''
        selfParent = self.parent
        self.removeParent(otherParent, otherNode)
        otherNode.removeParent(selfParent, self)
        
    def replaceNodeData(self,key,value,lc=None,rc=None, parent=None):
        self.key = key
        self.val = value
        if self.hasLeftChild():
            #detach self as the left child's parent
            self.leftChild.parent = None
        #assign new left child
        self.leftChild = lc
        #attach self as the left child's parent
        if self.leftChild: self.leftChild.parent = self
        
        if self.hasRightChild():
            #detach self as the right child's parent
            self.rightChild.parent = None
        #assign new right child
        self.rightChild = rc
        #attach self as the right child's parent
        if self.rightChild: self.rightChild.parent = self
        
        self.removeParent(parent)
    
    def _swap(self, min_node):
        #technically, swapping is..
        #self.replaceNodeData(min_node.key, min_node.val, parent=min_node.parent)
        min_node.replaceNodeData(self.key, self.val, lc = self.leftChild, rc = self.rightChild, parent = self.parent)
    


class rbNode(TreeNode):
    '''color denotes the node's parent link'''
    def __init__(self,key,val, color, left=None,right=None,parent=None):
        # True- red, False - black
        super(type(self), self).__init__(key,val,left=left,right=right,parent=parent)
        self.color = color
        
    def isRed(self): return self.color
    
    def isBlack(self): return not self.isRed()
    

#BST functions

def findMax(node):
    while node.hasRightChild():
        node = node.rightChild
    return node

def findMin(node):
    while node.hasLeftChild():
        node = node.leftChild
    return node
    
def delMax(bst):
    node = findMax(bst.root)
    parent = node.parent
    parent.rightChild = None
    del node
    bst.size -= 1

def delMin(bst):
    node = findMin(bst.root)
    parent = node.parent
    parent.leftChild = None
    del node
    bst.size -= 1

def delete(bst, key):
    """
    search and perform removal for bst.
    """
    node = bst.root
    while node:
        if key < node.key: node = node.leftChild
        elif key > node.key: node = node.rightChild
        else:
            bst._remove(node)


class BinarySearchTree(object):

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self): return self.size

    def insert(self,key,val, left=None, right=None):
        if self.root: self._insert(key,val, self.root, left=left, right=right)
        else: self.root = TreeNode(key,val, left=left,right=right)
        self.size = self.size + 1

    def _insert(self,key,val, currentNode, left=None, right=None):
        lastNode = None
        child_attr = ''
        while currentNode:
            lastNode = currentNode
            if key <= currentNode.key:    
                currentNode = currentNode.leftChild
                child_attr = 'leftChild'
            else:
                currentNode = currentNode.rightChild
                child_attr = 'rightChild'
        setattr(lastNode, child_attr, TreeNode(key,val,left=left, right=right, parent=lastNode))

    def __setitem__(self,k,v): self.insert(k,v)

    def get(self,key):
       if self.root:
           return self._get(key,self.root)
       return None

    def _get(self,key,currentNode):
        while currentNode:
            if key == currentNode.key: return currentNode
            elif key < currentNode.key: currentNode = currentNode.leftChild
            else: currentNode = currentNode.rightChild
        return None
        
    def __getitem__(self,key): return self.get(key)

    def __contains__(self,key): return not not self.get(key)
    
    def __iter__(self):
        '''bfs type level order traversal'''
        s = deque([self.root], 3)
        while s: 
            node = s.pop()
            yield node
            if node.hasLeftChild(): s.appendleft(node.leftChild)
            if node.hasRightChild(): s.appendleft(node.rightChild)
    
    
    def __delitem__(self, key): 
        delete(self, key)
        self.size -= 1
    
    def _remove(self, node):
        """
        Assuming key is not Min or Max.
            - If key is a leaf - just delete
            - If key has one subtree - root of child-subtree takes key'
         position
            - If key has two subtrees:
                    - find Min node of right subtree
                    - swap Min node with key.
                    - delete key
        """
        if node.hasLeftChild() and not node.hasRightChild():
            x = node.leftChild
            node.replaceNodeData(x.key,x.val,lc=x.leftChild,rc=x.rightChild, parent=node.parent)
            if not node.parent: self.root = node
            del x
        elif node.hasRightChild() and not node.hasLeftChild():
            x = node.rightChild
            node.replaceNodeData(x.key,x.val,lc=x.leftChild,rc=x.rightChild, parent=node.parent)
            if not node.parent: self.root = node
            del x
        elif node.hasLeftChild() and node.hasRightChild():
            min_node = findMin(node.rightChild)
            node._swap(min_node)
            node.setParentChild(min_node)
            if not min_node.parent: self.root = min_node.parent
            del node
        elif node.isLeaf():
            node.setParentChild(None)
            if not node.parent: self.root = None
            del node


#red black tree functions

def rotateLeft(node):
    x = node.rightChild
    nodeParent = node.parent
    #x.parent = node.parent
    #node.rightChild = x.leftChild
    x.removeParent(nodeParent, x.leftChild)
    node.removeParent(x, x)
    if node.hasRightChild(): node.rightChild.parent = node
    x.leftChild = node
    
    x.color = node.color
    node.color = True
    #node.parent = x
    return x

def rotateRight(node):
    x = node.leftChild
    nodeParent = node.parent
    #x.parent = node.parent
    #node.leftChild = x.rightChild
    x.removeParent(nodeParent, x.rightChild)
    node.removeParent(x, x)
    if node.hasLeftChild(): node.leftChild.parent = node
    x.rightChild = node
    
    x.color = node.color
    node.color = True
    #node.parent = x
    return x

def flipColor(node):
    assert not node.isRed()
    assert node.leftChild.isRed()
    assert node.rightChild.isRed()
    
    node.leftChild.color = not node.leftChild.color
    node.rightChild.color = not node.rightChild.color
    if node.parent: node.color = not node.color

def rotateProtocol(node):
    #rotate right newly inserted node if on right
    stat = False
    if node.rightChild:
        if node.rightChild.isRed():            
            if node.leftChild:
                if node.leftChild.isBlack():
                    stat = True
            if stat or not (stat or node.hasLeftChild()):
                node = rotateLeft(node)
                node = node.leftChild
    #right rotate if child node and parent node links red
    if node.leftChild:
        if node.leftChild.isRed() and node.isRed() and node.isLeftChild():
            node = rotateRight(node.parent)
    #flip color links if right and left nodes red and parent link black
    if node.leftChild and node.rightChild:
        if node.leftChild.isRed() and node.rightChild.isRed():
            flipColor(node)
    return node


def shiftRedRight(node):
    flipColor(node)
    if node.hasLeftChild():
        if node.leftChild.hasLeftChild():
            if node.leftChild.leftChild.isRed():
                node = rotateRight(node)
                flipColor(node)
    return node

def shiftRedLeft(node):
    flipColor(node)
    if node.hasRightChild():
        if node.rightChild.hasLeftChild():
            rotateRight(node.rightChild)
            node = rotateLeft(node)
            flipColor(node)
    return node

def rbDelMax(rb):
    s = deque([])
    node = rb.root
    while node:  
        if node.hasLeftChild():
            if node.leftChild.isRed():
                node = rotateRight(node)
        
        if node:
            if not node.hasRightChild():
                x = node.parent
                node.setParentChild(None)
                del node
                node = x
            
            if node.hasRightChild():
                if not node.rightChild.isRed() and node.rightChild.hasLeftChild():
                    if not node.rightChild.leftChild.isRed():
                        node = shiftRedRight(node.rightChild)
        
            
            if s:
                if s[0] != node:
                    s.appendleft(node)
            elif not s: 
                s.appendleft(node)
                
            node = node.rightChild
    
    #print "stack is %s"%s
    node = s.popleft()
    node.rightChild = None
    while s:
        node = rotateProtocol(node)
        #print "node after rotateProtocol is: %s and stack: %s"%(node.key, s)
        x = s.popleft()
        x.rightChild = node
        node = x
    
    rb.root = node
    rb.size -= 1
    return

def rbDelMin(rb):
    s = deque([])
    node = rb.root
    while node:
        if not node.hasLeftChild():
            x = node.parent
            node.setParentChild(None)
            del node
            node = x
        
        if node:
            if node.hasLeftChild():
                if not node.leftChild.isRed() and node.leftChild.hasLeftChild():
                    if node.leftChild.leftChild.isRed():
                        node = shiftRedLeft(node)
            
            if s:
                if s[0] != node:
                    s.appendleft(node)
            elif not s: 
                s.appendleft(node)
                
            node = node.leftChild
    
    node = s.popleft()
    node.leftChild = None
    while s:
        node = rotateProtocol(node)
        x = s.popleft()
        x.leftChild = node
        node = x
        
    rb.root = node
    rb.size -= 1
    return


def rbDel(rb, key):
    s = deque([])
    node = rb.root
    while node:
        if key < node.key:
            if node.hasLeftChild():
                if not node.leftChild.isRed() and node.leftChild.hasLeftChild():
                    if not node.leftChild.leftChild.isRed():
                        node = shiftRedLeft(node)
                s.appendleft([node, 'leftChild'])
                node = node.leftChild
        else:
            if node.hasLeftChild():
                if node.leftChild.isRed():
                    node = rotateRight(node)
            
            if key == node.key and node.isLeaf():
                x = node.parent
                node.setParentChild(None)
                del node
                node = x
            
            if node.hasRightChild():
                if not node.rightChild.isRed():
                    node = shiftRedRight(node)
            
            if key == node.key and not node.isLeaf():
                min_node = findMin(node.rightChild)
                node._swap(min_node)
                node.setParentChild(min_node)
                del node
                node = min_node
            
            s.appendleft([node, 'rightChild'])
            node = node.rightChild
        
    node, orientation = s.popleft()
    setattr(node, orientation, None)
    while s:
        node = rotateProtocol(node)
        x, orientation = s.popleft()
        setattr(x, orientation, node)
        node = x
        
    rb.root = node
    return


class rbTree(BinarySearchTree):
    
    def insert(self,key,val, left=None, right=None):
        if self.root:
            self._insert(key,val, self.root, left=left, right=right)
        else:
            self.root = rbNode(key,val, None, left=left,right=right)
        self.size = self.size + 1
    
    def _insert(self,key,val, currentNode, left=None, right=None):
        print "key %s; val %s"%(key, val)
        root = lastNode = None
        child_attr = ''
        #worst case lg(N)
        while currentNode:
            lastNode = currentNode
            if key <= currentNode.key:    
                currentNode = currentNode.leftChild
                child_attr = 'leftChild'
            else:
                currentNode = currentNode.rightChild
                child_attr = 'rightChild'
        setattr(lastNode, child_attr, rbNode(key,val, True, left=left, right=right, parent=lastNode))
        
        #worst case lg(N)
        print "lastNode was %s %s" %(lastNode.key, lastNode.val)
        while lastNode:
            print "lastNode: %s %s" %(lastNode.key, lastNode.val)
            lastNode = rotateProtocol(lastNode)
            root = lastNode
            print "returned lastNode: %s %s" %(lastNode.key, lastNode.val)
            lastNode = lastNode.parent
            
        self.root = root
        return
    
    def __delitem__(self, key): 
        rbDel(self, key)
        self.size -= 1



if __name__ == "__main__":
    print "\ntesting for BinarySearchTree"
    
    b = BinarySearchTree()
    
    b.insert(1, 'red')
    
    b.insert(20, 'redness')
    
    b.insert(40, 'hotness')
    
    for x in b: print x.key, x.val
    print "="*10
    
    
    del b[1]
    for x in b: print x.key, x.val
    print "="*10
    
    b.insert(40, 'hotness')
    b.insert(40, 'hotness')
    b.insert(400, 'hotness')
    b.insert(-34540, 'hotness')
    for x in b: print x.key, x.val
    print "="*10
    
    print "\ntesting for rbTree"
    
    r = rbTree()
    print "\ntesting for insertion"
    r[1] = 'one'
    r[3] = 'three'
    r[2] = 'two'
    r[4] = 'four'
    r[6] = 'six'
    r[5] = 'five'
    
    print "\ntesting for deletion"
    #TODO: check this
    rbDelMax(r)
    rbDelMin(r)
    
    del r
    
    print "Creating new rbTree\n"
    r = rbTree()
    print "\n randomly generated integers"
    arr = [ 27552,  29086,  70311, -84170,  13924,   9010,  75356, -14113, 15858, -26237]
    del_stat = [0, 1, 0, 1, 1, 1, 1, 0, 0, 1]
    
    for each in arr: r[each] = each
    
    #for each in del_stat:
    #    if each:
    #        delMax(r)
    #    else:
    #        delMin(r) 
    
    
        
