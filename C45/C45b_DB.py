# '''
#数据库
import math
import operator
import matplotlib.pyplot as plt
# import TreePlotter
import sys

sys.path.append('./decisionTree_1/')
# from TreePlotter import *
from decisionTree_1 import TreePlotter
from DT_database import SQL_matrix
#'''
from decisionTree_1 import TreePlotter


'''
https://blog.csdn.net/u012421852/article/details/79808223?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165079769516780366593959%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=165079769516780366593959&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-5-79808223.142^v9^pc_search_result_cache,157^v4^control&utm_term=c4.5%E5%86%B3%E7%AD%96%E6%A0%91python&spm=1018.2226.3001.4187
'''

# -*- coding: utf-8 -*-
""" 
@author: 蔚蓝的天空Tom 
Talk is cheap,show me the code 
Aim:C4.5算法生成决策树(字典存储), 并绘制决策树图形
"""

import numpy as np
import math
import matplotlib.pyplot as plt

varnamestr = lambda v, nms: [vn for vn in nms if id(v) == id(nms[vn])][0]


class CUtileTool(object):
    '''提供有用的方法 比如dump_list方法，可以打印给定的list的相关信息'''

    def dump_list(self, src_list, src_list_namestr):
        '''逐行打印list
        :param self:类实例自身
        :param src_list:被打印的源list
        :return 无
        '''
        print('\n============', src_list_namestr, '================')
        list_len = len(src_list)
        list_shape = np.shape(src_list)
        print('type(', src_list_namestr, '):', type(src_list))  # <class 'list'>
        print('np.shape(', src_list_namestr, '):', np.shape(src_list))
        if 1 == len(list_shape):
            print(src_list)
        elif 2 == len(list_shape):
            for i in range(list_len):
                if 0 == i:
                    print('[', src_list[i])
                elif (list_len - 1) == i:
                    print(src_list[i], ']')
                else:
                    print(src_list[i])
        else:
            print(src_list)
        print('======\n')
        return

    def dump_array(self, src_a, src_dict_namestr):
        '''''
        逐行打印array
        :param self:类实例自身
        :param src_a:被打印的源array
        :return 无
        '''
        print('\n===============', src_dict_namestr, '===================')
        a_len = len(src_a)
        a_shape = np.shape(src_a)
        print('type(', src_dict_namestr, '):', type(src_a))  # <class 'list'>
        print('np.shape(', src_dict_namestr, '):', np.shape(src_a))
        if 1 == len(a_shape):
            print(src_a)
        elif 2 == len(a_shape):
            for i in range(a_len):
                if 0 == i:
                    print('[', src_a[i])
                elif (a_len - 1) == i:
                    print(src_a[i], ']')
                else:
                    print(src_a[i])
        else:
            print(src_a)
        print('======\n')
        return

    def print_dict(self, src_dict, level, src_dict_namestr=''):
        '''''
        逐行打印dict
        :param self:类实例自身
        :param src_dict:被打印的dict
        :param level:递归level，初次调用为level=0
        :param src_dict_namestr:对象变量名称字符串
        '''
        if isinstance(src_dict, dict):
            tab_str = '\t'
            for i in range(level):
                tab_str += '\t'
            if 0 == level:
                print(src_dict_namestr, '= {')
            for key, value in src_dict.items():
                if isinstance(value, dict):
                    has_dict = False
                    for k, v in value.items():
                        if isinstance(v, dict):
                            has_dict = True
                    if has_dict:
                        print(tab_str, key, ":{")
                        self.print_dict(value, level + 1)
                    else:
                        print(tab_str, key, ':', value)
                else:
                    print(tab_str, key, ': ', value, )
            print(tab_str, '}')

    def dump_dict(self, src_dict, src_dict_namestr):
        '''''
        逐行打印dict
        :param self:类实例自身
        :param src_dict:被打印的dict对象
        :return 无
        '''
        print('\n===============', src_dict_namestr, '===================')
        dict_len = len(src_dict)
        dict_shape = np.shape(src_dict)
        dict_type = type(src_dict)
        print('len(', src_dict_namestr, '):', dict_len)
        print('type(', src_dict_namestr, '):', dict_type)  # <class 'dict'>
        print('np.shape(', src_dict_namestr, '):', dict_shape)
        print('len(dict_shape):', len(dict_shape))

        self.print_dict(src_dict, 0, src_dict_namestr)
        print('======\n')
        return

    def dump(self, src_thing, src_thing_namestr):
        name = type(src_thing).__name__
        if name == 'list':
            return self.dump_list(src_thing, src_thing_namestr)
        elif name == 'dict':
            return self.dump_dict(src_thing, src_thing_namestr)
        elif name == 'ndarray':
            print('hello')
            return self.dump_array(src_thing, src_thing_namestr)
        else:
            print(src_thing_namestr, ':', src_thing)
        return


