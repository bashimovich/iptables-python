from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
from django.shortcuts import render, redirect
from .main import Iptables
from os import system
import re


chains = ["INPUT", "FORWARD", "OUTPUT"]


def interfaces():
    # system("ip link show > file/interface.txt")
    interfaces_file = open("files/interfaces.txt", 'r')
    interfaces_file_read_line = interfaces_file.readlines()
    interface = []
    for i in interfaces_file_read_line:
        if re.match(r'\d{1,2}:', i):
            i = i[:15]
            interface.append(i.split()[1])
    interfaces_file.close()
    return interface


def file_reader():
    # system("iptables -nvL > files/iptables-nvL.txt")

    file = open('files/iptables-vnL.txt', 'r')
    read_file = file.readlines()
    rule_id = 0
    id = 0
    rules = []
    chain = "Chain"
    for line in read_file:

        if len(line) != 1 or 0:
            if "pkts" not in line.split():
                pkts, bytes, target, prot, opt, inn, out, source, destination, p, dport = "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"
                name = [pkts, bytes, target, prot, opt,
                        inn, out, source, destination, p, dport]
                split_lines = []
                if "INPUT" in line.split():
                    chain = "INPUT"
                    continue
                elif "FORWARD" in line.split():
                    rule_id = 0
                    chain = "FORWARD"
                    continue
                elif "OUTPUT" in line.split():
                    rule_id = 0
                    chain = "OUTPUT"
                    continue
                rule_id = rule_id+1
                id = id+1
                for i in line.split():
                    split_lines.append(i)
                helper = 0
                for var in split_lines:
                    name[helper] = var
                    helper = helper+1
                rule = Iptables(id, rule_id, name[0], name[1], name[2], name[3],
                                name[4], name[5], name[6], name[7], name[8], name[9], name[10], chain)

                rules.append(rule)
    file.close()
    net_interfaces = interfaces()
    data = {
        'rules': rules,
        'network_interfaces': net_interfaces,
        'chains': chains
    }
    return data


@require_http_methods(["GET"])
def index(request):
    data = file_reader()
    return render(request, "iptables/index.html", data)


@require_http_methods(["GET"])
def interfaces_chain_view(request, interface, chain):
    data = file_reader()
    interface = interface.split(":")[0]
    rules = []
    for rule in data["rules"]:
        if (rule.inn == interface or rule.inn == "--" or rule.inn == "*") and rule.chain == chain:
            rules.append(rule)
    net_interfaces = interfaces()
    data = {
        'rules': rules,
        'network_interfaces': net_interfaces,
        'chains': chains
    }
    return render(request, "iptables/interfaces.html", data)


@require_http_methods(["POST"])
def delete_rule_using_no(request, chain, rule_id):
    system('iptables -D {} {}'.format(chain, rule_id))
    # system("iptables -nvL > files/iptables-nvL.txt")
    return HttpResponse("Deleted")
