'''
https://blog.csdn.net/u013719339/article/details/84502265?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165079177916781685324929%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=165079177916781685324929&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-84502265.142^v9^pc_search_result_cache,157^v4^control&utm_term=cart%E5%86%B3%E7%AD%96%E6%A0%91python&spm=1018.2226.3001.4187
'''


from math import log
import operator
from DT_database import SQL_matrix

#图形化引用
from decisionTree_1 import TreePlotter

def createDataSet1():
    """
    创造示例数据/读取数据
    @param dataSet: 数据集
    @return dataSet labels：数据集 特征集
    """
    # 数据集（样例说明：是否同意贷款申请逻辑实现）
    '''
    dataSet = [('青年', '否', '否', '一般', '不同意'),
               ('青年', '否', '否', '好', '不同意'),
               ('青年', '是', '否', '好', '同意'),
               ('青年', '是', '是', '一般', '同意'),
               ('青年', '否', '否', '一般', '不同意'),
               ('中年', '否', '否', '一般', '不同意'),
               ('中年', '否', '否', '好', '不同意'),
               ('中年', '是', '是', '好', '同意'),
               ('中年', '否', '是', '非常好', '同意'),
               ('中年', '否', '是', '非常好', '同意'),
               ('老年', '否', '是', '非常好', '同意'),
               ('老年', '否', '是', '好', '同意'),
               ('老年', '是', '否', '好', '同意'),
               ('老年', '是', '否', '非常好', '同意'),
               ('老年', '否', '否', '一般', '不同意')]
    # 特征集
    labels = ['年龄', '有工作', '有房子', '信贷情况']
    #'''
    dataSet=[
        # ['奖学金情况', '入学-毕业成绩变动大小', '曾参与项目级别', '参与社团数', '成绩', '兼职', '就业状况'],
        ['院/系级', '20%', '无', '1-2', '30%', '是', '本专业'],
        ['校级', '20%', '省级/国家级', '1-2', '30%', '是', '本专业'],
        ['校级', '20%', '无', '1-2', '30%', '是', '本专业'],
        ['院/系级', '20%', '省级/国家级', '1-2', '30%', '是', '本专业'],
        ['省级/国家级', '20%', '无', '1-2', '30%', '是', '本专业'],
        ['院/系级', '10%', '无', '1-2', '50%', '否', '本专业'],
        ['校级', '10%', '无', '0', '50%', '否', '本专业'],
        ['校级', '10%', '无', '1-2', '50%', '是', '本专业'],
        ['校级', '10%', '省级/国家级', '0', '50%', '是', '非本专业'],
        ['院/系级', '40%', '校/市级', '1-2', '10%', '否', '非本专业'],
        ['省级/国家级', '40%', '校/市级', '3+', '10%', '是', '非本专业'],
        ['省级/国家级', '20%', '无', '3+', '10%', '否', '非本专业'],
        ['院/系级', '10%', '无', '0', '30%', '是', '非本专业'],
        ['省级/国家级', '10%', '省级/国家级', '0', '30%', '是', '非本专业'],
        ['校级', '10%', '无', '1-2', '50%', '否', '非本专业'],
        ['省级/国家级', '20%', '无', '3+', '10%', '是', '非本专业'],
        ['院/系级', '20%', '省级/国家级', '0', '50%', '是', '非本专业']
    ]

    dataSet = SQL_matrix.to_mat1("sql_pyc", "stu_w1")

    # 特征集
    labels = ['奖学金情况', '入学-毕业成绩变动大小', '曾参与项目级别', '参与社团数', '成绩', '兼职']
    return dataSet, labels


def calcProbabilityEnt(dataSet):
    """
    样本点属于第1个类的概率p，即计算2p(1-p)中的p
    @param dataSet: 数据集
    @return probabilityEnt: 数据集的概率
    """
    numEntries = len(dataSet)  # 数据条数
    feaCounts = 0
    fea1 = dataSet[0][len(dataSet[0]) - 1]
    for featVec in dataSet:  # 每行数据
        if featVec[-1] == fea1:
            feaCounts += 1
    probabilityEnt = float(feaCounts) / numEntries
    return probabilityEnt


