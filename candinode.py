class CandiNode:
    def __init__(self, smgr, snode, val, prv_cnode=None):
        self.smgr = smgr
        self.val = val
        self.prv = prv_cnode
        self.psnode = snode.parent
        self.ch = snode.chdic[val]
        self.tnode = self.ch['tnode']
        self.reset()  # reset self.pvs=full, and self.next==None

    def reset(self):
        if self.psnode != None:
            self.pvs = self.ch['parent-ch-keys'][:]
        self.next = None

    def find_next(self):
        if len(self.pvs) == 0:
            pass

        pchdic = self.tnode.holder.parent.chdic
        pv = self.p

    def find_candi(self, sat_array=None):
        if sat_array == None:
            sat_array = []

        succ = True
        for sat in sat_array[1:]:
            if not self.tnode.check_sat(sat):
                return None

        sat_array.insert(0, self.ch['hsat'])

        if self.psnode == None:
            return sat_array

        pv = self.pvs.pop(0)
        if self.next == None:
            self.next = CandiNode(self.smgr, self.psnode, pv, self)
        return self.next.find_candi(sat_array)
