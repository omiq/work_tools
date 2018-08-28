import sys
import nmap
nm = nmap.PortScanner()
nm.scan('10.0.1.0/24', '22')

for host in sorted(nm.all_hosts()):

    vendor = ""

    if len(nm[host]['vendor']) > 0:
        mac = tuple(nm[host]['vendor'].keys())
        vendor = tuple(nm[host]['vendor'].values())
        if str(vendor).find('Raspberry'):
            vendor = "Pi!"
            sys.stdout.write(u"\u001b[41;1m" + "{} {}\u001b[40;1m".format(nm[host].hostname(), host))
        else:
            vendor = ""
            print('{} ({}): {}'.format(nm[host].hostname(), host))

