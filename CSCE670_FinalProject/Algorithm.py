# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 16:18:53 2014

@author: LimingYe
"""
__author__ = 'michael'
from scipy.spatial import distance
import cjson
import numpy as np
import math

index = 1
total = {}
with open("/Users/LimingYe/Downloads/dataCollection2.txt", "r") as f:
    for line in f:
        data = cjson.decode(line)
        total[index] = data
        index += 1
        
#==============================================================================
#   test case      
#==============================================================================
ME = {}
ME['faith'] = 'Jewish'
ME['wants kids'] = 'someday'
ME['gender'] = 'woman'
ME['age'] = '22'
ME['drink'] = 'social drinker'
ME['have kids'] = 'yes, and they live away from home'
ME['body type'] = 'slender'
ME['height'] = ["6", "2", "187"]
ME['relationship'] = 'never married'
ME['smoke'] = 'no way'
ME['ethnicity'] = 'asian'
ME['interests'] = 'Camping , Cooking , Dining out , Fishing/Hunting , Movies/Videos , Music and concerts , Exploring new areas , Nightclubs/Dancing , Playing cards , Playing sports , Travel/Sightseeing , Watching sports'
ME['pets'] = ['dogs', 'cats'] 

#==============================================================================
#assign weight to every thing
#==============================================================================
haveK = {}
haveK['i\'ll tell you later'] = -2
haveK['no'] = -1
haveK['yes, and they sometimes live at home'] = 0
haveK['yes, and they live away from home'] = 1
haveK['yes, and they live at home'] = 2

wantK = {}
wantK['i\'ll tell you later'] = -3
wantK['no'] = -2
wantK['probably not'] = -1
wantK['no, but it\'s ok if my partner has kids'] = 0
wantK['not sure'] = 1
wantK['someday'] = 2
wantK['definitely'] = 3

body = {}
body['i\'ll tell you later'] = -3
body['slender'] = -2
body['about average'] = -1
body['athletic and toned'] = 0
body['a few extra pounds'] = 1
body['stocky'] = 2
body['heavyset'] = 3

smoke = {}
smoke['i\'ll tell you later'] = -2
smoke['no way'] = -1
smoke['occasionally'] = 0
smoke['yes, but trying to quit'] = 1
smoke['daily'] = 2
smoke['cigar aficionado'] = 3

drink = {}
drink['i\'ll tell you later'] = -2
drink['never'] = -1
drink['social drinker'] = 0
drink['moderately'] = 1
drink['regularly'] = 2

#==============================================================================
# begin to process
#==============================================================================
finalScore = {}
for index,record in total.iteritems():
    TOTALSCORE = 0.0
    if ME['gender'] == record['gender']:#如果同性,直接跳过
#        finalScore[index] = TOTALSCORE
        continue
    if ME['relationship'] == record['relationship']:#如果婚状相同,则加1,权重可以自行调整
        TOTALSCORE += 1
    if ME['ethnicity'] == record['ethnicity']:#如果民族相同,则加1,权重可以自行调整
        TOTALSCORE += 1
    if ME['faith'] == record['faith']:#如果信仰相同,则加1,权重可以自行调整
        TOTALSCORE += 1
    
    if math.fabs(body[ME['body type']] - body[record['body type']]) != 0: #身体状况, 越远则权重越小
        TOTALSCORE += 1/math.fabs(body[ME['body type']] - body[record['body type']])
    else:
        TOTALSCORE += 1
        
    if math.fabs(smoke[ME['smoke']] - smoke[record['smoke']]) != 0: #抽烟状况,越远则权重越小
        TOTALSCORE += 1/math.fabs(smoke[ME['smoke']] - smoke[record['smoke']])
    else:
        TOTALSCORE += 1
    
    if math.fabs(drink[ME['drink']] - drink[record['drink']]) != 0:#喝酒状况,越远则权重越小
        TOTALSCORE += 1/math.fabs(drink[ME['drink']] - drink[record['drink']])
    else:
        TOTALSCORE += 1
    
    if math.fabs(haveK[ME['have kids']] - haveK[record['have kids'].split('(')[0].strip()]) != 0:#有孩子状况,越远则权重越小
        TOTALSCORE += 1/math.fabs(haveK[ME['have kids']] - haveK[record['have kids'].split('(')[0].strip()])
    else:
        TOTALSCORE += 1
    
    if math.fabs(wantK[ME['wants kids']] - wantK[record['wants kids']]) != 0:#想孩子状况,越远则权重越小
        TOTALSCORE += 1/math.fabs(wantK[ME['wants kids']] - wantK[record['wants kids']])
    else:
        TOTALSCORE += 1
    
    if math.fabs(int(ME['age']) - int(record['age'])) != 0:#年龄,差距越大则权重越小
        TOTALSCORE += 1/math.fabs(int(ME['age']) - int(record['age']))
    else:
        TOTALSCORE += 1
        
    if math.fabs(int(ME['height'][2]) - int(record['height'][2])) != 0:#身高,差距越大则权重越小
        TOTALSCORE += 1/math.fabs(int(ME['height'][2]) - int(record['height'][2]))
    else:
        TOTALSCORE += 1
        
    for animal in ME['pets']:#对于宠物, 每有一只相同宠物就多加1点,权重可以改变,必须是birds dogs cats exotic pets fish horses
        if animal in record['pets']:
            TOTALSCORE += 1
   

    interest = []# stores the interest list
    lisRecord = []
    for word in ME['interests'].split(","):#兴趣爱好由单一string存储
        interest.append(word.strip().lower())
        lisRecord.append(1)
    lis = []#if the word in input is in her interests, then it is 1, if not, it is 0 
    for word in interest:
        if word in record["interests"]:
            lis.append(1)
        elif word not in total[index]["interests"]:
            lis.append(0)

    match = np.array(lisRecord)#match is the array for the input
    interestScore = np.array(lis)
    
    if math.isnan(1- distance.cosine(match, interestScore)):
        TOTALSCORE += 0
    else:
        TOTALSCORE += (1- distance.cosine(match, interestScore))
    
    finalScore[index] = TOTALSCORE

print finalScore

#==============================================================================
# intereset score
#==============================================================================
#interest = []# stores the interest list
#lisRecord = []
#for word in ME['interests'].split(","):
#    interest.append(word.strip().lower())
#    lisRecord.append(1)
#    
#match = np.array(lisRecord)#match is the array for the input
#interestScore = {}# Array is the 1,0 array for each person
#for index in total.keys():
#   lis = []#if the word in input is in her interests, then it is 1, if not, it is 0
#   for word in interest:
#       if word in total[index]["interests"]:
#           lis.append(1)
#       elif word not in total[index]["interests"]:
#           lis.append(0)
#   interestScore[index] = np.array(lis)   
#    
##max = 0
##final = []
#for index in interestScore.keys():
#    num = 0#total number for each person
#    for i in interestScore[index]:
#        num = num + i
#    if num == 0:
#        index = index + 1
#        continue
#    finalResult = 1- distance.cosine(match, interestScore[index])
#    
##    if finalResult >= max:
##        if finalResult > max:
##            max = finalResult
##            final = []
##            final.append(index)
##        else:
##            final.append(index)
#
#for index in final:
#    print total[index]
#
#pass