class CDictHelper(object):
    '''
    dict helper
    a_dict = {'name':'Tom', 'age':18}
    'name':'Tom' is a item of a_dict
    'name' is key of item
    'Tom' is value of item
    '''

    def add(self, src_dict, key, value):
        if type(src_dict).__name__ != 'dict':
            print('error:expect type is dict, actual %', type(src_dict).__name__)
            return False
        src_dict[key] = value
        return True

    def add_func(self, src_dict, key, value):
        '''dict[key] = value的向量化'''
        func = np.frompyfunc(self.add, 3, 1)
        return func(src_dict, key, value)

    def max_val_pair(self, src_dict, keys):
        if type(src_dict).__name__ != 'dict':
            print('type error:expace dict, acturl', type(src_dict).__name__)
            return None
        ret_key, max_val = None, -9527
        for key in keys:
            if key in src_dict.keys():
                if src_dict[key] > max_val:
                    ret_key, max_val = key, src_dict[key]
        return ret_key  #

    def min_val_pair(self, src_dict, keys):
        if type(src_dict).__name__ != 'dict':
            print('type error:expace dict, acturl', type(src_dict).__name__)
            return None
        ret_key, min_val = None, 9527
        for key in keys:
            if key in src_dict.keys():
                if src_dict[key] < min_val:
                    ret_key, min_val = key, src_dict[key]
        return ret_key

    def agv_item(self, src_dict, parent_keys, child_key):
        '''计算src_dict[parent_key][child_key]的平均值，其中parent_key来自parent_keys'''
        if type(src_dict).__name__ != 'dict':
            print('type error:expace dict, actual', type(src_dict).__name__)
            return None
        ret_avg = 0.0
        cnt = 0.0
        for key in parent_keys:
            if key in src_dict.keys() and child_key in src_dict[key].keys():
                ret_avg += src_dict[key][child_key]
                cnt += 1
        if 0.0 == cnt:
            return None
        return (ret_avg / cnt)

    def max_val_item(self, src_dict, parent_keys, child_key):
        '''max函数和min函数的判断操作符，必须有一个包含等于判断，否则会得出不正确的决策树
        1)>=, <         2)>, <=
        '''
        if type(src_dict).__name__ != 'dict':
            print('type error:expact dict, actual', type(src_dict).__name__)
            return None
        ret_key, max_val = None, -9527
        for key in parent_keys:
            if key in src_dict.keys() and child_key in src_dict[key].keys():
                # if src_dict[key][child_key] >= max_val:#配对的min必须使用<
                if src_dict[key][child_key] > max_val:  # 配对的min必须使用<=
                    ret_key, max_val = key, src_dict[key][child_key]
        avg = self.agv_item(src_dict, parent_keys, child_key)
        if avg != None:
            if max_val <= avg:
                return None
        return ret_key

    def min_val_item(self, src_dict, parent_keys, child_key):
        if type(src_dict).__name__ != 'dict':
            print('type error:expace dict, acturl', type(src_dict).__name__)
            return None
        ret_key, min_val = None, 9527
        for key in parent_keys:
            if key in src_dict.keys() and child_key in src_dict[key].keys():
                # if src_dict[key][child_key] < min_val:#配对的max必须使用>=
                if src_dict[key][child_key] <= min_val:  # 配对的max必须使用>
                    ret_key, min_val = key, src_dict[key][child_key]
        return ret_key


