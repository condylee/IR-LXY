@[TOC](Experiment2: Ranked retrieval model)
# 0.个人信息：
[201800122025，李心怡，2018级数据班]
# 1.实验目的：
在Experiment1的基础上实现最基本的Ranked retrieval model
• Input：a query (like Ron Weasley birthday)
• Output: Return the top K (e.g., K = 100) relevant tweets.
1. Use SMART notation: lnc.ltn
• Document: logarithmic tf (l as first character), no idf and cosine 
normalization
• Query: logarithmic tf (l in leftmost column), idf (t in second column), 
no normalization
2. 改进Inverted index
• 在Dictionary中存储每个term的DF
• 在posting list中存储term在每个doc中的TF with pairs (docID, tf)

# 2.软件环境：
python3.6, Anaconda3, Spyder,pycharm
# 3.实验内容与设计：
## （1）实验内容：
– 使用我们介绍的方法，在tweets数据集上构建inverted index; 
– 实现Boolean Retrieval Model，使用TREC 2014 test topics 进行测试；
 – Boolean Retrieval Model：
       • Input：a query (like Ron and Weasley) 
       • Output: print the qualified tweets. 
       • 支持and, or ,not；查询优化可以选做；
    
##  （2）算法描述：
对于本实验的代码结构：
（1）倒排索引表：
在使用defaultdict(dict)结构建立原倒排索引字典的基础上，将每个term对应的list的元素类型改为tuple：二元组类型，具体为（docID,tf值）。
（2）查询：
删除了实验一的多元bool查询，仅支持二元bool查询，也就是说三个单词的情况仍然不支持进行自然语言查询。除了三个单词的情况，对每个文档的ranking值，进行检索排序。
得到ranking值的过程如课本所述，为SMART notation的方法。对于文档，用lnc方法，对于查询，用ltn方法，分别对wtq和wtd权重值进行计算，最终相乘并累积加和得到相应的ranking值。计算过程较为复杂，但并不困难，只要将对应的参数值都进行计算就可以。
## （3）测试结果：
1、例一：search>>Merging of US Air and American
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201008204647425.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDk5ODU4MA==,size_16,color_FFFFFF,t_70#pic_center)

2、例二：search>>Pope washed Muslims feet
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201008204657835.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDk5ODU4MA==,size_16,color_FFFFFF,t_70#pic_center)

3、例三：search>>with the murder of
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020100820470964.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDk5ODU4MA==,size_16,color_FFFFFF,t_70#pic_center)

# 4.分析与探讨：
  本实验我感觉最难的地方在于怎样对SMART NOTATION里的wi进行计算，因为在倒排索引表建立的过程中是无法进行的，完成建立后重新遍历的时间复杂度又太高。我的解决方法是，新建立一个索引表，与倒排索引表并列，是一个以docID为key，（term,tf）为value的dict类型字典。这样对于每个doc的遍历与wi的求取就方便了很多，时间复杂度也降低了很多。
