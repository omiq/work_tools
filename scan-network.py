import sys
import nmap
nm = nmap.PortScanner()
nm.scan('10.0.1.0/24', '22')

for host in sorted(nm.all_hosts()):

    vendor = ""

    if len(nm[host]['vendor']) > 0:

        try:
            mac = nm[host]['addresses']['mac']
        except:
            mac = ""

        vendor = tuple(nm[host]['vendor'].values())
        if str(vendor).find('Raspberry') > 0:
            vendor = "Pi!"
            sys.stdout.write(u"\u001b[41;1m" + "{} ({}) {}\n\u001b[0m".format(nm[host].hostname(), host, mac))
        else:
            vendor = ""
            sys.stdout.write(u"\u001b[40;1m" + "{} ({}) {}\n\u001b[0m".format(nm[host].hostname(), host, mac))

