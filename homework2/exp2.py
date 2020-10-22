# -*- coding: utf-8 -*-

"""
#================实验二========================#。
Spyder Editor


This is a temporary script file.

"""

import re

import sys

from textblob import TextBlob

from textblob import Word

from collections import defaultdict
import math
import cmath


uselessTerm = ["username","text","tweetid"]

postings = defaultdict(dict)
postings2 = defaultdict(dict) #建立第二个列表，用于按照DOCid存储


N=0  #总的ID个数。

def merge2_and(term1,term2):

    global postings

    answer = []  

    if (term1 not in postings) or (term2 not in postings):

        return answer      

    else:

        i = len(postings[term1])

        j = len(postings[term2])

        x=0

        y=0

        while x<i and y<j:

            if postings[term1][x]==postings[term2][y]:

                answer.append(postings[term1][x])

                x+=1

                y+=1

            elif postings[term1][x] < postings[term2][y]:

                x+=1

            else:

                y+=1            

        return answer                        



def merge2_or(term1,term2):

    answer=[]

    if (term1 not in postings)and(term2 not in postings):

        answer = []      

    elif term2 not in postings:

        answer = postings[term1]

    elif term1 not in postings:

         answer = postings[term2]

    else:

        answer = postings[term1]

        for item in postings[term2]:

            if item not in answer:

                answer.append(item)              

    return answer



def merge2_not(term1,term2):

    answer=[]

    if term1 not in postings:

        return answer      

    elif term2 not in postings:

        answer = postings[term1]

        return answer

        

    else:

        answer = postings[term1]

        ANS = []

        for ter in answer:

            if ter not in postings[term2]:

                ANS.append(ter)

        return ANS



def do_rankSearch(terms): #将这个函数改成SMART NOTATION.

    Answer = defaultdict(float)
    #总ID个数：

    for item in terms:

        if item in postings:
            #key, val in pack.items():
            for d,tf in postings[item]:
                if d not in Answer:
                    Answer[d]=0
                    df = len(postings[item])  # 某个词项出现在哪些文档中
                # Wtq:
                    wtq = (1 + math.log(tf, 10)) * (math.log((N/df), 10))  # N为全部的个数
                # Wtd:
                    # 计算wt,d用到的c（cosine），归一化函数。对每一个DOCID都是不一样的。
                    c = 0
                    lenn = len(postings2[d])
                    for ii in range(0, lenn):
                        c = c + (postings2[d][ii][1] * math.log((N / df), 10)) * (
                                    (postings2[d][ii][1]) * math.log((N / df), 10))  # w^2,w=tf*lgN/df.
                    wtd =  math.sqrt(c)
                    Answer[d] =Answer[d]+ wtd * wtq   #为什么
               # else:
               #     Answer[d] = 0
   # for tt in Answer.keys():
    #    print("theAnswerIs: ")
     #   print(Answer[tt])

    for id in postings2.keys():#对每个用户的发表
        lenn=len(postings2[id])
        all=0
        for i in range(0,lenn):
            all=all + postings2[id][i][1]   #最后记录下所有DOCid的长度，tf作为每个词在文章里出现的次数，统计起来就是整篇文章的长度。
        if id in Answer.keys():
            Answer[id]=Answer[id]/all

    #以上，就把每个DOCid的评分都计算出来了。
    for tt in Answer.keys():
        print("theAnswerIs: ")
        print(Answer[tt])

    #排序：降序排序的得到最大值
    Answer = sorted(Answer.items(),key = lambda x: x[1],reverse = True)

    return Answer





def token(doc):

    doc = doc.lower()

    terms=TextBlob(doc).words.singularize()

    

    result=[]

    for word in terms:

        expected_str = Word(word)

        expected_str = expected_str.lemmatize("v")     

        result.append(expected_str)

    return result         



