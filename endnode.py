class EndNode:
    def __init__(self, parent, sh):
        self.parent = parent
        self.sh = sh
        self.nov = sh.ln
        self.reset()

    def reset(self):
        self.vkdic = {}
        self.sats = []

    def add_vk(self, satfilter, vk):
        if vk.filter_hit(satfilter):
            tvk = vk.clone_tail(seld.sh.varray, self.nov)
        if tvk:
            self.vkdic[tvk.kname] = tvk

    def solve(self, filter_dic, tnodes):
        for tn in tnodes:
            print(f'add vks from {tn.name}')
            for kn, vk in tn.vkdic.items():
                self.add_vk(filter_dic, vk)
