from basics import topbits, filter_sdic
from TransKlauseEngine import TxEngine
from vk12mgr import VK12Manager
from satholder import SatHolder


class Node12:
    def __init__(self, vname, parent, vk12m, sh, hsat):
        self.parent = parent
        self.hsat = hsat
        # vname//100:nov, (vname%100)//10:nob,  vname%10:val
        self.vname = vname
        self.nexts = []
        self.sh = sh
        if type(vk12m) == type([]):  # when vk12m is a list of dict(full-sats)
            self.sats = vk12m        # save the full-sats
            self.nov = len(vk12m)
            self.state = 2           # this will trigger collect_sats() call
        else:  # vk12m is of type VK12Manager
            self.vk12m = vk12m
            self.nov = vk12m.nov

            self.state = 0
            if self.nov <= 3:  # for nov=3 or less: get all sats by looping
                self.sats = self.nov321_sats()

    def next_sat(self):
        if self.sat_cur < len(self.sats):
            sat = {**self.hsat, **self.sats[self.sat_cur]}
            self.sat_cur += 1
            return sat
        return None

    def nov321_sats(self):   # when nov==3,2,1, collect integer-sats
        nsats = []
        vkdic = self.vk12m.vkdic
        N = 2 ** self.nov
        for i in range(N):  # 2** nov
            hit = False
            for vk in vkdic.values():
                if vk.hit(i):
                    hit = True
                    break
            if not hit:
                nsats.append(i)
        ln = len(nsats)
        if ln == 0:
            self.suicide()
        else:
            self.sats = [self.sh.get_sats(si) for si in nsats]
            self.state = 2
        return self.sats
    # end of def nov3_sats(self):
