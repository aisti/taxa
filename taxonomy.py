
class Taxon(object):

    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.parent = parent
        self.description = None
        self.level = None
        self.gallery = []
        self.properties = {}

    def add_child(self, taxon):
        self.children.append(taxon)
        taxon.parent = self

    def lineage(self):
        p = self.parent.lineage() if self.parent else ""
        return f"{p}/{self.name}"

    def __str__(self):
        s = f"{self.name}"
        if self.description:
            s += f": {self.description}"
        return s


class Taxonomy(object):

    def __init__(self, root_taxon):
        self.root = root_taxon
