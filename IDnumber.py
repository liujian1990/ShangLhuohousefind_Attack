# coding=utf-8
import random, time
import urllib

class ID_Yield():
    def __init__(self):
        self.num = 0
    @classmethod
    def calc(self,forhead_six_num,forhead_six_str,birthday, last_three):
        sum = (7 * int(forhead_six_str[0])) + (9 * int(forhead_six_str[1])) + (10 * int(forhead_six_str[2])) + (
        5 * int(forhead_six_str[3])) + (8 * int(forhead_six_str[4])) + (4 * int(forhead_six_str[5]))

        sum = sum + 2 * int(birthday[0]) + 1 * int(birthday[1]) + 6 * int(birthday[2]) + 3 * int(birthday[3]) + 7 * int(
        birthday[4]) + 9 * int(birthday[5]) + 10 * int(birthday[6]) + 5 * int(birthday[7])
        sum = sum + 8 * int(last_three[0]) + 4 * int(last_three[1]) + 2 * int(last_three[2])
        yushu = sum % 11  # 身份证最后一位 验证码  http://baike.baidu.com/view/188003.htm?qq-pf-to=pcqq.c2c#1_7
        if yushu == 0:  # 7－9－10－5－8－4－2－1－6－3－7－9－10－5－8－4－2
            last_one = "1"  # 0－1－2－3－4－5－6－7－8－9－10
        elif yushu == 1:  # 1－0－X －9－8－7－6－5－4－3－2
            last_one = "0"
        elif yushu == 2:
            last_one = "X"
        else:
            last_one = str(12 - yushu)
        id_num = forhead_six_num + birthday + last_three + last_one
        return id_num

    @classmethod
    def authdata(self,ID):
        post_data = {
            'sfz': ID,
            'mm': 111111,
            'imageField.x': 35,
            'imageField.y': 15
        }
        return urllib.urlencode(post_data)

    @classmethod
    def gen(self,place,year):#place = 0 ~6 year=1944
        data_list=[]
        _six_nums=[u'612501',u'612522',u'612523',u'612524',u'612525',u'612526',u'612527']#地方编码号
        six_num = _six_nums[place]
        for m in range(1,12):
            if m == 2 and year % 4 == 0:  # 闰年二月29天
                maxday = 29
            elif m == 2 and year % 4 != 0:
                m = 28
            elif m in [1, 3, 5, 7, 8, 10, 12]:  # 大月31天
                maxday = 31
            else:
                maxday = 30
            if m < 10:
                m = '0' + str(m) #位数不够，填0
                for d in range(10,maxday):
                    if d < 10:
                        d = '0' + str(d)
                    for last in range(0,999):
                        if last < 10:
                            last = '00' + str(last)
                        elif last < 100:
                            last = '0' + str(last)
                        ID=ID_Yield.calc(six_num,str(six_num),str(year)+str(m)+str(d),str(last))
                        data_list.append(ID_Yield.authdata(ID))
        print "[*] GEN OK!"
        return data_list
