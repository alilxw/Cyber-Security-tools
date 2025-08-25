import argparse
import validators
import requests
import yaml
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment

parser = argparse.ArgumentParser(description='THE Kratos HTML VULNERABILITY 1.0')

parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument('url', type=str, help='THE URL OF THE HTML TO ANALYZE')
parser.add_argument('--config', help='Path to Configuration file')
parser.add_argument('-o', '--output', help='Report file output path')

args = parser.parse_args()
config = {'forms': True, 'comment': True, 'passwords': True}
if args.config:
    print('USING CONFIG FILE' + args.config)
    config_file = open(args.config, 'r')
    config_from_file = yaml.load(config_file)
    if config_from_file:
        config = config_from_file
        config = {**config, **config_from_file}

report = ''
header = ''
url = args.url

if validators.url(url):
    result_html = requests.get(url).text
    parsed_html = BeautifulSoup(result_html, 'html.parser')

    forms = (parsed_html.find_all('form'))
    comments = parsed_html.find_all(string=lambda text: isinstance(text, Comment))
    password_inputs = parsed_html.find_all('input', {'name': 'password'})

    for form in forms:
        if (form.get('action').find('https') < 0) and (urlparse(url).scheme != 'https'):
            report += 'Form Issue: insecure form found in document \n' + form.get('action') + ' found in document\n'

    for comment in comments:
        if comment.find('key: ') > -1:
            report += 'Comment Issue: Key is found in the HTML Comments , please remove it\n'
    for password_inputs in password_inputs:
        if password_inputs.get('type') != 'password':
            report += 'input issue : Plain text password input found , please secure your code'
else:
    print('INVALID URL , please include a full URL')

if report == '':
    report += ' CONGRATULATIONS ! YOU HTML CODE IS SECURE !!!!'
else:
    header = 'Vulnerability report is as follows:'
    header += '#==================================#'

print(header + report)

if args.output:
    f = open(args.output, 'w')
    f.write(report)
    f.close()
    print('report saved to :' + args.output)
