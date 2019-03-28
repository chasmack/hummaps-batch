from importlib import reload

import select_paths

RELOAD = True

if RELOAD:
    reload(select_paths)

from select_paths import SelectedPaths


class Toolbox(object):
    def __init__(self):
        self.label = "TRS Path Specs"
        self.alias = ""
        self.tools = []
        self.tools += [SelectedPaths]