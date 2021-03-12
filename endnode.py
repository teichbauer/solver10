class EndNode:
    def __init__(self, parent, sh):
        self.parent = parent
        self.sh = sh
        self.nov = sh.ln
        self.vkdic = {}

    def add_vk(self, satfilter, vk):
        tvk = vk.clone_tail(satfilter, self.nov)
        if tvk:
            self.vkdic[tvk.kname] = tvk

    def solve(self):
        pass
