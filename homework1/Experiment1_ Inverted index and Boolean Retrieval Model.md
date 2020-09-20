@[TOC](Experiment1: Inverted index and Boolean Retrieval Model)
# 0.个人信息：
[201800122025，李心怡，2018级数据班]
# 1.实验目的：
（1）了解倒排索引表的构建过程和方法；
（2）了解搜索倒排索引表的搜索过程；
（3）学会构建bool查询。

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
使用defaultdict(dict)结构建立字典，字典中每个term对应的 tweetID列表以list格式存在。
（2）查询：
建立多个函数模块，每个模块支持一个二元或者三元的bool查询。（例如：A OR B,A AND B,etc）
对二元bool查询，进行双指针方法寻找共同存在的tweetID。具体体现为
对于三元查询，可以拆解为二元查询。
## （3）测试结果：
1、A and B、A or B、A not B：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200920110126150.png#pic_center)

2、A and B and C、A or B or C、(A and B) or C、(A or B) and C：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200920110155384.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200920121824895.png#pic_center)

3、一般的非3词或5词的自然语言查询：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200920121837630.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDk5ODU4MA==,size_16,color_FFFFFF,t_70#pic_center)

# 4.分析与探讨：
  对于倒排索引，因为不熟悉python编写的确花费了一点时间去了解函数API等。但是更重要的是一开始对于数据结构的选择，以及对于函数模块之间的嵌套、调用关系。思路上并没有很大的问题，易于理解设计。
  但是做的过程中发现python的sort函数对于大文件集十分不友好，今后会想办法缩短其排序所需要用掉的时间。
