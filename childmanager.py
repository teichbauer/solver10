from basics import verify_sat


class ChildManager:
    def __init__(self, satnode, sh):
        self.satnode = satnode
        self.parent = None  # child-mgr of one level higher
        if satnode.parent:
            self.parent = satnode.parent.chmgr
        self.sh = sh
        self.nov = satnode.nov
        self.vk12dic = {}
        # after tx_vkm.morph, tx_vkm only has (.vkdic) vk3 left, if any
        # and nov decreased by 3
        # {vk12dic:{}, parent-ch-keys:[], hsat:{}}
        self.chdic = satnode.tx_vkm.morph(satnode.topbits, self.vk12dic)
        self.set_restrict()

    def set_restrict(self):
        for val in self.chdic.keys():
            hsat = self.satnode.sh.get_sats(val)
            self.chdic[val]['hsat'] = hsat
            if self.parent:
                vksat = self.parent.sh.reverse_sdic(hsat)
                pvs = []
                for v, ch in self.parent.chdic.items():
                    if verify_sat(ch['vk12dic'], vksat):
                        pvs.append(v)
                if len(pvs) > 0:
                    # self.psearch_dic[val] = pvs
                    self.chdic[val]['parent-ch-keys'] = pvs
