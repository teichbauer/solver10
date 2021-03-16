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
        if tail_vk:
            if not self.vk12mgr.add_vk(tail_vk):
                return False

    def solve(self, filter_dic, tnodes):
        if len(self.vk12mgr.vkdic) > 0:
            self.reset()

        for tn in tnodes:
            print(f'add vks from {tn.name}')
            for kn, vk in tn.vkdic.items():
                if not self.add_vk(filter_dic, vk, tn.t_sh):
                    # returned: vk12mgr.valid (is False)
                    break
        if self.vk12mgr.valid:
            pass
