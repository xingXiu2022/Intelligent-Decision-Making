
#数据库：
import pymysql
#矩阵：
import numpy as np
new_array = np.zeros((5,3))


#___________________________________________________数据库相关
#'''
#链接数据库：
db=pymysql.connect(
    user="root",
    password="12345678",
    host="127.0.0.1",
    #db="DT_K",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)
cursor=db.cursor()
#'''
"""
#输出watermelon表的所有信息：
cursor.execute('use sql_pyc')
cursor.execute("select * from watermelon")

#将运行结果保存
data=cursor.fetchall()

#退出数据库：
db.close()

print(data[0]["色泽"])
# print(data[2])
print(data)
print(type(data[0]))
#字典转数组：(list(****.values()))
dc1=[] 
for i in range(len(data)):      #len(data):表示data的长度
    dc1.append(list(data[i].values()))


for i in range(len(data)):
    print(dc1[i])

#"""




#-------------------------------------------------------------------------
"""
import pymysql

#db = pymysql.connect(host="localhost", user="root", passwd="12345678", db="", post=3306, charset="utf8");
str = "select * from watermelon";
#cursor = db.cursor()
cursor.execute('use sql_pyc')
try:
    cursor.execute("select * from watermelon")
    index = cursor.description  # 列描述
    result = []
    db.commit()
    for res in cursor.fetchall():  # 返回的全部结果
        row = {}
        for i in range(len(index) - 1):
            row[index[i][0]] = res[i]

        result.append(row)  # result是最后要的dict数组
    print(row)
except:
    db.rollback()
cursor.close()
db.close()
#"""


#-------------------------------------------------------------2
"""
import pymysql
#db = pymysql.connect(host="127.0.0.1", user="root", password="",database="data", port=3306, charset='utf8', )
str = "select * from watermelon";
# str="select * from  userinfo where certificate_no='20200317001' ;"
#cursor = db.cursor()
cursor.execute('use sql_pyc')
'''
try:
    cursor.execute(str)
    desc = cursor.description  # 获取字段的描述
    data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # row是数据库返回的一条一条记录，外侧的这个for是大循环，里边的for提取了数据列描述，                                                                                         #和一条数据合成一个字典，外侧循环将多条记录循环成字典数组
    print(data_dict)
except:
    db.rollback()
cursor.close()
db.close()
#'''
'''
try:
    cursor.execute("select * from watermelon")
    result = cursor.fetchall()  # 所有结果
    column = [index[0] for index in cursor.description]  # 列名
    data_dict = [dict(zip(column, row)) for row in result]  # row是数据库返回的一条一条记录，其中的每一天和column写成字典，最后就是字典数组

    print(data_dict)
except:
    db.rollback()
cursor.close()
#'''
#"""

#------------------------------------------------------------------------------
"""
import pymysql
#db = pymysql.connect(host="", user="", passwd="", db="", post=3306, charset="utf8");
#str = "select * from db1 where usrID="";";
#cursor = db.cursor()
cursor.execute('use sql_pyc')
def new2dict(new):  # 迭代函数
    return dict(zip([x[0] for x in cursor.description], [x for x in new]))  # zip函数
try:
    cursor.excute("select * from watermelon")
    news_list = list(map(new2dict, cursor.fetchall()))  # news_list是转换后的dict数组  这里有map函数
except:
    db.rollback()
cursor.close()
db.close()
#print(news_list)
"""



#################################################################
'''
#字典转列表：
dict={'name':'wsm',
      'age':'22',
      'sex':'female'}

print(list(dict))       #输出键列表
print(list(dict.keys()))        #输出键列表
print(list(dict.values()))      #输出值列表
print(list(dict.items()))       #输出[(键,值),……]列表
#'''
#输出:
# ['name', 'age', 'sex']
# ['name', 'age', 'sex']
# ['wsm', '22', 'female']
# [('name', 'wsm'), ('age', '22'), ('sex', 'female')]