'''CTailorSamples
裁剪规格简介
#每个样本example的特征列表
feature_type_list = ['youth','work','hourse','credit']
即每个样本=[age_value, work_value, housr_value, crdit_value, class_label]
如下一个样本集：
samples_list = [ ['youth', 'work_no', 'no', '1', 'refuse']
                 ['youth', 'work_no', 'no', '2', 'refuse']
                 ['youth', 'work_yes', 'no', '2', 'agree']
                 ['youth', 'work_yes', 'yes', '1', 'agree']
                 ['youth', 'work_no', 'no', '1', 'refuse']
                 ['mid', 'work_no', 'no', '1', 'refuse']
                 ['mid', 'work_no', 'no', '2', 'refuse']
                 ['mid', 'work_yes', 'yes', '2', 'agree']
                 ['mid', 'work_no', 'yes', '3', 'agree']
                 ['mid', 'work_no', 'yes', '3', 'agree']
                 ['elder', 'work_no', 'yes', '3', 'agree']
                 ['elder', 'work_no', 'yes', '2', 'agree']
                 ['elder', 'work_yes', 'no', '2', 'agree']
                 ['elder', 'work_yes', 'no', '3', 'agree']
                 ['elder', 'work_no', 'no', '1', 'refuse'] ]
假设已经通过信息增益选出此样本集的决策树的最优根节点为特征housre
如果想求子决策树的最优根节点的话，就需要对原始样本集进行裁剪了，然后用新的样本集筛选新的最优根节点
#通过如下规则得到新的样本集
step1:删除hourse特征值为yes所在的所有行
step2:然后再删除hourse特征值列
'''


class CTailorSamples(object):
    '''裁剪样本集'''

    def __init__(self, data_list, feat_type_list, feat_type_index, feat_value):
        self.data_list = data_list
        self.feat_type_list = feat_type_list
        self.feat_type_index_tailed = feat_type_index
        self.feat_value_tailed = feat_value
        self.tailer_work()  # 裁剪

    def get_samples(self):
        '''返回裁剪后的样本集，特征类型列表'''
        return self.data_list, self.feat_type_list

    def get_all_indexs(self, src_list, dst_value):
        '''内部工具函数，请不要外部调用
        返回给定值的所有元素的下标
        src_list, e= [10,20,30,30,30,50], 30
        indexs_list = tailor.get_all_indexs(src_list, e)
        print(indexs_list) #[2, 3, 4]
        '''
        dst_val_index = [i for i, x in enumerate(src_list) if x == dst_value]
        return dst_val_index

    def tailer_work(self):
        '''内部工具函数，请不要外部调用
        裁剪得到新的特征列表
        '''
        del self.feat_type_list[self.feat_type_index_tailed]
        # 摘取被删除的特征列
        colum_to_del = self.feat_type_index_tailed
        self.feat_value_list = [example[colum_to_del] for example in self.data_list]
        # 找出含有self.feat_value_tailed特征值的所有样本所在行的下标
        rows_to_del = self.get_all_indexs(self.feat_value_list, self.feat_value_tailed)
        # 删除row_index_list中行下标对应的self.src_data_list的行
        # 技巧：从大的行下标开始依次删除
        # for row in list(reversed(rows_to_del)):
        # for row in rows_to_del[::-1]:
        rows_to_del.reverse()
        for row in rows_to_del:
            del self.data_list[row]
        # 删除给定的特征列
        for row in range(len(self.data_list)):
            del self.data_list[row][colum_to_del]
        return self.data_list, self.feat_type_list