def tokenize_tweet(document):

    

    document=document.lower()

    a = document.index("username")

    b = document.index("clusterno")

    c = document.rindex("tweetid")-1

    d = document.rindex("errorcode")

    e = document.index("text")

    f = document.index("timestr")-3  

    #提取用户名、tweet内容和tweetid三部分主要信息

    document = document[c:d]+document[a:b]+document[e:f]

    #print(document)

    terms=TextBlob(document).words.singularize()

      

    result=[]

    for word in terms:

        expected_str = Word(word)

        expected_str = expected_str.lemmatize("v")

        if expected_str not in uselessTerm:

            result.append(expected_str)

    return result





def get_postings(): #倒排索引字典的建立。

    global postings
    global N

    f = open(r"D:\data cache\tweets.txt")  

    lines = f.readlines()#读取全部内容

#下面是对以DOCid为key的索引词表的构建：
    for line in lines:
        line = tokenize_tweet(line)
        tweetid=line[0]
        line.pop(0)
        unique_terms = set(line)
        for te in unique_terms:
            if tweetid in postings2.keys():
                test0=0
                for i in range(0,len(postings2[tweetid])):
                    if postings2[tweetid][i][0] == te: #如果已经存在这个term了
                        test0 = 1
                        kk = postings2[tweetid][i][1] + 1
                        postings2[tweetid].pop(i)
                        postings2[tweetid].append((te, kk))
                if test0 == 0:  # 如果全局都没有一个ID能够对应上。
                    postings2[tweetid].append((te,1))
            else:
                postings2[tweetid] = [(te,1)]
    """          
    for id in postings2.keys():  # 对每个
        lenn = len(postings2[id])
        all = 0
        for i in range(0, lenn):
            all = all + postings2[id][i][1]  # 最后记录下所有DOCid的长度，tf作为每个词在文章里出现的次数，统计起来就是整篇文章的长度。
        print("all:")
        print(all)
    """


#下面是对一般倒排索引词表的构建：
    for line in lines:
       N=N+1
       line = tokenize_tweet(line)

       #print(line)

       tweetid = line[0]

       line.pop(0)

       unique_terms = set(line)

       for te in unique_terms:

           if te in postings.keys():
               test0=0
               for i in range(0,len(postings[te])): #对每个te（term）对应的元组

                if postings[te][i][0]==tweetid: #如果已经存在这个ID，也就是之前记录过个数
                    test0=1
                    kk=postings[te][i][1]+1
                    postings[te].pop(i)
                    postings[te].append((tweetid,kk))

               if test0==0:#如果全局都没有一个ID能够对应上。
                   postings[te].append((tweetid,1))

           else:            

               postings[te] = [(tweetid,1)] #这样是不是更加符合二元组tuple的定义？
               
     #  for tee in postings.keys():
      #     postings[tee].sort();    #如果是postings不再是之前的int型list，那么这样排序就很不好，需要用一种其他方式来进行排序，应该对pair的first：ID排序。
            #sorted(postings[tee],)
    #按字典序对postings进行升序排序,但返回的是列表，失去了键值的信息

    #postings = sorted(postings.items(),key = lambda asd:asd[0],reverse=False)       

    #print(postings)


def do_search():

    terms = token(input("Search query >> "))

    if terms == []:

        sys.exit()  

    #搜索的结果答案   


    if len(terms)==3:

        #A and B

        if terms[1]=="and":

            answer = merge2_and(terms[0],terms[2])   

            print(answer)

        #A or B       

        elif terms[1]=="or":

            answer = merge2_or(terms[0],terms[2])  

            print(answer)

        #A not B    

        elif terms[1]=="not":

            answer = merge2_not(terms[0],terms[2])

            print(answer)

        #输入的三个词格式不对    

        else:

            print("input wrong!")


    #进行自然语言的排序查询，返回按相似度排序的最靠前的若干个结果

    else:

        #leng = len(terms)

        answer = do_rankSearch(terms)

        print ("[Rank_Score: Tweetid]  THE FIRST 10 SEARCH:")

        num=0

        for (tweetid,score) in answer:
            if num<10:
                print(str(score) + ": " + tweetid)
                num=num+1              

       # print("the type of answer is :")
       # print(type(answer))






def main():

    get_postings()

    while True:

        do_search()





if __name__ == "__main__":

    main()