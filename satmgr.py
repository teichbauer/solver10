from basics import verify_sat

class SatManager:
    def __init__(self):
        self.sats = []
        self.limit = 2

    def resolve(self, hnode, lnode):
        crmgr = hnode.chmgr
        if lnode.done:
            csats = lnode.sh.fullsat_gen()  # iterator
        else:
            csats = lnode.csats
        for tsat in csats:
            if self.collect_sats(crmgr, tsat):
                if len(self.sats) >= self.limit:
                    print('limit reached')

    def collect_sats(self, chmgr, 
                    test_sat, 
                    candis=None):
        rsat = test_sat.copy()
        vksat = chmgr.sh.reverse_sdic(rsat)
        for val, ch in chmgr.chdic.items():
            if candis==None or val in candis:
                if verify_sat(ch['vk12dic'], vksat):
                    rsat.update(ch['hsat'])
                    if chmgr.parent == None:
                        self.sats.append(rsat)
                        return self.sats
                    else:
                        return self.collect_sats(
                                    chmgr.parent, 
                                    rsat, 
                                    ch['parent-ch-keys'])
        return None

