from basics import verify_sat, set_bit


class SatManager:
    def __init__(self):
        self.sats = []
        # candis: list of tuples.
        # each tuple: ([<ch>,<ch>,..], <tsat-dic>), where
        # ch is an entry in childmgr.chdic:
        #   {'tnode':<tnode>, 'hsat':{,,}, 'parent-ch-keys':[1,2,..]}
        # tsat-dic is a dict, for restricting tail-part of the sh:
        #   key:bit/var, value: 0,1 or 2(wild-card)
        self.candis = []
        self.satpaths = {}
        self.limit = 10

    def build_candis(self, snode):
        for val, ch in snode.chmgr.chdic.items():
            pvs = ch['parent-ch-keys']
            ch['tnode'].find_candis(snode.chmgr.parent, pvs, self.candis)

    def convert_sat(self, candi):
        sat = {}
        return sat

    def build_solutions(self, snode):
        self.build_candis(snode)
        for candi in candis:
            sat = self.convert_sat(candi)
            self.sats.append(sat)

    def build_solutions0(self, snode, path=None, vals=None, vk12dic=None):
        if snode == None:
            return
        if path == None:
            vals = snode.chmgr.chdic.keys()
            # setup start-points
            for val in vals:
                ch = snode.chmgr.chdic[val]
                # self.satpaths[val] = {
                pth = {
                    'hsat': ch['hsat'].copy(),
                    'tsat_keys': snode.next.sh.varray,
                    'tsat': {}
                }
                pvs = ch['parent-ch-keys']
                res = self.build_solutions(
                    snode.parent,
                    pth,
                    pvs,
                    ch['vk12dic']
                )
                if res:
                    self.satpaths[val] = pth
        else:
            scnt = 0
            for val in vals:
                ch = snode.chmgr.chdic[val]

                if self.check_conflict(vk12dic, ch['vk12dic'], path):
                    self.collect(ch, path)
                    res = self.build_solutions(
                        snode.parent,
                        path,
                        ch['parent-ch-keys'],
                        ch['vk12dic']
                    )
                    if res:
                        scnt += 1
                        if snode.parent == None:
                            self.sats.append(
                                {*path['hsat'], *path['tsat']}
                            )
            return scnt > 0

    def check_conflict(self, vk12dic0, vk12dic1, path):
        pass

    def collect(self, ch, path):
        pass

    def sat_val(self, sat):
        value = 0
        for b, v in sat.items():
            value = set_bit(value, b, v)
        return value

    def resolve(self, hnode, lnode):
        chmgr = hnode.chmgr
        if lnode.done:
            gen = lnode.sh.val_gen()
            sat = lnode.sh.next_sat(gen)
            while sat and len(self.sats) < self.limit:
                self.collect_sats(chmgr, sat)
                sat = lnode.sh.next_sat(gen)
        else:
            for sat in lnode.csats:
                if not self.collect_sats(chmgr, sat):
                    break

    def collect_sats(self, chmgr,
                     test_sat,
                     candis=None):
        rsat = test_sat.copy()
        vksat = chmgr.sh.reverse_sdic(rsat)
        for val, ch in chmgr.chdic.items():
            if candis == None or val in candis:
                if verify_sat(ch['vk12dic'], vksat):
                    rsat.update(ch['hsat'])
                    if chmgr.parent == None:
                        self.sats.append(rsat)
                        if len(self.sats) >= self.limit:
                            print('limit reached')
                            return False
                    else:
                        go_on = self.collect_sats(
                            chmgr.parent,
                            rsat,
                            ch['parent-ch-keys'])
                        if not go_on:
                            return False
        return True
