class Restrict:
    def __init__(self, sh):
        self.sh = sh
        # requires asks the value of a sdic must be the value given here.
        self.requires = {}
        # conditional_conflicts: list of (var,value) pairs (vvp)
        # when varible has that value, there is conflict
        self.conditional_conflicts = []
        # list of dics with 2 key(bit)/value-pairs.
        # if both of the values in a pair are met, it blocks
        self.block_pairs = []
        self.thru = True

    def set_cflt_condition(self, vk12dic):
        for vk in vk12dic.values():
            if vk.nob == 1:
                b = vk.bits[0]
                self.conditional_conflicts.append((b, vk.dic[b]))
            else:
                pass

    def add_cconflict(self, cdic):
        if type(cdic) == type(()):
            self.conditional_conflicts.append(cdic)
        elif type(cdic) == type({}):
            self.conditional_conflicts.append(list(cdic)[0])

    def check_conflict(self, sdic):
        if len(self.conditional_conflicts) > 0:
            for k, v in sdic.items():
                if (k, v) in self.conditional_conflicts:
                    return False
        return True

    def check_require(self, sdic):
        for k, v in sdic.items():
            if k in self.requires:
                if self.requires[k] != 2 and self.requires[k] != v:
                    return False
        return True

    def check_block_pairs(self, sdic):
        for p in self.block_pairs:
            hitcnt = 0
            for k, v in p.items():
                if k in sdic and v == sdic[k]:
                    hitcnt += 1
            if hitcnt == 2:
                return False
        return True

    def add_require(self, sdic):
        thru = self.check_require(sdic)
        if thru:
            self.requires.update(sdic)
        return thru

    def add_bpair(self, pdic):
        if pdic in self.block_pairs:
            return
        self.block_pairs.append(pdic)

    def check(self, sdic):
        return self.check_block_pairs(sdic) and \
            self.check_require(sdic) and \
            self.check_conflict(sdic)
