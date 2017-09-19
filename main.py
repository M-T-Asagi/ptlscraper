from urllib import request, error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import sleep
import math, sys

def base_str(n, radix):
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def num_check(attr, i):
        try:
            return int(i)
        except:
            raise ValueError('invalid %s : %s' % (attr, i))

    n = num_check('n', n)
    radix = num_check('radix', radix)

    if not 1 < radix < 63:
        raise ValueError('invalid radix %s' % radix)

    is_negative = n < 0
    n = abs(n)

    result = []

    while n:
        result.insert(0, n % radix)
        n = math.floor(n / radix)
        if n == 0:
            break

    s = ''. join([digits[i] for i in result])
    if is_negative:
        s = '-' + s
    return s        

args = sys.argv
start_num = 0
use_big = False

for arg in args:
    if arg == "usebig":
        use_big = True
    elif arg.isdigit():
        start_num = int(arg)

url_base = "http://p.tl/"
base_netloc = "p.tl"

count = 0
index = start_num
error_count = 0
radix = 62 if use_big else 36

print("result, ptl, original, others")

while count < 8886484:
    if error_count > 100:
        break

    i = index
    index += 1
    error_count += 1
    number = base_str(i, radix).zfill(4)
    url = url_base + number
    try:
        res = request.urlopen(url)
    except (error.URLError, error.HTTPError, UnicodeEncodeError) as e:
        print('Failed!, ' + url + ',, ' + str(e))
        continue

    data = res.read()
        
    if urlparse(res.url).netloc == base_netloc:
        try:
            soup = BeautifulSoup(data, "html.parser")
            elem = soup.find("a", class_="jump")
        except Exception as e:
            print('Failed!, ' + url + ',, ' + str(e))
            continue
        
        if elem is not None:
            print('Success!, ' + url + ', ' + soup.find("a", class_="jump").get("href") + ',')
        else:
            print('Failed!, ' + url + ', ' +  res.url + ', invalid page')
    else:
        print('Success, ' + url + ',' +  res.url + ', ')

    count += 1
    error_count = 0
    sleep(0.001)

print("all of,  process, are, finished.")