class CC4dot5DecisionTree(object):
    '提供样本集的摘取目标数据的方法'

    def __init__(self, data_list, feat_list, leastFeatNum):
        '''''
        初始化函数
        :param data_list:数据集
        :param feat_list:数据的特征类型列表
        :return 无
        '''

        '''self.data_list 样例： 
        [['youth', 'no',  'no',   '1', 'refuse'], 
         ['youth', 'no',  'no',   '2', 'refuse']] 
        '''
        self.data_list = data_list

        '''self.feat_list样例['age', 'working', 'house', 'credit']'''
        self.feat_list = feat_list

        '''至少有leastFeatNum个特征，才求样本集的决策树'''
        self.leastFeatNum = leastFeatNum

        '''样本集的香农熵,H(Y={refuse, agree})'''
        self.samples_shanon_entropy = 0.0

        '''''self.n_feats 就是每个样本的特征值类型总数'''
        self.n_feats = len(feat_list)

        ''''' 
        self.feat_value_list 每种类型特征的取值列表, 样例: 
        [
          ['no','no','no','yes','no','no','no','yes','yes','yes','yes','yes','no','no','no'] 
          ['1', '2', '2', '1', '1', '1', '2', '2', '3', '3', '3', '2', '2', '3', '1']
        ] 
        '''
        self.feat_value_list = []

        ''''' 
        self.class_list 样本集的分类标签取值列表，长度为样本总数，样例： 
        ['refuse', 'refuse', 'agree', …… ,'agree', 'agree', 'refuse'] 
        '''
        self.class_list = []

        ''''' 
        self.stat_dict 样本集的统计字典，样例： 
        {
         age :{
                 mid :{
                         cnt :  5.0
                         ent :  0.9709505944546686
                         p_self :  0.3333333333333333
                         refuse : {'cnt': 2, 'p_self': 0.4}
                         agree : {'cnt': 3, 'p_self': 0.6}
                         }
                 info_gain :  0.08300749985576883
                 elder :{
                         cnt :  5.0
                         ent :  0.7219280948873623
                         p_self :  0.3333333333333333
                         refuse : {'cnt': 1, 'p_self': 0.2}
                         agree : {'cnt': 4, 'p_self': 0.8}
                         }
                 cond_ent :  0.8879430945988998
                 youth :{
                         cnt :  5.0
                         ent :  0.9709505944546686
                         p_self :  0.3333333333333333
                         refuse : {'cnt': 3, 'p_self': 0.6}
                         agree : {'cnt': 2, 'p_self': 0.4}
                         }
                 }
         working :{
                 no :{
                         cnt :  10.0
                         ent :  0.9709505944546686
                         p_self :  0.6666666666666666
                         refuse : {'cnt': 6, 'p_self': 0.6}
                         agree : {'cnt': 4, 'p_self': 0.4}
                         }
                 info_gain :  0.32365019815155627
                 cond_ent :  0.6473003963031123
                 yes :{
                         cnt :  5.0
                         ent :  0.0
                         p_self :  0.3333333333333333
                         refuse : {'cnt': 0, 'p_self': 0.0}
                         agree : {'cnt': 5, 'p_self': 1.0}
                         }
                 }
         samples_ent :  0.9709505944546686
         credit :{
                 1 :{
                         cnt :  5.0
                         ent :  0.7219280948873623
                         p_self :  0.3333333333333333
                         refuse : {'cnt': 4, 'p_self': 0.8}
                         agree : {'cnt': 1, 'p_self': 0.2}
                         }
                 3 :{
                         cnt :  4.0
                         ent :  0.0
                         p_self :  0.26666666666666666
                         refuse : {'cnt': 0, 'p_self': 0.0}
                         agree : {'cnt': 4, 'p_self': 1.0}
                         }
                 info_gain :  0.36298956253708536
                 2 :{
                         cnt :  6.0
                         ent :  0.9182958340544896
                         p_self :  0.4
                         refuse : {'cnt': 2, 'p_self': 0.3333333333333333}
                         agree : {'cnt': 4, 'p_self': 0.6666666666666666}
                         }
                 cond_ent :  0.6079610319175832
                 }
         house :{
                 no :{
                         cnt :  9.0
                         ent :  0.9182958340544896
                         p_self :  0.6
                         refuse : {'cnt': 6, 'p_self': 0.6666666666666666}
                         agree : {'cnt': 3, 'p_self': 0.3333333333333333}
                         }
                 info_gain :  0.4199730940219749
                 cond_ent :  0.5509775004326937
                 yes :{
                         cnt :  6.0
                         ent :  0.0
                         p_self :  0.4
                         refuse : {'cnt': 0, 'p_self': 0.0}
                         agree : {'cnt': 6, 'p_self': 1.0}
                         }
                 }
         }
        '''
        '''样本集的统计字典'''
        self.stat_dict = {}

        '''决策树字典, 供绘制者使用
        tree_dict = {
         house :{
                 no :{
                         working :{
                                 no :{
                                         age : {'elder': 'refuse', 'youth': 'refuse'}
                                         }
                                 yes :  agree
                                 }
                         }
                 yes :  agree
                 }
         }
         '''
        self.tree_dict = {}

        self.pickout_feat()
        self.pickout_class()
        self.pickout_samples_shannon_entropy()
        self.build_stat_dict()
        return  # end of __init__()

    def get_example_cnt(self, feat_values, val, class_values, label):
        '''
        feat_values = ['high','high','high','low']
        class_values = ['refuse','refuse','agree','refuse']
        相同index时，特征值为high且分类值为refuse的总数，即2
        '''
        if type(feat_values).__name__ != 'list':
            print('type error:param1 expect list, actual', type(feat_values).__name__)
            return None
        if type(class_values).__name__ != 'list':
            print('type error:param2 expect list, actual', type(feat_values).__name__)
            return None
        if len(feat_values) != len(class_values):
            print('len error:param1 and param2 are of different length')
            return None

        ret_cnt = 0
        for i in range(len(feat_values)):
            pair_tuple = (feat_values[i], class_values[i])
            if pair_tuple == (val, label):
                ret_cnt += 1
        return ret_cnt

    def shan_ent_ele(self, p):
        if 0 == p:
            return 0
        else:
            return -1 * p * math.log2(p)

    def shan_ent(self, P):
        '''样本概率, 如P=[0.4,0.6]'''
        func = np.frompyfunc(self.shan_ent_ele, 1, 1)
        ent_ele_list = func(P)
        entropy = ent_ele_list.sum()
        return entropy

    def pickout_feat(self):
        '''摘取每种类型特征的特征值'''
        self.feat_value_list = []
        for dim in range(self.n_feats):
            curtype_feat = [example[dim] for example in self.data_list]
            self.feat_value_list.append(curtype_feat)
        return self.feat_value_list

    def pickout_class(self):
        '''摘取分类列表，大小一定是m×1 '''
        self.class_list = [example[-1] for example in self.data_list]
        return self.class_list

    def pickout_samples_shannon_entropy(self):
        '''计算样本集的香农熵，H(Y={refuse, agree})'''
        # 统计样本集的分类标签分布
        label_set = set(self.class_list)
        label_cnt_list = []
        for label in label_set:
            label_cnt_list.append(self.class_list.count(label))
            # 统计样本集分类标签概率密度
        n_samples = len(self.class_list)
        label_prob_list = [label_cnt / n_samples for label_cnt in label_cnt_list]
        # 计算样本集的香农熵
        self.samples_shanon_entropy = self.shan_ent(label_prob_list)
        return self.samples_shanon_entropy

    def feat_info_gain_ratio(self, feat_info_gain, val_pden):
        '''计算给定特征的信息增益比
        :param self 类实例本身
        :param info_gain 特征的信息增益
        :param val_pden 特征的值得概率密度
        :return 特征的信息增益比
        '''
        val_ent = self.shan_ent(val_pden)
        if 0 == val_ent:
            return 0
        else:
            return feat_info_gain * 1.0 / val_ent

    def get_stat_dict(self):
        return self.stat_dict

    def build_stat_dict(self):
        '''核心函数'''
        self.stat_dict = dict({})
        self.stat_dict['samples_ent'] = self.samples_shanon_entropy
        self.stat_dict['samples_cnt'] = len(self.data_list)
        class_vals, class_set = self.class_list, set(self.class_list)  # class values, class value set
        for i in range(self.n_feats):  # for feat in [age, house, work, cedit]
            feat, vals, val_set = self.feat_list[i], self.feat_value_list[i], set(self.feat_value_list[i])
            feat_c_ent, val_pden = 0, []  # feat-conditional-enttropy, feat-value-probability-density
            self.stat_dict[feat] = {}
            for val in val_set:  # for val in {youth, mid, elder}
                val_p_self = vals.count(val) * 1.0 / len(vals)
                val_pden.append(val_p_self)
                val_ent, val_labels, label_dist, label_pden = 0, [], [], []
                for label in class_set:  # for label in {agree, refuse}
                    val_labels.append(label)
                    n_label = self.get_example_cnt(vals, val, class_vals, label)
                    label_dist.append(n_label)
                    label_pden.append(n_label * 1.0 / vals.count(val))
                val_ent = self.shan_ent(label_pden)
                feat_c_ent += val_p_self * val_ent  # update feat cond-entropy
                self.stat_dict[feat][val] = {}
                self.stat_dict[feat][val]['cnt'] = vals.count(val)
                self.stat_dict[feat][val]['p_self'] = val_p_self
                self.stat_dict[feat][val]['ent'] = val_ent
                for i in range(len(class_set)):  # 填充value的分类样本分布和概率密度
                    if val_labels[i] not in self.stat_dict[feat][val].keys():
                        self.stat_dict[feat][val][val_labels[i]] = {}
                    self.stat_dict[feat][val][val_labels[i]]['cnt'] = label_dist[i]
                    self.stat_dict[feat][val][val_labels[i]]['p_self'] = label_pden[i]
            self.stat_dict[feat]['cond_ent'] = feat_c_ent
            self.stat_dict[feat]['info_gain'] = self.samples_shanon_entropy - feat_c_ent
            self.stat_dict[feat]['gain_ratio'] = self.feat_info_gain_ratio(self.stat_dict[feat]['info_gain'], val_pden)
        return self.stat_dict

    def get_tree_dict(self):
        return self.tree_dict

    def create_tree(self):
        '''对外核心函数'''
        dh = CDictHelper()
        # root
        root = dh.max_val_item(self.stat_dict, self.feat_list, 'gain_ratio')
        if (root == None):
            return None
        feat, feat_ind = root, self.feat_list.index(root)
        # lcond, rcond
        val_set = set(self.feat_value_list[feat_ind])
        rcond = value = dh.min_val_item(self.stat_dict[feat], val_set, 'ent')
        lcond = dh.max_val_item(self.stat_dict[feat], val_set, 'ent')
        # lnode, rnode
        class_set = set(self.class_list)
        rnode = dh.max_val_item(self.stat_dict[feat][value], class_set, 'p_self')
        lnode = dh.min_val_item(self.stat_dict[feat][value], class_set, 'p_self')
        # 子树作为lnode,裁剪数据得到子树的样本数据
        if self.n_feats >= self.leastFeatNum:
            tailor = CTailorSamples(self.data_list, self.feat_list, feat_ind, value)
            new_samples_list, new_feat_list = tailor.get_samples()
            child_examples = CC4dot5DecisionTree(new_samples_list, new_feat_list, self.leastFeatNum)
            child_tree = child_examples.create_tree()
            if child_tree != None:
                lnode = child_tree
        # 填充决策树
        self.tree_dict = {}
        self.tree_dict[root] = {}
        self.tree_dict[root][rcond] = rnode
        self.tree_dict[root][lcond] = lnode
        return self.tree_dict


