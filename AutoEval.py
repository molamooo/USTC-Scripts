username = '##########'
passowrd = '******'
# save_dir = '/mnt/d/staff_pic/'

import requests
from bs4 import BeautifulSoup
# session 帮你保存cookies
session = requests.Session()

session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
# 获取页面中的随机token
page = session.get(r'https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fmis.teach.ustc.edu.cn/casLogin.do')
if not page.ok:
    print('Connection fail! error code {}'.format(page.status_code))
soup = BeautifulSoup(page.text, 'html.parser')
_token = soup.find('input', {'name' : '_token'})['value']
print(_token)

# 这里将redirect设为false，从而不自动跳转，获取ticket后可以手动跳转
# 或者允许自动跳转
session.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
r = session.post(r'https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fmis.teach.ustc.edu.cn/casLogin.do', 
                 data={'_token' : _token, 'login' : username, 'password' : passowrd, 'button' : '登录'})
if not r.ok:
    print('Login fail! error code {}'.format(r.status_code))
if '密码错误' in r.text:
    print('Login fail! wrong password')

# print(BeautifulSoup(r.text, 'html.parser'))
# print(r.headers)
# 评教页面
r = session.get(r'http://mis.teach.ustc.edu.cn/initjxpgkc.do')
if not r.ok:
    print('Connection fail! error code {}'.format(r.status_code))
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup)
kvs = []
for l in soup.findAll(name='a'):
    link = l['href']
    if len(link) < 15:
        continue
    # print(link)
    tmp1 = [kv for kv in link.split('?')[1].split('&')]
    kvs.append({})
    for kv in tmp1:
        [k, v] = kv.split('=')
        kvs[-1][k] = v.strip()
    kvs[-1]['_name_'] = l.parent.previous_sibling.previous_sibling.text.strip()
        
    # print(kvs[-1])

# 爬照片
# for staff in kvs:
    # if len(staff['js']) < 10:
        # continue
    # r = session.get(r'https://mis.teach.ustc.edu.cn/zjPhoto.do?zjsno=' + staff['js'] + '&kcbjbh=' + staff['kcbjbh'] + '&xqdm=' + staff['xn'] + staff['xq'])
    # f = open(save_dir + staff['_name_'] + '.jpg', 'wb')
    # f.write(r.content)
    # f.close()

for staff in kvs:
    if len(staff['js']) < 10:
        # staff
        data = {'zjsno' : staff['js'],
                'kcbjbh' : staff['kcbjbh'],
                'kcid' : staff['kcid'],
                'czy' : staff['czy'],
                'js' : staff['js'],
                'yhdj' : staff['yhdj'],
                'xqdm' : staff['xn'] + staff['xq'],
                'xmdm' : staff['xmdm'],
                'answer' : '|' + '|'.join([str(i) + '&1&1' for i in range(1, 9)]) + '|9&1&3|'}
        r = session.post('https://mis.teach.ustc.edu.cn/submitanswer.do', data = data)
        if not r.ok:
            print('Submit staff {} fail! error code {}'.format(staff['_name_'], r.status_code))
        else:
            print(staff['_name_'])
    else:
        data = {'zjsno' : staff['js'],
                'kcbjbh' : staff['kcbjbh'],
                'kcid' : staff['kcid'],
                'czy' : staff['czy'],
                'js' : staff['js'],
                'yhdj' : staff['yhdj'],
                'xqdm' : staff['xn'] + staff['xq'],
                'xmdm' : staff['xmdm'],
                'answer' : '|' + '|'.join([str(i) + '&1&1' for i in range(2, 8)]) + '|'}
        r = session.post('https://mis.teach.ustc.edu.cn/submitanswer.do', data = data)
        if not r.ok:
            print('Submit staff {} fail! error code {}'.format(staff['_name_'], r.status_code))
        else:
            print(staff['_name_'])