def splitDataSet(dataSet, index, value):
    """
    划分数据集，提取含有某个特征的某个属性的所有数据
    @param dataSet: 数据集
    @param index: 属性值所对应的特征列
    @param value: 某个属性值
    @return retDataSet: 含有某个特征的某个属性的数据集
    """
    retDataSet = []
    for featVec in dataSet:
        # 如果该样本该特征的属性值等于传入的属性值，则去掉该属性然后放入数据集中
        if featVec[index] == value:
            reducedFeatVec = featVec[:index] + featVec[index + 1:]  # 去掉该属性的当前样本
            retDataSet.append(reducedFeatVec)  # append向末尾追加一个新元素，新元素在元素中格式不变，如数组作为一个值在元素中存在
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    """
    选择最优特征
    @param dataSet: 数据集
    @return bestFeature: 最优特征所在列
    """
    numFeatures = len(dataSet[0]) - 1  # 特征总数
    if numFeatures == 1:  # 当只有一个特征时
        return 0
    bestGini = 1  # 最佳基尼系数
    bestFeature = -1  # 最优特征
    for i in range(numFeatures):
        uniqueVals = set(example[i] for example in dataSet)  # 去重，每个属性值唯一
        feaGini = 0  # 定义特征的值的基尼系数
        # 依次计算每个特征的值的熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)  # 根据该特征属性值分的类
            # 参数：原数据、循环次数(当前属性值所在列)、当前属性值
            prob = len(subDataSet) / float(len(dataSet))
            probabilityEnt = calcProbabilityEnt(subDataSet)
            feaGini += prob * (2 * probabilityEnt * (1 - probabilityEnt))
        if (feaGini < bestGini):  # 基尼系数越小越好
            bestGini = feaGini
            bestFeature = i
            #这里有修改——临时加上-1
    return bestFeature


def majorityCnt(classList):
    """
    对最后一个特征分类，出现次数最多的类即为该属性类别，比如：最后分类为2男1女，则判定为男
    @param classList: 数据集，也是类别集
    @return sortedClassCount[0][0]: 该属性的类别
    """
    classCount = {}
    # 计算每个类别出现次数
    for vote in classList:
        try:
            classCount[vote] += 1
        except KeyError:
            classCount[vote] = 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)  # 出现次数最多的类别在首位
    # 对第1个参数，按照参数的第1个域来进行排序（第2个参数），然后反序（第3个参数）
    return sortedClassCount[0][0]  # 该属性的类别


def createTree(dataSet, labels):
    """
    对最后一个特征分类，按分类后类别数量排序，比如：最后分类为2同意1不同意，则判定为同意
    @param dataSet: 数据集
    @param labels: 特征集
    @return myTree: 决策树
    """
    classList = [example[-1] for example in dataSet]  # 获取每行数据的最后一个值，即每行数据的类别
    # 当数据集只有一个类别
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 当数据集只剩一列（即类别），即根据最后一个特征分类
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    # 其他情况
    bestFeat = chooseBestFeatureToSplit(dataSet)  # 选择最优特征（所在列）
    try:
        bestFeatLabel = labels[bestFeat]  # 最优特征
        del (labels[bestFeat])  # 从特征集中删除当前最优特征
        uniqueVals = set(example[bestFeat] for example in dataSet)  # 选出最优特征对应属性的唯一值
        myTree = {bestFeatLabel: {}}  # 分类结果以字典形式保存
        for value in uniqueVals:
            subLabels = labels[:]  # 深拷贝，拷贝后的值与原值无关（普通复制为浅拷贝，对原值或拷贝后的值的改变互相影响）
            myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)  # 递归调用创建决策树
    except:
        pass
    return myTree


if __name__ == '__main__':
    dataSet, labels = createDataSet1()  # 创造示列数据
    r11=createTree(dataSet, labels)
    print(r11)  # 输出决策树模型结果
    TreePlotter.createPlot(r11)