import subprocess
import re

from progress import printProgressBar

INVALID_IP_ADRESSES = ["127.0.0.1", "172.17.0.1"]


def app() :

    # execute "ifconfig" in shell
    shell = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    shell_result = shell.stdout.read().decode("utf-8")

    # execute a regex on ifconfig result to find all ip adresses
    regex_result = re.findall(r'inet (?:addr){0,1}:((?:(?:\d){1,3}.){3}(?:\d){1,3})', shell_result)

    # filter out invalid ip adresses
    local_ips= list(filter(lambda ip_adress: ip_adress not in INVALID_IP_ADRESSES, regex_result))

    # create a subnet mask according to the valid ips and try to ping each host in the subnet
    network_hosts = []
    counter = 0
    printProgressBar(counter, 50, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for local_ip in local_ips:
        subnet_mask = re.match(r'(?:[0-9]{1,3}\.){3}', local_ip).group(0)
        for i in range(1, 255):
            ip = subnet_mask + str(i)
            shell = subprocess.Popen(["ping", ip, "-c", "1"], stdout=subprocess.PIPE)

            try:
                ping_result = shell.communicate(timeout=0.05)
                network_hosts.append(ip)
            except subprocess.TimeoutExpired:
                pass

            if i % 5 == 0:
                counter += 1
                printProgressBar(counter, 50, prefix = 'Scanning Network:', length = 50)

        print(network_hosts)

if __name__ == "__main__":
    app()
