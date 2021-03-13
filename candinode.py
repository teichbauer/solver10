class CandiNode:
    def __init__(self, smgr, snode, prv_cnode=None):
        self.smgr = smgr
        self.prv = prv_cnode
        self.picks = list(snode.chdic.keys())
        self.snode = snode
        self.reset()  # reset self.pvs=full, and self.next==None

    def reset(self):
        self.pv_dic = {}
        if self.snode.parent != None:
            for v in self.snode.chdic:
                self.pv_dic[v] = self.snode.chdic[v].pvs[:]
        self.next = None

    def find_candi(self, candis, sat_array=None):
        if len(self.picks) == 0:
            return True

        while len(self.picks) > 0:
            self.val = self.picks.pop(0)
            allowed = self.prv == None or \
                self.val in self.prv.ch.pvs
            if allowed:
                break

        if not allowed:
            return len(self.picks) == 0

        self.ch = self.snode.chdic[self.val]

        if sat_array == None:
            sat_array = []

        succ = True
        for sat in sat_array[1:]:
            succ = self.ch['tnode'].check_sat(sat)
            if not succ:
                break
        if not succ:
            self.find_candi(candis, sat_array)

        new_array = sat_array[:]

        new_array.insert(0, self.ch['hsat'])

        if self.snode.parent == None:
            candis.append(new_array)
            return len(self.picks) == 0

        if self.next == None:
            self.next = CandiNode(
                self.smgr,
                self.snode.parent,
                self)
        _end = False
        while not _end:
            _end = self.next.find_candi(candis, new_array)

        return len(self.pick) == 0

    def name(self, val):
        return f'{self.snode.name}.{val}'
