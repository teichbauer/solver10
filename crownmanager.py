from basics import filter_sdic, unite_satdics, oppo_binary, verify_sat


class CrownManager:
    def __init__(self, satnode, sh, nov):
        self.satnode = satnode
        self.parent = None  # crwnmgr of one level higher
        if satnode.parent:
            self.parent = satnode.parent.crwnmgr
        self.chdic = None
        self.psearch_dic = {}
        self.sh = sh
        self.nov = nov
        self.state = 0
        # after tx_vkm.morph, tx_vkm only has (.vkdic) vk3 left, if any
        # and nov decreased by 3
        self.chdic = satnode.tx_vkm.morph(satnode.topbits)
        self.set_restrict()

    def set_restrict(self):
        if self.chdic and self.satnode.parent:
            for val in self.chdic.keys():
                hsat = self.satnode.sh.get_sats(val)
                pvs = []
                for v, vk12dic in self.parent.chdic.items():
                    if verify_sat(vk12dic, hsat, self.parent.sh):
                        pvs.append(v)
                if len(pvs) > 0:
                    self.psearch_dic[val] = pvs


    def build_sat(self, satmgr):
        pass

