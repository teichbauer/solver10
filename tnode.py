from basics import verify_sat, oppo_binary
from restrict import Restrict


class TNode:
    def __init__(self, vk12dic, t_sh):
        self.vkdic = vk12dic
        self._sort12()
        self.t_sh = t_sh
        self.restrict = Restrict(t_sh)
        self.bmap = {}
        self.set_bmap()
        self._proc_vk2s()
        self._proc_vk2s()

    def _proc_vk2s(self):
        sames = []
        oppos = []
        kns = self.kn2s[:]
        vk = self.vkdic[kns.pop()]
        bs = vk.bits
        while len(kns) > 0:
            for kn in kns:
                vkx = self.vkdic[kn]
                if vk.bits == vkx.bits:
                    if vk.dic[bs[0]] == vkx.dic[bs[0]]:
                        if vk.dic[bs[1]] == vkx.dic[bs[1]]:
                            sames.append(vkx.kname)
                        else:
                            oppos.append()

    def _proc_vk1s(self):
        for kn1 in self.kn1s:
            vk1 = self.vkdic[kn1]
            bit = vk1.bits[0]
            val = vk1.dic[bit]
            lst = self.bmap[bit]
            ind = 0
            while ind < len(lst):
                if lst[ind][0] == kn1 or lst[ind][1] != val:
                    ind += 1
                else:  # vk(not vk1) on the same bit, with the same val
                    self.vkdic.pop(lst[ind][0])
                    lst.pop(ind)
            # a vk1 makes a conditional-conflict entry
            self.restrict.add_cconflict((bit, val))

    def _sort12(self):
        self.kn1s = []
        self.kn2s = []
        for kn, vk in self.vkdic.items():
            if vk.nob == 1:
                self.kn1s.append(kn)
            else:
                self.kn2s.append(kn)

    def set_bmap(self):
        for kn, vk in self.vkdic.items():
            for b, v in vk.dic.items():
                lst = self.bmap.setdefault(b, [])
                lst.append((kn, v))
        self._proc_vk2s()
    # end of set_bmap ----------------------------------------

    def check_sat(self, sdic):
        return verify_sat(self.vkdic, sdic)

    def find_candis(self, pchmgr, pvs, candis):
        pass

    def compatible_with(self, higher_tnode, restrict=None):
        return restrict
