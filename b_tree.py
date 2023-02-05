# THIS FILE CONTAINS BASIC IMPLEMENTATION OF A B-TREE

class BTreeNode:
    def __init__(self, is_leaf=False):
        # .leaf - indicator "IS THIS NODE A LEAF?"
        # .children - array of references to node`s children
        # .keys - array of node values
        # .n - number of keys in node (currently)
        self.leaf = is_leaf
        self.children = []
        self.keys = []
        self.n = 0


class BTree:
    def __init__(self, deg):
        self.root = BTreeNode(is_leaf=True)
        self.degree = deg

    # SEARCH FOR A KEY IN NOE VALUES. NOT FOUND => DESCEND TO A CHILD WITH NEEDED RANGE OF VALUES
    # key - KEY TO FIND
    # node - CURRENT NODE TO SEARCH IN
    def search(self, key, node=None):
        i = 0
        if node is None:
            node = self.root

        while i < node.n and key > node.keys[i][0]:
            i += 1

        if i < node.n and key == node.keys[i][0]:
            return node.keys[i]
        elif node.leaf:
            return None

        return self.search(key, node.children[i])

    # SPLITTING NODE`S CHILD INTO 2 NEW CHILDREN WITH (DEGREE - 1) KEYS
    # (ASSUMING THAT child_to_split IS FULL (HAS (2*DEGREE - 1) KEYS))
    # node - NODE WHICH HOLDS FULL CHILD
    # index - INDEX OF A FULL NODE IN node.children
    def split_child(self, node, index):
        new_child = BTreeNode(True)
        child_to_split = node.children[index]
        new_child.leaf = child_to_split.leaf
        new_child.n = self.degree - 1

        # DIVIDING FULL CHILD INTO 2 EQUAL NEW CHILDREN
        new_child.keys = child_to_split.keys[self.degree:]
        if not child_to_split.leaf:
            new_child.children = child_to_split.children[self.degree:]

        # RESIZING OLD CHILD
        median = child_to_split.keys[self.degree - 1]
        child_to_split.n = self.degree - 1
        child_to_split.keys = child_to_split.keys[:self.degree - 1]
        child_to_split.children = child_to_split.children[:self.degree]

        # SHIFTING PARENT NODE DATA, TO FIT IN NEW KEY AND CHILD
        node.children[index + 1:node.n + 2] = [new_child, *node.children[index + 1:]]
        node.keys[index:node.n + 1] = [median, *node.keys[index:]]
        node.n += 1

    # INITIATE INSERTION IN THE TREE (FIRSTLY CHECK IF ROOT IS FULL)
    # pair - KEY-VALUE PAIR TO INSERT IN DATABASE
    def insert(self, pair):
        r = self.root                           # BEGIN "PASS-DOWN" FROM THE ROOT
        if r.n == 2*self.degree - 1:            # IF ROOT IS FULL => SPLIT
            s = BTreeNode(is_leaf=False)
            self.root = s                       # CHANGING ROOT (TREE GROWS IN HEIGHT)
            s.n = 0
            s.children.append(r)                # EMPTY NEW ROOT WILL HAVE 1 CHILD - FULL OLD ROOT
            self.split_child(s, 0)              # SPLIT OLD FULL ROOT
            self.insert_non_full(s, pair)
        else:
            self.insert_non_full(r, pair)

    # INSERTING VALUE INTO TREE NODE. (ASSUMING THAT THE NODE IS NOT FULL)
    # node - NODE TO INSERT INTO
    # pair - KEY-VALUE PAIR TO INSERT IN DATABASE
    def insert_non_full(self, node, pair):
        # FIND INDEX OF FIRST SMALLER KEY IN NODE
        i = self.find_predecessor(node.keys, pair[0])
        if i < node.n and node.n > 0:
            assert node.keys[i][0] != pair[0], 'DUPLICATE KEY'

        if node.leaf:
            if i == -1:
                # i = -1 => NEW KEY WILL BE THE SMALLEST IN THE LEAF
                # IF NODE IS EMPTY => ADD VALUES TO NODE. ELSE: PUT VALUES IN THE BEGINNING OF VALUES
                node.keys[0:1] = [pair] if node.n == 0 else [pair, node.keys[0]]
            else:
                # INSERT VALUE AFTER FIRST SMALLER KEY
                node.keys[i:i + 1] = [node.keys[i], pair]
            node.n += 1
        else:
            i += 1
            # IF NEXT NODE (TO OPERATE ON) IS FULL => SPLIT IT
            if node.children[i].n == 2*self.degree - 1:
                self.split_child(node, i)
                if pair[0] > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], pair)

    # REMOVE KEY-VALUE PAIR FROM THE TREE
    # key - KEY TO SEARCH
    # node - NODE TO SEARCH IN
    def remove_key(self, key, node=None):
        if node is None: node = self.root
        # FIND FIRST SMALLER KEY IN NODE
        pred_index = self.find_predecessor(node.keys, key)

        while True:
            if node.leaf:
                # IF NODE IS A LEAF => IF VALUE WAS FOUND IN LEAF => DELETE IT

                if node.n > 0 and node.keys[pred_index][0] == key:
                    node.keys = [*node.keys[:pred_index], *node.keys[pred_index + 1:]]
                    node.n -= 1
                return
            elif node.keys[pred_index][0] == key:
                # IF VALUE WAS FOUND IN INTERNAL NODE => USE ONE OF THREE DELETION-METHODS
                # (USE RIGHT/LEFT/BOTH CHILDREN IF THEY HAVE ENOUGH KEYS)

                if node.children[pred_index].n >= self.degree:
                    self.change_to_predecessor(node, pred_index)
                elif node.children[pred_index + 1].n >= self.degree:
                    self.change_to_successor(node, pred_index)
                else:
                    self.combine_children(node, pred_index)
            elif node.children[pred_index + 1].n < self.degree:
                # NEXT NODE DOES NOT HAVE ENOUGH KEYS TO DELETE FROM IT => EXTEND IT

                self.maximize_child(node, pred_index + 1)
                if len(self.root.keys) == 0:
                    self.root = node = node.children.pop()
                pred_index = self.find_predecessor(node.keys, key)
            else: break

        # NEXT NODE HAS ENOUGH KEYS TO DELETE FROM IT => RECURSION TO IT
        self.remove_key(key, node if key in node.keys else node.children[pred_index + 1])


    # EXTEND CHILD WITH INDEX i
    # node - NODE WHICH CONTAINS CHILD TO EXTEND
    # i - INDEX OF CHILD TO EXTEND
    def maximize_child(self, node, i):
        if i - 1 >= 0 and node.children[i - 1].n >= self.degree:
            # IF CHILD (i - 1) EXISTS AND HAS ENOUGH KEYS FOR CHANGING:

            extra_key = node.keys[i - 1]
            self.change_to_predecessor(node, i - 1)
            node.children[i].keys = [extra_key, *node.children[i].keys]
            node.children[i].n += 1
            if not node.children[i].leaf:
                node.children[i].children.insert(0, node.children[i - 1].children.pop())
        elif i + 1 <= len(node.children) - 1 and node.children[i + 1].n >= self.degree:
            # IF CHILD (i + 1) EXISTS AND HAS ENOUGH KEYS FOR CHANGING:

            extra_key = node.keys[i]
            self.change_to_successor(node, i)
            node.children[i].keys.append(extra_key)
            node.children[i].n += 1
            if not node.children[i].leaf:
                node.children[i].children.append(node.children[i + 1].children.pop(0))
        else:
            # IF BOTH CHILDREN HAS LESS THAN (DEGREE) KEYS => MERGE THEM

            node.children[i].n += 1
            if i - 1 >= 0:
                node.children[i].keys.insert(0, node.keys[i - 1])
                self.combine_children(node, i - 1)
            else:
                node.children[i].keys.append(node.keys[i])
                self.combine_children(node, i)

    # FINDING FIRST VALUE IN NODE KEYS, THAT IS SMALLER THAN VALUE
    def find_predecessor(self, keys, value):
        i = len(keys) - 1
        while i >= 0 and keys[i][0] > value:
            i -= 1

        return i

    # CHANGE KEY i IN NODE TO FIRST SMALLER VALUE IN TREE (LAST KEY IN NODE`S CHILD i)
    def change_to_predecessor(self, node, i):
        predecessor = node.children[i]
        node.keys[i] = predecessor.keys[len(predecessor.keys) - 1]
        predecessor.n -= 1
        predecessor.keys = predecessor.keys[0:-1]

    # CHANGE KEY i IN NODE TO FIRST BIGGER VALUE IN TREE (FIRST KEY IN NODE`S CHILD i + 1)
    def change_to_successor(self, node, i):
        successor = node.children[i + 1]
        node.keys[i] = successor.keys[0]
        successor.n -= 1
        successor.keys = successor.keys[1:]

    # MERGE TO CHILDREN OF NODE INTO ONE, WITH MEDIAN VALUE BETWEEN THEM
    # (MEDIAN VALUE - NODE'S KEY, WHICH WAS SEPARATING THEM)
    # node - PARENT OF NODES TO MERGE
    # i - INDEX OF CHILD TO EXTEND (RESPECTIVELY (i + 1) - CHILD WHICH WILL BE MERGED)
    def combine_children(self, node, i):
        node.n -= 1
        node.keys[i:] = node.keys[i + 1:]
        extend_child, merge_child = node.children[i], node.children[i + 1]

        # MERGE I AND I+1 CHILDREN OF NODE INTO ONE CHILD (DELETING i + 1 CHILD INCLUDED)
        extend_child.n += merge_child.n
        extend_child.keys[extend_child.n:] = merge_child.keys
        if not extend_child.leaf: extend_child.children += merge_child.children
        node.children[i + 1:] = node.children[i + 2:]

    # PRINTING TREE STRUCTURE
    def print_tree(self, node, level=0):
        print(level * '\t', f' {len(node.keys)} items', end=': ')
        for k in node.keys:
            print(k, end=' ')
        print()
        if len(node.children) > 0:
            for c in node.children:
                self.print_tree(c, level + 1)
