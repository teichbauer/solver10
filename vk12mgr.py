from vklause import VKlause
from basics import topvalue, topbits, topbits_coverages


class VK12Manager:
    def __init__(self, nov):
        self.nov = nov

    def reset(self):
        self.bdic = {}
        self.vkdic = {}
        self.kn1s = []
        self.kn2s = []
        self.valid = True  # no sat possible/total hit-blocked
        self.info = {}

    def add_vk(self, vk):
        if vk.nob == 1:
            bit = vk.bits[0]
            if bit in self.bdic and len(self.bdic[bit]) > 0:
                kns = self.bdic[bit][:]
                for kn in kns:
                    if kn in self.kn1s:
                        if self.vkdic[kn].dic[bit] != vk.dic[bit]:
                            self.valid = False
                            msg = f'vk1:{vk.kname} vs {kn}: valid: {self.valid}'
                            self.info[vk.kname] = msg
                            print(msg)
                            return False
                        else:  # self.vkdic[kn].dic[bit] == vk.dic[bit]
                            msg = f'{vk.kname} duplicated with {kn}'
                            self.info[vk.kname] = msg
                            print(msg)
                            return False
                    elif kn in self.kn2s:
                        if self.vkdic[kn].dic[bit] == vk.dic[bit]:
                            # a vk2 has the same v on this bit: remove vk2
                            msg = f'{vk.kname} removes {kn}'
                            self.info[vk.kname] = msg
                            print(msg)
                            self.kn2s.remove(kn)
                            vkn = self.vkdic.pop(kn)
                            for b in vkn.bits:
                                self.bdic[b].remove(kn)
            # add the vk
            self.vkdic[vk.kname] = vk
            self.kn1s.append(vk.kname)
            self.bdic.setdefault(bit, []).append(vk.kname)
            return True
        elif vk.nob == 2:
            # if an existin vk1 covers vk?
            for kn in self.kn1s:
                b = self.vkdic[kn].bits[0]
                if b in vk.bits and self.vkdic[kn].dic[b] == vk.dic[b]:
                    # vk not added. but valid is this still
                    msg = f'{vk.kname} blocked by {kn}'
                    self.info[vk.kname] = msg
                    print(msg)
                    return False
            # find vk2s withsame bits
            pair_kns = []
            for kn in self.kn2s:
                if self.vkdic[kn].bits == vk.bits:
                    pair_kns.append(kn)
            bs = vk.bits
            for pk in pair_kns:
                pvk = self.vkdic[pk]
                if vk.dic[bs[0]] == pvk.dic[bs[0]]:
                    if vk.dic[bs[1]] == pvk.dic[bs[1]]:
                        msg = f'{vk.kname} douplicated with {kn}'
                        self.info[vk.kname] = msg
                        print(msg)
                        return False  # vk not added
                    else:  # b0: same value, b1 diff value
                        msg = f'{vk.kname} + {pvk.kname}: {pvk.kname}->vk1'
                        self.info[vk.kname] = msg
                        print(msg)
                        # remove pvk
                        self.vkdic.pop(pvk.kname)       # from vkdic
                        self.kn2s.remove(pvk.kname)     # from kn2s
                        for b in bs:                    # from bdic
                            self.bdic[b].remove(pvk.kname)
                        pvk.drop_bit(bs[1])
                        self.add(pvk)  # validity made when add vkx as vk1
                        return False   # vk not added.
                else:  # b0 has diff value
                    if vk.dic[bs[1]] == pvk.dic[bs[1]]:
                        # b1 has the same value
                        msg = f'{vk.kname} + {pvk.kname}: {pvk.kname}->vk1'
                        self.info[vk.kname] = msg
                        print(msg)
                        # remove pvk
                        self.vkdic.pop(pvk.kname)       # from vkdic
                        self.kn2s.remove(pvk.kname)     # from vk2s
                        for b in bs:                    # from bdic
                            self.bdic[b].remove(pvk.kname)

                        # add pvk back as vk1, after dropping bs[1]
                        pvk.drop_bit(bs[0])
                        return self.add_vk(pvk)
                        return False    # vk not added
                    else:  # non bit from vk has the same value as pvk's
                        pass
            for b in bs:
                self.bdic.setdefault(b, []).append(vk.kname)
            self.kn2s.append(vk.kname)
            self.vkdic[vk.kname] = vk
            return True

    def morph(self):
        return {}
