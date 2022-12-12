"""
Binary search trees

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

class node():
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right
    def __repr__(self):
        return str(self.data)

def search_bt(t, d, is_find_only=True):
    """
    Input
      t:            a node of a binary tree
      d:            target data to be found in the tree
      is_find_only: True/False, specifying type of output

    Output
      the node that contans d or None if is_find_only is True, otherwise
      the node that should be the parent node of d
    """
    if t is None:
        return
    if d < t.data:
        next = t.left
    else:
        next = t.right
    if t.data == d:
        if is_find_only:
            return t
        else:
            return
    if is_find_only==False and next is None:
        return t
    return search_bt(next, d, is_find_only)

def insert(t, d):
    n = search_bt(t, d, False)
    if n is None:
        return
    n0 = node(d, left=None, right=None)
    if d < n.data:
        n.left = n0
    else:
        n.right = n0

def bt(data):
    root = node(data=data[0], left=None, right=None)
    for d in data[1:]:
        insert(root, d)
    return root

def search_bt_loop(t, d, is_find_only=True):
    """
    similar to search_bt, but use a while loop instead of recursive
    """
    while True:
        if t is None:
            return
        if t.data == d:
            if is_find_only:
                return t
            else:
                return
        if d < t.data:
            next = t.left
        else:
            next = t.right
        if not is_find_only and next is None:
            return t
        t = next

def insert_loop(t, d):
    n = search_bt_loop(t, d, False)
    if n is None:
        return
    n0 = node(d, left=None, right=None)
    if d < n.data:
        n.left = n0
    else:
        n.right = n0

def bt_loop(data):
    root = node(data=data[0], left=None, right=None)
    for d in data[1:]:
        insert_loop(root, d)
    return root

def bt_print(t):
    if t.left:
        bt_print(t.left)
    print(t)
    if t.right:
        bt_print(t.right)

def tree_print(t):
    """
    This is adopted from the MIT OpenCourseWare at
    https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/7f7ba1c1c85b1ec4bd58965bfe791489_bst.py

    The old link does not work:
    http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/readings/binary-search-trees/bst.py
 
    Now supports Python 3
    """
    def tree_print_helper(t):
        if t is None:
            return [], 0, 0
        # label = str(t.key)
        label = str(t)
        leftstr, leftpos, leftwidth = tree_print_helper(t.left)
        rightstr, rightpos, rightwidth = tree_print_helper(t.right)
        middle = max(rightpos+leftwidth - leftpos+1, len(label), 2) # length
        pos = leftpos + middle // 2                                 # pos of current node
        width = leftpos + middle + rightwidth - rightpos
        while len(leftstr)<len(rightstr):
            leftstr.append(' '*leftwidth)
        while len(rightstr)<len(leftstr):
            rightstr.append(' '*rightwidth)
        if (middle-len(label))%2 == 1:
            label += '_'
        label = label.center(middle, '_')
        if label[0] == '_':
            label=' ' + label[1:]
        if label[-1] == '_':
            label = label[:-1]+' '
        lines = [' '*leftpos + label + ' '*(rightwidth-rightpos), ' '*leftpos + '/' + ' '*(middle-2) + '\\' + ' '*(rightwidth-rightpos)] + [leftline + ' '*(width-leftwidth-rightwidth) + rightline for leftline, rightline in zip(leftstr, rightstr)]
        return lines, pos, width
    print('\n'.join(tree_print_helper(t)[0]))

if __name__ == '__main__':
    data = range(3)
    t = bt(data)
    tree_print(t)
