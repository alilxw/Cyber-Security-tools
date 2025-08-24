import requests
import pyfiglet

ascii_banner = pyfiglet.figlet_format("Directory scanner by ali")
print(ascii_banner)

target_url = input('[*] Enter target URL: ')
file_name = input('[*] Enter directory containing file: ')


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


file = open(file_name, 'r')
for line in file:
    directory = line.strip()
    full_url = target_url + '/' + directory
    response = request(full_url)
    if response:
        print('[*] Discovered directory at this path :' + full_url)