# 定义判断结点形状,其中boxstyle表示文本框类型,fc指的是注释框颜色的深度
decisionNode = dict(boxstyle="round4", color='r', fc='0.9')
# 定义叶结点形状
leafNode = dict(boxstyle="circle", color='m')
# 定义父节点指向子节点或叶子的箭头形状
arrow_args = dict(arrowstyle="<-", color='g')


def plot_node(node_txt, center_point, parent_point, node_style):
    ''' 内部函数，外部不要调用
    绘制父子节点，节点间的箭头，并填充箭头中间上的文本
    :param node_txt:文本内容
    :param center_point:文本中心点
    :param parent_point:指向文本中心的点
    '''
    createPlot.ax1.annotate(node_txt,
                            xy=parent_point,
                            xycoords='axes fraction',
                            xytext=center_point,
                            textcoords='axes fraction',
                            va="center",
                            ha="center",
                            bbox=node_style,
                            arrowprops=arrow_args)


def get_leafs_num(tree_dict):
    '''内部函数，外部不要调用
    获取叶节点的个数
    :param tree_dict:树的数据字典
    :return tree_dict的叶节点总个数
    '''
    # tree_dict的叶节点总数
    leafs_num = 0
    if len(tree_dict.keys()) == 0:
        print('input tree dict is void!!!!!')
        return 0
    # 字典的第一个键，也就是树的第一个节点
    root = list(tree_dict.keys())[0]
    # 这个键所对应的值，即该节点的所有子树。
    child_tree_dict = tree_dict[root]
    for key in child_tree_dict.keys():
        # 检测子树是否字典型
        if type(child_tree_dict[key]).__name__ == 'dict':
            # 子树是字典型，则当前树的叶节点数加上此子树的叶节点数
            leafs_num += get_leafs_num(child_tree_dict[key])
        else:
            # 子树不是字典型，则当前树的叶节点数加1
            leafs_num += 1
    # 返回tree_dict的叶节点总数
    return leafs_num


