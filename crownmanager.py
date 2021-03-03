from basics import filter_sdic, unite_satdics, oppo_binary, verify_sat


class CrownManager:
    def __init__(self, satnode, sh, nov):
        self.satnode = satnode
        self.raw_crown_dic = None
        self.psearch_dic = {}
        self.sh = sh
        self.nov = nov
        self.state = 0

    def set_restrict(self):
        if self.raw_crown_dic and self.satnode.parent:
            p_crown_dic = self.satnode.parent.raw_crown_dic
            for val in self.raw_crown_dic.keys():
                hsat = self.satnode.sh.get_sats(val)
                pvs = []
                for v, vk12dic in p_crown_dic.items():
                    if verify_sat(vk12dic, hsat):
                        pvs.append(v)
                if len(pvs) > 0:
                    self.psearch_dic[val] = pvs


    def build_sat(self, satmgr):
        pass

