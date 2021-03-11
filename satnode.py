from basics import topbits, filter_sdic, unite_satdics, print_json
from basics import vkdic_sat_test, vkdic_remove
from vklause import VKlause
from satholder import SatHolder
from TransKlauseEngine import TxEngine
from vkmgr import VKManager
from childmanager import ChildManager


class SatNode:
    def __init__(self, parent, sh, vkm):
        self.parent = parent
        self.sh = sh
        self.vkm = vkm
        self.nov = vkm.nov
        self.name = f'sn{self.nov}'
        self.sats = None
        self.topbits = topbits(self.nov, 3)
        self.next = None
        self.done = False
        if len(vkm.vkdic) == 0:
            self.sats = None  # self.sh.full_sats() all :2 means: no filter
            self.done = True
        else:
            self.prepare()

    def prepare(self):
        choice = self.vkm.bestchoice()
        self.bvk = self.vkm.vkdic[choice['bestkey'][0]]
        if self.topbits != choice['bits']:  # the same as self.bvk.bits:
            self.tx = TxEngine(self.bvk)
            self.sh.transfer(self.tx)
            self.tx_vkm = self.vkm.txed_clone(self.tx)
        else:
            self.tx_vkm = self.vkm.clone()
        self.tail_varray = self.sh.spawn_tail(3)
        self.next_sh = SatHolder(self.tail_varray[:])
        self.sh.cut_tail(3)

        # ChildManager constructor will call self.tx_vkm.morph in it,
        # after tx_vkm.morph, tx_vkm only has (.vkdic) vk3 left, if any
        # and nov decreased by 3. This will be used in spawning self.next
        self.chmgr = ChildManager(self, self.next_sh.clone())
        # self.next_stuff = (next_sh.clone(), self.tx_vkm)
    # end of def prepare(self):

    def spawn(self):
        if self.done:
            return self.sats
        # after morph, vkm.vkdic only have vk3s left, if any
        if len(self.chmgr.chdic) == 0:
            self.sats = None
            self.done = True
            return None

        self.next = SatNode(self, self.next_sh, self.tx_vkm)
        return self.next

    def verify_tail_sat(self, vkdic, sat):
        for vk in vkdic.values():
            Skip = False
            for b, v in vk.dic.items():
                key = self.tail_varray[b]
                if sat[key] != v:
                    Skip = True
                    break
            if not Skip:
                return False
        return sat