def get_tree_max_depth(tree_dict):
    ''' 内部函数，外部不要调用
    求树的最深层数
    :param tree_dict:树的字典存储
    :return tree_dict的最深层数
    '''
    # tree_dict的最深层数
    max_depth = 0
    if len(tree_dict.keys()) == 0:
        print('input tree_dict is void!')
        return 0
    # 树的根节点
    root = list(tree_dict.keys())[0]
    # 当前树的所有子树的字典
    child_tree_dict = tree_dict[root]
    for key in child_tree_dict.keys():
        # 树的当前分支的层数
        this_path_depth = 0
        # 检测子树是否字典型
        if type(child_tree_dict[key]).__name__ == 'dict':
            # 如果子树是字典型，则当前分支的层数需要加上子树的最深层数
            this_path_depth = 1 + get_tree_max_depth(child_tree_dict[key])
        else:
            # 如果子树不是字典型，则是叶节点，则当前分支的层数为1
            this_path_depth = 1
        if this_path_depth > max_depth:
            max_depth = this_path_depth
    # 返回tree_dict的最深层数
    return max_depth


def plot_mid_text(center_point, parent_point, txt_str):
    '''内部函数，外部不要调用: 计算父节点和子节点的中间位置，并在父子节点间填充文本信息
    :param center_point:文本中心点
    :param parent_point:指向文本中心点的点
    '''
    x_mid = (parent_point[0] - center_point[0]) / 2.0 + center_point[0]
    y_mid = (parent_point[1] - center_point[1]) / 2.0 + center_point[1]
    createPlot.ax1.text(x_mid, y_mid, txt_str)
    return


