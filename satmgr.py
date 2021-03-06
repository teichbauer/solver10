from basics import verify_sat, set_bit


class SatManager:
    def __init__(self):
        self.sats = []
        self.limit = 10

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
