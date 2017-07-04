from urllib import request, parse

req = request.Request(
    'https://passport.baidu.com/v2/?\
     regphonecheck&token=92f62c492cdb16d85026bf3497ccc6d7&tpl=mn&apiver=v3&\
     tt=1498793732041&phone={}&countrycode=&gid=9D4CE3F-EAA5-4B75-B160-4051120FF598&\
     exchange=0&isexchangeable=1&callback=bd__cbs__8uwa5j')
req.add_header(
    'Content-Type', 'text/html')
req.add_header(
    'Cookie', 'UBI=fi_PncwhpxZ%7ETaJcyutrgsBUkpgB3FJUSeV; HOSUPPORT=1; nocaptcha_hit=; Hm_lvt_90056b3f84f90da57dc0f40150f005d5=1498805655; Hm_lpvt_90056b3f84f90da57dc0f40150f005d5=1498805655; FP_UID=3c5f6c5f5246246aa4577bfa20b78d15; BAIDUID=F61E3BA610231EBAA33E0B2CA0E39F7E:FG=1; PSTM=1498808106; BIDUPSID=D4E83E84E6A2208F63BE1733F751E07E; PSINO=3; H_PS_PSSID=1455_21117_22074; BDORZ=FFFB88E999055A3F8A630C64834BD6D0')
req.add_header(
    'Referer', 'https://passport.baidu.com/v2/?reg&tt=1498805651922&gid=512E08E-92BC-4765-AF2F-70676643B1CA&tpl=mn&u=https%3A%2F%2Fwww.baidu.com%2F')
req.add_header(
    'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
# req.add_header('X-Requested-With', 'XMLHttpRequest')
data = parse.urlencode(
    {'regphonecheck': '',
     'token': '92f62c492cdb16d85026bf3497ccc6d7',
     'tpl': 'mn',
     'apiver': 'v3',
     'tt': '1498793732041',
     'phone': '',
     'countrycode': '',
     'gid': 'DE18DF6-9A7D-48D7-9586-289EC28DB8EE',
     'exchange': '0',
     'isexchangeable': '1',
     'callback': 'bd__cbs__lspaww'})
data = data.encode('ascii')

with request.urlopen(req, data) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print(f.read().decode('utf-8'))
