from basics import verify_sat, set_bit
from candinode import CandiNode


class SatManager:
    # tdic holds all tnode, under its name
    tdic = {}
    # v-dic: verif-result for less-nov tnode.hsat. fed by smgr
    vdic = {}

    def __init__(self, start_snode):
        self.start_snode = start_snode
        self.candis = []
        self.candinode = CandiNode(self, start_snode)
        self.sats = []
        self.limit = 10
        self.done = False  # limit reached.
        self.build_candis()

    def build_candis(self):
        _end = False
        while not _end:
            _end = self.candinode.find_candi(self.candis)
            break
        x = 1

    def resolve(self, endnode):
        for can in self.candis:
            self.convert_sat(can, endnode)
            if self.done:  # if limit reached, done==True.
                break

    def convert_sat(self, candi, endnode):
        filter_sat = {}
        tnodes = [self.tdic[tname] for tname in candi]
        for tn in tnodes:
            filter_sat.update(tn.hsat)
        endnode.solve(filter_sat, tnodes)

        self.sats.append(sat)
        self.done = len(self.sats) >= self.limit

    def sat_val(self, sat):
        value = 0
        for b, v in sat.items():
            value = set_bit(value, b, v)
        return value
