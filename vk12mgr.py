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
        self.invalid_info = ''

    def add_vk(self, vk):
        if vk.nob == 1:
            bit = vk.bits[0]
            if bit in self.bdic and len(self.bdic[bit]) > 0:
                kns = self.bdic[bit][:]
                for kn in kns:
                    if kn in self.kn1s:
                        if self.vkdic[kn].dic[bit] != vk.dic[bit]:
                            # kn is vk1 on the same bit, but values diff:
                            # conflict makes valid=False
                            self.invalid_info = f'vk1s:{vk.kname} vs {kn}'
                            self.valid = False
                            return False
                        # else: self.vkdic[kn].dic[bit] == vk.dic[bit]
                        #   ignore vk: a duplicate exits already
                    elif kn in self.kn2s:
                        if self.vkdic[kn].dic[bit] == vk.dic[bit]:
                            # a vk2 has the same v on this bit:
                            # delete vk2
                            self.kn2s.remove(kn)
                            del self.vkdic[kn]
                            self.bdic[bit].remove(kn)
            # add the vk
            self.vkdic[vk.kname] = vk
            self.kn1s.append(kv.kname)
            self.bdic.setdefault(bit, []).append(vk.kname)

        elif vk.nob == 2:
            # if an existin vk1 covers vk?
            for kn in self.kn1s:
                b = self.vkdic[kn].bits[0]
                if b in vk.bits and self.vkdic[kn].dic[b] == vk.dic[b]:
                    # vk not added. but valid is this still
                    return True
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
                        return True  # vk not added
                    else:  # b0: same value, b1 diff value
                        # pvk becomes vk1 on b0. vk not added

                        # remove pvk
                        vkx = self.vkdic.pop(pvk.kname)
                        self.kn2s.remove(pvk.kname)
                        for b in bs:
                            self.bdic[b]].remove(pvk.kname)

                        # vk not added. But add vkx, after dropped the bit
                        vkx.drop_bit(bs[1])
                        return self.add(vks)
                else:  # b0 has diff value
                    if vk.dic[bs[1]] == pvk.dic[bs[1]]:
                        # b1 has the same value
                        # pvk becomes vk1 on b1. vk not added

                        # remove pvk
                        vkx = self.vkdic.pop(pvk.kname)
                        self.kn2s.remove(pvk.kname)
                        for b in bs:
                            self.bdic[b]].remove(pvk.kname)

                        # add pvk, after dropping bs[1]
                        pvk.drop_bit(bs[0])
                        return self.add_vk(pvk)
                    else:
                        # non bit from vk has the same value as pvk's
                        # add vk
            for b in bs:
                self.bdic[b].append(vk.kname)
            self.kn2s.append(vk.kname)
            self.vkdic[vk.kname]= vk
            return True
