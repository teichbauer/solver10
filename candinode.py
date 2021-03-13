class CandiNode:
    def __init__(self, smgr, snode, val, prv_cnode=None):
        self.smgr = smgr
        self.val = val
        self.tnode = snode.chdic[val]['tnode']
        self.pvs = snode.chdic[val]['parent-ch-keys'][:]
        self.prv = prv_cnode
        self.cur = 0
        self.next = None

    def find_next(self):
        if len(self.pvs) == 0:

        pchdic = self.tnode.holder.parent.chdic
        pv = self.p

    def find_candi(self):
        pass
