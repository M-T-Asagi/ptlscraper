from urllib import request, error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import sleep
import math

def base_str(n, radix):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"

    def num_check(attr, i):
        try:
            return int(i)
        except:
            raise ValueError('invalid %s : %s' % (attr, i))

    n = num_check('n', n)
    radix = num_check('radix', radix)

    if not 1 < radix < 37:
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

url_base = "http://p.tl/"
base_netloc = "p.tl"

count = 0
index = 0
errorCount = 0

while count < 8886484:
    if errorCount > 100:
        break

    i = index
    index += 1
    errorCount += 1
    number = base_str(i, 36).zfill(4)
    url = url_base + number
    try:
        res = request.urlopen(url)
    except (error.URLError, error.HTTPError) as e:
        print('Error! "' + url + '" is ' + str(e))
        continue

    data = res.read()
        
    if urlparse(res.url).netloc == base_netloc:
        try:
            soup = BeautifulSoup(data, "html.parser")
        except Exception as e:
            print('Error! "' + url + '" is ' + str(e))
            continue

        print('Success! "' + url + '" is converted from "' + soup.find("a", class_="jump").get("href") + '"')
    else:
        print('Success! "' + url + '" is converted from "' +  res.url + '"')

    count += 1
    errorCount = 0
    sleep(0.001)

print("all of process are finished.")