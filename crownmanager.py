from basics import filter_sdic, unite_satdics, oppo_binary, verify_sat


class CrownManager:
    def __init__(self, satnode, sh, nov):
        self.satnode = satnode
        self.parent = None  # crwnmgr of one level higher
        if satnode.parent:
            self.parent = satnode.parent.crwnmgr
        self.sh = sh
        self.nov = nov
        self.state = 0
        # after tx_vkm.morph, tx_vkm only has (.vkdic) vk3 left, if any
        # and nov decreased by 3
        # {vk12dic:{}, parent-ch-keys:[], hsat:{}}
        self.chdic = satnode.tx_vkm.morph(satnode.topbits)
        self.set_restrict()

    def set_restrict(self):
        if self.satnode.parent:
            for val in self.chdic.keys():
                hsat = self.satnode.sh.get_sats(val)
                self.chdic[val]['hsat'] = hsat
                pvs = []
                for v, ch in self.parent.chdic.items():
                    if verify_sat(ch['vk12dic'], hsat, self.parent.sh):
                        pvs.append(v)
                if len(pvs) > 0:
                    # self.psearch_dic[val] = pvs
                    self.chdic[val]['parent-ch-keys'] = pvs

    def build_sat(self, satmgr):
        pass
