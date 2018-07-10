username = 'PB15000301'
passowrd = '280473'
save_dir = '/mnt/d/staff_pic/'

import requests
from bs4 import BeautifulSoup

import time
from tkinter import *

class USTCTool:
    grade_to_numstr = {'A+' : '95', 
                       'A'  : '90', 
                       'A-' : '85', 
                       'B+' : '82', 
                       'B'  : '78', 
                       'B-' : '75', 
                       'C+' : '72',
                       'C'  : '68',
                       'C-' : '65',
                       'D+' : '64',
                       'D'  : '61',
                       'D-' : '60',
                       'F'  : '0',
                       '旷考' : '0'}
    def __init__(self):
        # session 帮你保存cookies
        self.session = requests.Session()
        self.Logged = False

    def Login(self, username, password):
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        # 获取页面中的随机token
        page = self.session.get(r'https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fmis.teach.ustc.edu.cn/casLogin.do')
        if not page.ok:
            print('Connection fail! error code {}'.format(page.status_code))
        soup = BeautifulSoup(page.text, 'html.parser')
        _token = soup.find('input', {'name' : '_token'})['value']
        # print(_token)

        # 这里将redirect设为false，从而不自动跳转，获取ticket后可以手动跳转
        # 或者允许自动跳转
        self.session.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        r = self.session.post(r'https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fmis.teach.ustc.edu.cn/casLogin.do', 
                         data={'_token' : _token, 'login' : username, 'password' : passowrd, 'button' : '登录'})
        if not r.ok:
            print('Login fail! error code {}'.format(r.status_code))
        if '密码错误' in r.text:
            print('Login fail! wrong password')
        self.Logged = True

    def _get_staffs(self):
        # 获取所有未评教的老师、助教信息
        r = self.session.get(r'http://mis.teach.ustc.edu.cn/initjxpgkc.do')
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
        return kvs


    def GetStaffPhoto(self, save_dir):
        # 爬所有助教照片
        kvs = self._get_staffs()
        for staff in kvs:
            if len(staff['js']) < 10:
                continue
            r = self.session.get(r'https://mis.teach.ustc.edu.cn/zjPhoto.do?zjsno=' + staff['js'] + '&kcbjbh=' + staff['kcbjbh'] + '&xqdm=' + staff['xn'] + staff['xq'])
            f = open(save_dir + staff['_name_'] + '.jpg', 'wb')
            f.write(r.content)
            f.close()

    def GetOneStaffPhoto(self, save_dir, staff_id, course_id, xqdm):
        link = r'https://mis.teach.ustc.edu.cn/zjPhoto.do?zjsno=' + staff_id + '&kcbjbh=' + course_id + '&xqdm=' + xqdm
        r = self.session.get(link)
        if not r.ok:
            print('Login fail! error code {}'.format(r.status_code))
        f = open(save_dir + 'test1.jpg', 'wb')
        f.write(r.content)
        f.close()


    def EvalStaff(self):
        # 自动评教所有未评教的老师助教
        kvs = self._get_staffs()
        for staff in kvs:
            if len(staff['js']) < 10:
                # teacher
                data = {'zjsno' : staff['js'],
                        'kcbjbh' : staff['kcbjbh'],
                        'kcid' : staff['kcid'],
                        'czy' : staff['czy'],
                        'js' : staff['js'],
                        'yhdj' : staff['yhdj'],
                        'xqdm' : staff['xn'] + staff['xq'],
                        'xmdm' : staff['xmdm'],
                        'answer' : '|' + '|'.join([str(i) + '&1&1' for i in range(1, 9)]) + '|9&1&3|'}
                r = self.session.post('https://mis.teach.ustc.edu.cn/submitanswer.do', data = data)
                if not r.ok:
                    print('Submit staff {} fail! error code {}'.format(staff['_name_'], r.status_code))
                else:
                    print(staff['_name_'])
            else:
                # zhujiao
                data = {'zjsno' : staff['js'],
                        'kcbjbh' : staff['kcbjbh'],
                        'kcid' : staff['kcid'],
                        'czy' : staff['czy'],
                        'js' : staff['js'],
                        'yhdj' : staff['yhdj'],
                        'xqdm' : staff['xn'] + staff['xq'],
                        'xmdm' : staff['xmdm'],
                        'answer' : '|' + '|'.join([str(i) + '&1&1' for i in range(2, 8)]) + '|'}
                r = self.session.post('https://mis.teach.ustc.edu.cn/submitanswer.do', data = data)
                if not r.ok:
                    print('Submit staff {} fail! error code {}'.format(staff['_name_'], r.status_code))
                else:
                    print(staff['_name_'])

    def GetGrade(self, xuenian=''):
        # 获取指定学期的所有成绩，返回字典
        # 学年：18年春为 '20172'
        link = 'http://mis.teach.ustc.edu.cn/querycjxx.do'
        data = {'xuenian' : xuenian, 'chaxun' : r'+%B2%E9++%D1%AF+', 'px' : '1', 'zd' : '0'}
        r = self.session.post(link, data)
        if not r.ok:
            print('Query fail! error code {}'.format(r.status_code))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find_all('table')[2]
        # print(dir(table))
        lines = {}
        for line in table.find_all('tr'):
            tds = line.find_all('td')
            # print(tds)
            if len(tds) < 2:
                continue
            if tds[7].string == '覆盖':
                continue
            item = {}
            item['name'] = tds[2].string
            item['id'] = tds[1].string
            item['XQ'] = tds[0].string
            item['grade'] = tds[4].string
            item['score'] = tds[6].string
            # print(item)
            lines[item['name']] = item
            # lines.append(item)
        return lines

    def _grade_to_GPA(self, grade):
        # take in a str grade
        # return GPA
        if grade in self.grade_to_numstr:
            return self._grade_to_GPA(self.grade_to_numstr[grade])
        if grade == '通过':
            return None
        grade = int(grade)
        if grade < 60:
            return 0.0
        if grade == 60:
            return 1.0
        if grade <= 63:
            return 1.3
        if grade == 64:
            return 1.5
        if grade <= 67:
            return 1.7
        if grade <= 71:
            return 2.0
        if grade <= 74:
            return 2.3
        if grade <= 77:
            return 2.7
        if grade <= 81:
            return 3.0
        if grade <= 84:
            return 3.3
        if grade <= 89:
            return 3.7
        if grade <= 94:
            return 4.0
        return 4.3 

    def AverageGPA(self):
        # 计算所有学期平均GPA
        grades = self.GetGrade()
        gpa_sum = 0.0
        score_sum = 0.0
        for name in grades:
            line = grades[name]
            if self._grade_to_GPA(line['grade']) == None:
                continue
            gpa = self._grade_to_GPA(line['grade'])
                
            gpa_sum += gpa * float(line['score'])
            score_sum += float(line['score'])
        return gpa_sum / score_sum

    def AutoQueryGrade(self):
        grades = self.GetGrade('20172')
        while True:
            time.sleep(60 * 5)
            new_grades = self.GetGrade('20172')
            if len(new_grades) > len(grades):
                # alert_str = ''
                for name in new_grades:
                    if name not in grades:
                        alert_str = name + ' : ' + new_grades[name]['grade'] + '\n'
                        self.show_reminder(alert_str)
                grades = new_grades


                    
    def show_reminder(self, alert_str):
        root=Tk()
        root.withdraw()
        screenwidth=root.winfo_screenwidth()
        screenheight=root.winfo_screenheight()-100
        print(screenwidth, screenheight)
        root.resizable(False,False)
        root.title("reminder")
        frame=Frame(root,relief=RIDGE,borderwidth=3)
        frame.pack(fill=BOTH,expand=1)
        label=Label(frame,text=alert_str,font="Consolas -20 bold")
        label.pack(fill=BOTH,expand=1)
        button=Button(frame,text="OK",font="Consolas -25 bold", command=root.destroy)
        button.pack(side=BOTTOM)
        root.update_idletasks()
        root.deiconify()
        root.withdraw()
        root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10,
            int((screenwidth - root.winfo_width())/2), int((screenheight - root.winfo_height())/2)))    #窗口所在位置以及大小，前两个字符串代表窗口宽高，后两个字符串代表左上角坐标
        root.deiconify()
        root.lift(aboveThis=None)
        root.mainloop()


if __name__ == '__main__':
    tool = USTCTool()
    tool.Login(username, passowrd)
    # example:
    # 自动查询成绩，更新时弹窗提醒
    # tool.AutoQueryGrade()

    # 一键评教
    # tool.EvalStaff()






