class CandiNode:
    def __init__(self, smgr, snode, prv_cnode=None):
        self.smgr = smgr
        self.prv = prv_cnode
        self.snode = snode
        self.reset()  # reset self.pvs=full, and self.next==None

    def reset(self):
        self.picks = list(self.snode.chdic.keys())
        self.next = None

    def find_candi(self, candis, sat_array=None):
        allowed = False
        while len(self.picks) > 0 and (not allowed):
            self.val = self.picks.pop(0)
            allowed = self.prv == None or \
                self.val in self.prv.ch.pvs

        if not allowed:
            return len(self.picks) == 0

        self.ch = self.snode.chdic[self.val]

        if sat_array == None:
            new_array = []
        else:
            succ = True
            if len(sat_array) > 1:
                vt = [sat_array[0]]
                ss = self.smgr.tdic[vt[0]].hsat.copy()
                for tn in sat_array[1:]:
                    vt.append(tn)
                    ss.update(self.smgr.tdic[tn].hsat)
                succ = self.ch.check_sat(ss, True)

            if not succ:
                return self.find_candi(candis, sat_array)
            new_array = sat_array[:]

        new_array.insert(0, self.ch.name)

        if self.snode.parent == None:
            candis.append(new_array)
            return len(self.picks) == 0

        if self.next == None:
            self.next = CandiNode(
                self.smgr,
                self.snode.parent,
                self)
        else:
            self.next.reset()
        _end = False
        while not _end:
            _end = self.next.find_candi(candis, new_array)

        return len(self.picks) == 0
    # end of def find_candi(self, .. )

    def name(self, val):
        return f'{self.snode.name}.{val}'
