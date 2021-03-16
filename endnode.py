from vk12mgr import VK12Manager


class EndNode:
    def __init__(self, parent, sh):
        self.parent = parent
        self.sh = sh
        self.nov = sh.ln
        self.vk12mgr = VK12Manager(self.nov)
        self.reset()

    def reset(self):
        self.vk12mgr.reset()
        self.sats = []

    def add_vk(self, satfilter, vk, sh):
        tail_vk = vk.filter_hit(satfilter, sh, self.nov)
        added = False
        if tail_vk:
            added = self.vk12mgr.add_vk(tail_vk)
        return added

    def solve(self, filter_dic, tnodes):
        if len(self.vk12mgr.vkdic) > 0:
            self.reset()

        for tn in tnodes:
            print(f'add vks from {tn.name}')
            for kn, vk in tn.vkdic.items():
                added = self.add_vk(filter_dic, vk, tn.t_sh)
                msg = vk.kname + [' not added', ' added'][added]
                print(msg)
                if not self.vk12mgr.valid:
                    return False
        self.chdic = self.vk12mgr.morph()
        for v, enode in self.chdic.items():
            if enode.resolve():
                pass
        return True
