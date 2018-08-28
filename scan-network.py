import sys
import nmap
import time
nm = nmap.PortScanner()
nm.scan('10.0.1.0/24', '22')

# clear screen
sys.stdout.write(u"\u001b[2J\u001b[0;0H")
sys.stdout.flush()
time.sleep(0.2)

# iterate over the hosts on the network
for host in sorted(nm.all_hosts()):

    # blank if not Pi
    vendor = ""

    if len(nm[host]['vendor']) > 0:

        # attempt to get mac address
        try:
            mac = nm[host]['addresses']['mac']
        except:
            mac = ""

        vendor = tuple(nm[host]['vendor'].values())
        if str(vendor).find('Raspberry') > 0:
            vendor = "Pi!"
            print(u"\u001b[37m" + "{} ({}) {}\u001b[0m".format(nm[host].hostname(), host, mac))
        else:
            vendor = ""
            print(u"\u001b[0m" + "{} ({}) {}\u001b[0m".format(nm[host].hostname(), host, mac))

