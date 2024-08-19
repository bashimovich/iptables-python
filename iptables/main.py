
class Iptables:
    def __init__(self, id, rule_id, pkts, bytes, target, prot, opt, inn, out, source, destination, p, dport, chain):
        self.id = id
        self.rule_id = rule_id
        self.pkts = pkts
        self.bytes = bytes
        self.target = target
        self.prot = prot
        self.opt = opt
        self.inn = inn
        self.out = out
        self.source = source
        self.destination = destination
        self.p = p
        self.dport = dport
        self.chain = chain
