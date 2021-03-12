from basics import verify_sat, set_bit


class SatManager:
    def __init__(self, start_snode):
        self.start_snode = start_snode
        self.candi_dic = {}
        for val, ch in start_snode.chdic.items():
            self.candi_dic[val] = [ch['hsat']]
        # candis: list of tuples.
        # each tuple: ([<ch>,<ch>,..], <tsat-dic>), where
        # ch is an entry in childmgr.chdic:
        #   {'tnode':<tnode>, 'hsat':{,,}, 'parent-ch-keys':[1,2,..]}
        # tsat-dic is a dict, for restricting tail-part of the sh:
        #   key:bit/var, value: 0,1 or 2(wild-card)
        self.sats = []
        self.limit = 10

    def build_candi_dic(self):
        pass

    def build_candis(self, snode):
        for ch in snode.chdic.values():
            snode.parent
            pvs = ch['parent-ch-keys']
            # candi = [ch['hsat']]
            res = ch['tnode'].find_candis([ch[hsat]], snode.parent, pvs)
            if res:
                self.candis.append(candi)

    def convert_sat(self, candi):
        sat = {}
        return sat

    def build_solutions(self, snode):
        self.build_candis(snode)
        for candi in candis:
            sat = self.convert_sat(candi)
            self.sats.append(sat)

    def sat_val(self, sat):
        value = 0
        for b, v in sat.items():
            value = set_bit(value, b, v)
        return value

    def resolve(self, endnode):
        pass