def plotTree(tree_dict, parent_point, node_txt):
    '''内部函数，外部不要调用：绘制树
    :param tree_dict:树
    :param parent_point:父节点位置
    :param node_txt:节点内容
    '''
    leafs_num = get_leafs_num(tree_dict)
    root = list(tree_dict.keys())[0]
    # plotTree.totalW表示树的深度
    center_point = (plotTree.xOff + (1.0 + float(leafs_num)) / 2.0 / plotTree.totalW, plotTree.yOff)
    # 填充node_txt内容
    plot_mid_text(center_point, parent_point, node_txt)
    # 绘制箭头上的内容
    plot_node(root, center_point, parent_point, decisionNode)
    # 子树
    child_tree_dict = tree_dict[root]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    # 因从上往下画，所以需要依次递减y的坐标值，plotTree.totalD表示存储树的深度
    for key in child_tree_dict.keys():
        if type(child_tree_dict[key]).__name__ == 'dict':
            plotTree(child_tree_dict[key], center_point, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plot_node(child_tree_dict[key],
                      (plotTree.xOff, plotTree.yOff),
                      center_point, leafNode)
            plot_mid_text((plotTree.xOff, plotTree.yOff), center_point, str(key))
    # h绘制完所有子节点后，增加全局变量Y的偏移
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
    return


def createPlot(tree_dict):
    '''唯一对外函数：绘制决策树图形
    :param tree_dict
    :return 无
    '''
    # 设置绘图区域的背景色
    fig = plt.figure(1, facecolor='white')
    # 清空绘图区域
    fig.clf()
    # 定义横纵坐标轴,注意不要设置xticks和yticks的值!!!
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    # 由全局变量createPlot.ax1定义一个绘图区，111表示一行一列的第一个，frameon表示边框,**axprops不显示刻度
    plotTree.totalW = float(get_leafs_num(tree_dict))
    plotTree.totalD = float(get_tree_max_depth(tree_dict))
    if plotTree.totalW == 0:
        print('tree_dict is void~')
        return
    plotTree.xOff = -0.5 / plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(tree_dict, (0.5, 1.0), '')
    plt.show()


def create_samples():
    '''''
    提供训练样本集
    每个example由多个特征值+1个分类标签值组成
    比如第一个example=['youth', 'no', 'no', '1', 'refuse'],此样本的含义可以解读为：
    如果一个人的条件是：youth age，no working, no house, 信誉值credit为1
    则此类人会被分类到refuse一类中，即在相亲中被拒绝(也可以理解为银行拒绝为此人贷款)
    每个example的特征值类型为：
    ['age', 'working', 'house', 'credit']
    每个example的分类标签class_label取值范围为：'refuse'或者'agree'
    '''


    '''
    data_list = [['youth', 'no', 'no', '1', 'refuse'],
                 ['youth', 'no', 'no', '2', 'refuse'],
                 ['youth', 'yes', 'no', '2', 'agree'],
                 ['youth', 'yes', 'yes', '1', 'agree'],
                 ['youth', 'no', 'no', '1', 'refuse'],
                 ['mid', 'no', 'no', '1', 'refuse'],
                 ['mid', 'no', 'no', '2', 'refuse'],
                 ['mid', 'yes', 'yes', '2', 'agree'],
                 ['mid', 'no', 'yes', '3', 'agree'],
                 ['mid', 'no', 'yes', '3', 'agree'],
                 ['elder', 'no', 'yes', '3', 'agree'],
                 ['elder', 'no', 'yes', '2', 'agree'],
                 ['elder', 'yes', 'no', '2', 'agree'],
                 ['elder', 'yes', 'no', '3', 'agree'],
                 ['elder', 'no', 'no', '1', 'refuse']]
    feat_list = ['age', 'working', 'house', 'credit']
    return data_list, feat_list
    #'''

    data_list = [
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

    data_list = SQL_matrix.to_mat1("sql_pyc", "stu_w1")

    feat_list = ['奖学金情况', '入学-毕业成绩变动大小', '曾参与项目级别', '参与社团数', '成绩', '兼职']
    return data_list, feat_list



if __name__ == '__main__':
    # 创建样本集
    train_data_list, feat_list = create_samples()
    # 决策树生成终止的条件,当样本的特征少于leastFeatNum个时，不再继续求样本集的决策树
    leastFeatNum = 1
    # 创建ID3算法生成决策树类的对象
    samples = CC4dot5DecisionTree(train_data_list, feat_list, leastFeatNum)
    # 生成决策树字典
    samples.create_tree()
    # 打印样本集的统计字典
    CUtileTool().dump(samples.get_stat_dict(), 'samples statistic dict')
    # 打印决策树字典
    CUtileTool().dump(samples.get_tree_dict(), 'samples decision-tree dict')
    # 绘制决策树
    # createPlot(samples.get_tree_dict())
    TreePlotter.createPlot(samples.get_tree_dict())




