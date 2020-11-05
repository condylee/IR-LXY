import math
import numpy as np

def generate_tweetid_gain(file_name):
    qrels_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in qrels_dict:  #0号是query id。
                qrels_dict[ele[0]] = {}
            # here we want the gain of doc_id in qrels_dict > 0,
            # so it's sorted values can be IDCG groundtruth
            if int(ele[3]) > 0:
                qrels_dict[ele[0]][ele[2]] = int(ele[3]) #[3]：gain,相当于tf值。
               # print(type(qrels_dict[ele[0]][ele[2]])) 类型是int
               # print(type(qrels_dict[ele[0]])) 类型是dict
    return qrels_dict

def read_tweetid_test(file_name):
    # input file format
    # query_id doc_id
    # query_id doc_id
    # query_id doc_id
    # ...
    test_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in test_dict:
                test_dict[ele[0]] = []
            test_dict[ele[0]].append(ele[1])
            #print(type(test_dict[ele[0]]))
           # print(type(test_dict))
    return test_dict

def MAP_eval(qrels_dict, test_dict, k = 100):
    lenOfQ=len(test_dict)  #|Q| 查询数量
    #for i in test_dict.keys():
    #    lenOfQ+=len(test_dict[i])
    #以上算出的就是全部相关文档Q的个数
    answer=0
    for i in test_dict.keys():
        num=len(test_dict[i])
        num=1/num  #1/mj
        sigema=0
        fenzi=0
        fenmu=0
       # k=100  #precision值
        for kk in qrels_dict.keys():
            if kk==i: #对上了两个queryID
                for j in range(0, len(test_dict[i])):
                    jishu = 0
                    jishu = jishu + 1
                    if jishu <= 100:
                        if test_dict[i][j] in qrels_dict[kk].keys():  # 如果result的这个docID存在于groundtruth对应查询的前k个中，那么sigema的值就要加一
                            fenzi = fenzi + 1
                            fenmu = fenmu + 1
                            sigema += fenzi / fenmu
                        else:
                            fenmu = fenmu + 1
                            sigema += 0
        answer+=num*sigema
    answer*=1/lenOfQ
    return answer

def MRR_eval(qrels_dict, test_dict, k = 100):
    answer = 0
    for i in qrels_dict.keys():  # 对每一个查询。
        for kk in test_dict.keys():
            if kk == i:  # 两个查询对应上了
                jud = 1
                for cc in qrels_dict[kk].keys():  # 取第一个ground truth值
                    if jud == 1:
                        for ll in range(0, len(test_dict[kk])):
                            if test_dict[kk][ll] == cc:
                                answer += 1 / (ll+1)
                    else:
                        break
                    jud += 1
    answer=answer/len(test_dict)
    return answer


def NDCG_eval(qrels_dict, test_dict, k = 100):
    ANS=0
    NDCG=0
    #初始化操作：对每个查询：进行result集合的gain值的构建，并进行DCG IDCG的构建
    for i in test_dict.keys():
        DCG=0#都是针对每一个查询的
        IDCG=0
        alist=[]
        kl = k
        if k > len(test_dict[i]):
            kl = len(test_dict[i])
        for j in range (0,kl):#对查询中result的每一个doc找是否有groundtruth集匹配的doc：
            flag=0
            if test_dict[i][j] in qrels_dict[i].keys():
                m=test_dict[i][j]
                alist.append((test_dict[i][j], qrels_dict[i][m]))
                #print(qrels_dict[i][m])
            else :
                alist.append((test_dict[i][j],0))
        sorted_alist = sorted(alist, key=lambda t: t[1], reverse=True)  # 降序排序完毕。
        #print(sorted_alist)
        #DCG:#IDCG：
        DCG=0
        IDCG=0
        q_NDCG=0
        for kk in range(0,len(alist)):
            if kk==0:
                DCG+=alist[kk][1]
                IDCG+=sorted_alist[kk][1]
                #print(alist[1])
            else :
                DCG += alist[kk][1]/ math.log( kk + 1,2)
                IDCG+=sorted_alist[kk][1]/ math.log( kk + 1,2)
            #print("DCG:",DCG)
            #print("IDCG:",IDCG)
            q_NDCG=DCG/IDCG
       # q_NDCG=q_NDCG/len(alist)
        NDCG+=q_NDCG  #对一个query的和

    ANS = NDCG / len(qrels_dict)
    return ANS


def evaluation():
    k = 100
    # query relevance file
    file_qrels_path = 'qrels.txt'
    # qrels_dict = {query_id:{doc_id:gain, doc_id:gain, ...}, ...} gain就是所谓的tf值。
    qrels_dict = generate_tweetid_gain(file_qrels_path)
    # ur result, format is in function read_tweetid_test, or u can write by ur own
    file_test_path = 'result.txt'
    # test_dict = {query_id:[doc_id, doc_id, ...], ...}
    test_dict = read_tweetid_test(file_test_path)

   # for ii in qrels_dict.keys():
    #    for j in qrels_dict[ii].keys():
     #       print(j)
   # for ii in test_dict.keys():
    #    for j in range(0,len(test_dict[ii])):
     #       print(test_dict[ii][j])

    MAP = MAP_eval(qrels_dict, test_dict, k)
    print('MAP', ' = ', MAP, sep='')

    MRR = MRR_eval(qrels_dict, test_dict, k)
    print('MRR', ' = ', MRR, sep='')
    NDCG = NDCG_eval(qrels_dict, test_dict, k)
    print('NDCG', ' = ', NDCG, sep='')

if __name__ == '__main__':
    evaluation()
