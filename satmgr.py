from basics import verify_sat

class SatManager:
    def __init__(self):
        self.sats = []

    def resolve(self, hnode, lnode):
        sats = []
        crmgr = hnode.crwnmge
        if lnode.done:
            csats = lnode.sh.fullsat_gen()
        else:
            csats = lnode.csats
        for tsat in csats:
            for val, vk12dic in crmgr.chdic.items():
                if verify_sat(vk12dic, tsat):
                    pass
            sats += hnode.crwnmgr.resolve(tsat)
        hnode.next = None
        hnode.sats = sats
        if hnode.parent:
            self.resolve(hnode.parent, hnode.sats)
        else:
            self.sats = hnode.sats
