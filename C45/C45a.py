
'''
https://blog.csdn.net/leaf_zizi/article/details/84866918?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165079769516780366593959%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=165079769516780366593959&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-84866918.142^v9^pc_search_result_cache,157^v4^control&utm_term=c4.5%E5%86%B3%E7%AD%96%E6%A0%91python&spm=1018.2226.3001.4187 p
'''

def calcGainRatio(dataSet, labelIndex, labelPropertyi):
    """
    type: (list, int, int) -> float, int
    计算信息增益率,返回信息增益率和连续属性的划分点
    dataSet: 数据集
    labelIndex: 特征值索引
    labelPropertyi: 特征值类型，0为离散，1为连续
    """
    baseEntropy = calcShannonEnt(dataSet, labelIndex)  # 计算根节点的信息熵
    featList = [example[labelIndex] for example in dataSet]  # 特征值列表
    uniqueVals = set(featList)  # 该特征包含的所有值
    newEntropy = 0.0
    bestPartValuei = None
    IV = 0.0
    totalWeight = 0.0
    totalWeightV = 0.0
    totalWeight = calcTotalWeight(dataSet, labelIndex, True)  # 总样本权重
    totalWeightV = calcTotalWeight(dataSet, labelIndex, False)  # 非空样本权重
    if labelPropertyi == 0:  # 对离散的特征
        for value in uniqueVals:  # 对每个特征值，划分数据集, 计算各子集的信息熵
            subDataSet = splitDataSet(dataSet, labelIndex, value)
            totalWeightSub = 0.0
            totalWeightSub = calcTotalWeight(subDataSet, labelIndex, True)
            if value != 'N':
                prob = totalWeightSub / totalWeightV
                newEntropy += prob * calcShannonEnt(subDataSet, labelIndex)
            prob1 = totalWeightSub / totalWeight
            IV -= prob1 * log(prob1, 2)
    else:  # 对连续的特征
        uniqueValsList = list(uniqueVals)
        if 'N' in uniqueValsList:
            uniqueValsList.remove('N')
            # 计算空值样本的总权重，用于计算IV
            totalWeightN = 0.0
            dataSetNull = splitDataSet(dataSet, labelIndex, 'N')
            totalWeightN = calcTotalWeight(dataSetNull, labelIndex, True)
            probNull = totalWeightN / totalWeight
            if probNull > 0.0:
                IV += -1 * probNull * log(probNull, 2)

        sortedUniqueVals = sorted(uniqueValsList)  # 对特征值排序
        listPartition = []
        minEntropy = inf

        if len(sortedUniqueVals) == 1:  # 如果只有一个值，可以看作只有左子集，没有右子集
            totalWeightLeft = calcTotalWeight(dataSet, labelIndex, True)
            probLeft = totalWeightLeft / totalWeightV
            minEntropy = probLeft * calcShannonEnt(dataSet, labelIndex)
            IV = -1 * probLeft * log(probLeft, 2)
        else:
            for j in range(len(sortedUniqueVals) - 1):  # 计算划分点
                partValue = (float(sortedUniqueVals[j]) + float(
                    sortedUniqueVals[j + 1])) / 2
                # 对每个划分点，计算信息熵
                dataSetLeft = splitDataSet(dataSet, labelIndex, partValue, 'L')
                dataSetRight = splitDataSet(dataSet, labelIndex, partValue, 'R')
                totalWeightLeft = 0.0
                totalWeightLeft = calcTotalWeight(dataSetLeft, labelIndex, True)
                totalWeightRight = 0.0
                totalWeightRight = calcTotalWeight(dataSetRight, labelIndex, True)
                probLeft = totalWeightLeft / totalWeightV
                probRight = totalWeightRight / totalWeightV
                Entropy = probLeft * calcShannonEnt(
                    dataSetLeft, labelIndex) + probRight * calcShannonEnt(dataSetRight, labelIndex)
                if Entropy < minEntropy:  # 取最小的信息熵
                    minEntropy = Entropy
                    bestPartValuei = partValue
                    probLeft1 = totalWeightLeft / totalWeight
                    probRight1 = totalWeightRight / totalWeight
                    IV = -1 * (probLeft * log(probLeft, 2) + probRight * log(probRight, 2))

        newEntropy = minEntropy
    gain = totalWeightV / totalWeight * (baseEntropy - newEntropy)
    if IV == 0.0:  # 如果属性只有一个值，IV为0，为避免除数为0，给个很小的值
        IV = 0.0000000001
    gainRatio = gain / IV
    return gainRatio, bestPartValuei
