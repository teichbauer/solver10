from vk12mgr import VK12Manager


class EndNode:
    def __init__(self, parent, sh):
        self.parent = parent
        self.sh = sh
        self.nov = sh.ln
        self.reset()

    def reset(self):
        self.vkdic = {}
        self.sats = []

    def add_vk(self, satfilter, vk, sh):
        tail_vk = vk.filter_hit(satfilter, sh, self.nov)
        if tail_vk:
            self.vkdic[vk.kname] = tail_vk

    def solve(self, filter_dic, tnodes):
        for tn in tnodes:
            print(f'add vks from {tn.name}')
            for kn, vk in tn.vkdic.items():
                self.add_vk(filter_dic, vk, tn.t_sh)
        vk12mgr = VK12Manager(self.vkdic, self.nov)
