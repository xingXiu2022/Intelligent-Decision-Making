#import lightGBM;
#部分决策树引用库

#https://www.bilibili.com/video/BV14m4y197F6?spm_id_from=333.337.search-card.all.click
'''
https://blog.csdn.net/codelady_g/article/details/123898844?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165062694716780271559519%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=165062694716780271559519&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-123898844.142^v9^pc_search_result_cache,157^v4^control&utm_term=codelady_g&spm=1018.2226.3001.4187
'''

import math
import operator
#树的可视化引用：
#import TreePlotter

def createDataset():

    dataSet = [
        #17*样本；6*属性
        #前6列为参照属性,7列为目标属性
        ['青绿','蜷缩','浊响','清晰','凹陷','硬滑','好瓜'],
        ['乌黑','蜷缩','沉闷','清晰','凹陷','硬滑','好瓜'],
        ['乌黑','蜷缩','浊响','清晰','凹陷','硬滑','好瓜'],
        ['青绿','蜷缩','沉闷','清晰','凹陷','硬滑','好瓜'],
        ['浅白','蜷缩','浊响','清晰','凹陷','硬滑','好瓜'],
        ['青绿','稍蜷','浊响','清晰','稍凹','软粘','好瓜'],
        ['乌黑','稍蜷','浊响','稍糊','稍凹','软粘','好瓜'],
        ['乌黑','稍蜷','浊响','清晰','稍凹','硬滑','好瓜'],
        ['乌黑','稍蜷','沉闷','稍糊','稍凹','硬滑','坏瓜'],
        ['青绿','硬挺','清脆','清晰','平坦','软粘','坏瓜'],
        ['浅自','硬挺','清脆','模糊','平坦','硬滑','坏瓜'],
        ['浅自','蜷缩','浊响','模糊','平坦','软粘','坏瓜'],
        ['青绿','稍蜷','浊响','稍彻','凹陷','硬滑','坏瓜'],
        ['浅自','稍蜷','沉问','稍糊','凹陷','硬滑','坏瓜'],
        ['乌黑','稍蜷','浊响','清晰','稍凹','软粘','坏瓜'],
        ['浅自','蜷缩','浊响','模糊','平坦','硬滑','坏瓜'],
        ['青绿','蜷缩','沉问','稍糊','稍凹','硬滑','坏瓜']
    ]

    # 特征列表
    labels = ['色泽','根蒂','敲击','纹理','脐部','触感']
    return dataSet,labels



#计数：
#返回字典所有的键组成的列表
def majorityCnt(classList):
    classCount={}
    for value in classList:
        if value not in classCount.keys():      #返回字典所有的键组成的列表
            classCount[value]=0
        classCount[value]+=1
    #排序：返回一个列表，列表中的每个元素都是一个元组（包含字典的每个元素的键和值）
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    # 返回最多的类别的名称:
    return sortedClassCount[0][0]

    #返回字典所有的键组成的列表

#计算信息熵
def calcShannonEnt(dataSet):
    #首先看数据中有多少个样本
    numEntries = len(dataSet)
    #计算每个类都有多少个样本（用字典存放）
    labelCount={}
    for featVec in dataSet:
        if featVec[-1] not in labelCount.keys():
            labelCount[featVec[-1]] = 0
    labelCount[featVec[-1]] += 1

    #初始化信息熵为0,并计算后返回
    shannonEnt = 0
    for key in labelCount:
        prob = float(labelCount[key]) / numEntries
        shannonEnt -= prob * math.log(prob,2)
    return shannonEnt

    pass


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0                            #设置初始信息熵为0
    bestFeature = -1                            #设置初始信息增益为-1
    
    for i in range(numFeatures):
        #得到集合
        featList = [example[i] for example in dataSet]

        #集合操作去重
        uniqueVals = set(featList)
        newEntropy = 0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        #更新信息增益值（若当前信息增益大于选定的信息增益值）
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
        return bestFeature

    pass

#返回的是最好的那个属性（选做根节点）的索引；
def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]

    #结束递归条件（就是什么时候可以不再往下分类了）
    #1>：当所有的出条件都趋向于单一属性：
    if classList.count(classList[0]) == len(dataSet):
        return classList[0]

    #2>:当所有属性都被用过了（一个属性仅能被作为一次分类的条件）：
    if len(dataSet[0]) == 1:
        # 返回的是数据集中个数最多的那个类别
        return majorityCnt(classList)

    #选择最好的分类属性进行划分:
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]

    #结果以字典形式进行保存
    myTree={bestFeatLabel:{}}
    #删除用过的属性：
    del(labels[bestFeat])

    #用集合操作进行去重
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)

    #拷贝一个属性的列表
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    
    return myTree



#调用函数：
dataSet,labels=createDataset()
myTree=createTree(dataSet,labels)
print(myTree)






