# eforms page element id map

from dotmap import DotMap


class Page(DotMap):
    def __init__(self, elements=dict()):
        self.elements = DotMap(elements)
        super().__init__()

    def __getattr__(self, name):
        return self.elements[name]

    def __setattr__(self, name, value):
        if name == 'elements':
            self.elements = value
        else:
            self.elements[name] = value
