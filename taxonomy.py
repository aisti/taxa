import os


class Taxon(object):

    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.description = None
        self.level = 1
        self.gallery = []
        self.properties = {}
        self.parent = None
        if parent:
            parent.add_child(self)

    def set_parent(self, parent_taxon):
        self.parent = parent_taxon
        self.level = parent_taxon.level + 1

    def add_child(self, child_taxon):
        self.children.append(child_taxon)
        child_taxon.set_parent(self)

    def lineage(self):
        p = self.parent.lineage() if self.parent else ""
        return f"{p}/{self.name}"

    def depth(self):
        if self.parent:  # recur
            return 1 + self.parent.depth()
        else:  # root is depth=1
            return 1

    def __str__(self):
        s = f"{self.name}"
        if self.description:
            s += f": {self.description}"
        return s


class Taxonomy(object):

    def __init__(self, root_taxon):
        self.root = root_taxon

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as fh:
            previous_depth = -1
            previous_taxon = None
            taxonomy = None
            for line in fh:
                if line.strip().startswith('#') or line.strip() == '':
                    continue

                parent = previous_taxon
                indent = 0
                while line.startswith(' '):
                    indent += 1
                    line = line[1:]
                line = line.strip()

                i = indent
                while i <= previous_depth:
                    parent = parent.parent
                    i += 1

                taxon = Taxon(line, parent)
                previous_taxon = taxon
                previous_depth = indent
                if indent == 0:
                    taxonomy = Taxonomy(taxon)

        return taxonomy

    def __str__(self):
        nodes = [self.root]
        node_strings = []
        while nodes:
            current_node = nodes.pop(0)
            node_strings.append(current_node.lineage())
            nodes.extend(current_node.children)
        return "\n".join(sorted(node_strings))


if __name__ == "__main__":
    t = Taxonomy.load(os.path.join(__file__, '..', 'resources', 'test.txt'))
    print(t)
