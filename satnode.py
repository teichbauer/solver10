from basics import topbits, filter_sdic, unite_satdics, print_json
from basics import vkdic_sat_test, vkdic_remove
from satholder import SatHolder
from TransKlauseEngine import TxEngine
from endnode import EndNode


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

        self.vk12dic = {}  # store all vk12s, all tnode's vkdic ref to here
        # after tx_vkm.morph, tx_vkm only has (.vkdic) vk3 left, if any
        # and tx_vkm.nov decreased by 3, used in spawning self.next
        self.chdic = self.tx_vkm.morph(self)
        self.restrict_chs()

    # end of def prepare(self):

    def spawn(self):
        if self.done:
            return self.sats
        # after morph, vkm.vkdic only have vk3s left, if any
        if len(self.chdic) == 0:
            self.sats = None
            self.done = True
            return None
        if len(self.tx_vkm.vkdic) == 0:
            self.next = EndNode(self, self.next_sh)
        else:
            self.next = SatNode(self, self.next_sh.clone(), self.tx_vkm)
        return self.next

    def restrict_chs(self):
        ''' for every child C in chdic, check which children of 
            self.satnode.chdic, are compatible with C, (allows vksat)
            build a pvs containing child-keys of the children that are 
            compatible, set chdic[val].pvs
            '''
        del_chs = []
        for val, tnode in self.chdic.items():
            # hsat = self.sh.get_sats(val)
            hsat = tnode.hsat
            # self.chdic[val]['hsat'] = hsat
            if self.parent:
                vksat = self.parent.next_sh.reverse_sdic(hsat)
                pvs = []
                for v, tn in self.parent.chdic.items():
                    if tn.check_sat(vksat):
                        pvs.append(v)
                if len(pvs) > 0:
                    tnode.pvs = pvs
                else:
                    del_chs.append(val)
        for chval in del_chs:
            del self.chdic[chval]
