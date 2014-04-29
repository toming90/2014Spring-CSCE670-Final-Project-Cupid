__author__ = 'Toming90'
import urllib2
from bs4 import BeautifulSoup
import urllib
import cookielib
import re
import os
import json
lgurl = "http://www.match.com/login/logout.aspx?lid=3"
storePath = 'd:/489final1/'
hds = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'}


pstdata = {"__VIEWSTATE":"/wEPDwUKMTExNTkxMjA5NGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgIFPGN0bDAwJHdvcmthcmVhJGxvZ291dFBhZ2VWaWV3JGN0bDAwJGxvZ2luJGN0bDAwJGNieEF1dG9Mb2dpbgU4Y3RsMDAkd29ya2FyZWEkbG9nb3V0UGFnZVZpZXckY3RsMDAkbG9naW4kY3RsMDAkYnRuTG9naW4=",
           "ctl00$workarea$logoutPageView$ctl00$login$ctl00$tbxHandle":"<UserName>",
           "ctl00$workarea$logoutPageView$ctl00$login$ctl00$tbxPassword":"<PassWord>",
           "ctl00$workarea$logoutPageView$ctl00$login$ctl00$cbxAutoLogin":"on",
           "ctl00$workarea$logoutPageView$ctl00$login$ctl00$btnLogin.x":"0",
           "ctl00$workarea$logoutPageView$ctl00$login$ctl00$btnLogin.y":"0"
           }


zipcodelist = ['76801','78380','77840','76002','77517','78730','77701','78102','77833',
                '77802','78402','75284','75342','88554','77005','77068','77282','78249',
                '78263','78296','78108','76686','77990','78502','76666','76550','75652',
                '78140','78749','77631']
genderlist = ['cl=1&gc=2&tr=1','cl=1&gc=1&tr=2']
agePair = [['25','18'],['30','26'],['35','31'],['40','32'],['50','41']]

for zipcode in zipcodelist:
    print zipcode
    for age in agePair:
        for gender in genderlist:
            cookie = cookielib.CookieJar()
            cookie_handler = urllib2.HTTPCookieProcessor(cookie)

            dt = urllib.urlencode(pstdata)

            opener = urllib2.build_opener(cookie_handler)
            opener.open(lgurl,dt)

           #==========================================================================================================
           # the html we will parse (which is a combination of different gender,zipcode and age range)
           #==========================================================================================================
            queryurl = 'http://www.match.com/SearchReskin/?dls=1&st=Q&CLR=true&%3fEXEC=GO&SB=radius&lid=226&'+gender+'&uage='+age[0]+'&ua='+age[0]+'&pc='+zipcode+'&dist=50&po=1&oln=0&lage='+age[1];
            response = opener.open(queryurl)
            urlcontent = response.read()
            soup = BeautifulSoup(urlcontent)

            head = soup.find_all('a',href = re.compile(r"/profile/showprofile.aspx"))
            hreflist = []
            for i in head:
                hreflist.append(i['href'])
            a = set(hreflist)
            hreflist = list(a)
            mainUrl = "http://www.match.com/"
            hreflist.remove(hreflist[0])
            count = 1
            for m in hreflist:
                dtList = []
                ddList = []
                newurl = mainUrl + m
                res = opener.open(newurl)
                newcontent = res.read()
                newSoup = BeautifulSoup(newcontent)

                if newSoup.h2 == None:
                    pass
                else:
                    h2content = newSoup.h2.string
                    PeopleName = h2content
                    dtList.append('Name')
                    ddList.append(PeopleName)
                    if not os.path.exists(storePath+PeopleName):
                        os.makedirs(storePath+PeopleName)

                    #==========================================================================================================
                    #Getting customer age info by parsing html
                    #==========================================================================================================
                    GenderAgeList = []

                    SeekingTag = newSoup.find('strong',text ='Seeking')
                    temp = str(SeekingTag.find_previous_siblings('strong'))
                    temp2 = re.sub(r'<.*?>|,|\]|\[',' ',temp)
                    temp3 = re.split(r'\s+',temp2)
                    for ele in temp3:
                        if ele !='':
                            GenderAgeList.append(ele)
                    dtList.append('Age')
                    ddList.append(GenderAgeList[0])
                    dtList.append('Gender')
                    ddList.append(GenderAgeList[3])
                                 
                                 
                    #==========================================================================================================
                    #Getting customer personal infomation such as relationship,have kid or not... etc..
                    #==========================================================================================================
                    PersonalInfo = newSoup.dl
                    dic_PersonalInfo ={}
                    countele2 = 0
                    for ele1 in PersonalInfo.find_all('dt'):
                        temp = str(ele1.string).lower()
                        temp2 = re.sub(r':','-',temp)
                        temp3 = re.split(r'\-',temp2)
                        for te in temp3:
                            if te!='':
                                dtList.append(te)
                    for ele2 in PersonalInfo.find_all('dd'):
                        if countele2 == 5:
                            temp = str(ele2.string.lower())
                            temp2 = re.sub(r'\'|\"|\(|\)|[a-z]',' ',temp)
                            temp3 = re.split(r'\s+',temp2)
                            heightList = []
                            for t in temp3:
                                if t!='':
                                    heightList.append(t)
                            ddList.append(heightList)
                        else:

                            ddList.append(str(ele2.string).lower())
                        countele2 = countele2+1
                        
                        
                        
                    #==========================================================================================================
                    #Getting customers' Interests by parsing html
                    #==========================================================================================================
                    interests = []
                    temp = str(newSoup.find_all('p',class_='interests'))
                    temp2 = re.sub(r'<.*>|\]|\[',',',temp)
                    temp3 = re.split(r',|\r|\t|\n',temp2)
                    for tp3 in temp3:
                        if tp3!='':
                            tp4 = tp3.strip()
                            interests.append(tp4)

                    dtList.append('interests')
                    ddList.append(interests)
                    
                    
                    
                    #==========================================================================================================           
                    #Getting customers' favourate pets
                    #==========================================================================================================
                    PetsList = []
                    ttt = newSoup.find('h3',text = 'Pets')
                    if ttt == None:
                        dtList.append('Pets')
                        ddList.append(PetsList)
                    else:

                        temp = str(ttt.find_next_siblings('p'))
                        temp2 = re.sub(r'<.*?>|,|\]|\[',' ',temp)
                        temp3 = re.split(r'\s+',temp2)
                        for tpt in temp3:
                            if tpt!='':
                                PetsList.append(tpt)
                        dtList.append('Pets')
                        ddList.append(PetsList)
                    dic_PersonalInfo = dict(zip(dtList,ddList))
                    
                    
                    
           
                    #==========================================================================================================
                    #store all the information of one person in one txt file
                    #==========================================================================================================
                    txtName = PeopleName+'_BasicInfo.txt'
                    txtPath = storePath+PeopleName+'/'+txtName
                    with open(txtPath,'w') as outfile:
                        json.dump(dic_PersonalInfo,outfile)

                    #==========================================================================================================
                    #Getting the picture of customer and download it
                    #==========================================================================================================
                    imgcluster = newSoup.find_all('img')
                    picNum = 1
                    for ele in imgcluster:
                        if picNum == 3:
                            imgurl = ele['src']
                            picName = PeopleName+'_Picture'+'.jpeg'
                            localPath = storePath+PeopleName+'/'+ picName
                            urllib.urlretrieve(imgurl,localPath)
                        picNum = picNum+1
                    count = count+1






