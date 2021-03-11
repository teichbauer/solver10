# from basics import verify_sat


class ChildManager:
    def __init__(self, satnode, sh):
        self.satnode = satnode
        self.parent = None  # child-mgr of one level higher
        if satnode.parent:
            self.parent = satnode.parent.chmgr
        self.sh = sh
        self.nov = satnode.nov
        self.vk12dic = {}  # all vk12 objs ref-ed by chdic[v]['tnode']
        print(f'satnode: {satnode.name}')
        self.chdic = satnode.tx_vkm.morph(satnode, self)
        self.set_restrict()

    def set_restrict(self):
        ''' for every child C in chdic, check which children of 
            self.satnode.chdic, are compatible with C, (allows vksat)
            build a pvs containing child-keys of the children that are 
            compatible, set chdic[val]['parent-ch-keys'] = pvs
            '''
        for val in self.chdic.keys():
            hsat = self.satnode.sh.get_sats(val)
            self.chdic[val]['hsat'] = hsat
            if self.parent:
                vksat = self.parent.sh.reverse_sdic(hsat)
                pvs = []
                for v, ch in self.parent.chdic.items():
                    if ch['tnode'].check_sat(vksat):
                        # if verify_sat(ch['vk12dic'], vksat):
                        pvs.append(v)
                if len(pvs) > 0:
                    # self.psearch_dic[val] = pvs
                    self.chdic[val]['parent-ch-keys'] = pvs
