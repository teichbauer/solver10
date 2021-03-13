from basics import verify_sat, set_bit
from candinode import CandiNode


class SatManager:
    def __init__(self, start_snode):
        self.start_snode = start_snode
        self.candis = []
        self.vals = []
        self.candi_dic = {}
        for val in start_snode.chdic:
            self.candi_dic[val] = CandiNode(self, start_snode, val)
            self.vals.append(val)
        self.sats = []
        self.limit = 10
        self.done = False  # limit reached.
        self.build_candis()

    def build_candis(self):
        candis = []
        val = self.vals.pop(0)
        while True:
            candi = self.candi_dic[val].find_candi()
            if candi:
                candis.append(candi)
            else:
                if len(candis) > 0:
                    self.candis += candis

                if len(self.vals) == 0:
                    break
                candis = []
                val = self.vals.pop(0)

    def resolve(self, endnode):
        for can in self.candis:
            self.convert_sat(can, endnode)
            if self.done:  # if limit reached, done==True.
                break

    def convert_sat(self, candi, endnode):
        sat = {}
        self.sats.append(sat)
        self.done = len(self.sats) >= self.limit

    def sat_val(self, sat):
        value = 0
        for b, v in sat.items():
            value = set_bit(value, b, v)
        return value
