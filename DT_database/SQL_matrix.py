
#数据库：
import pymysql
#矩阵：
import numpy as np
new_array = np.zeros((5,3))

def to_mat(a,b):#a为数据库名；b为表名
    # ___________________________________________________数据库相关
    # 链接数据库：
    db = pymysql.connect(
        user="root",
        password="12345678",
        host="127.0.0.1",
        # db="DT_K",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    # """
    # 输出watermelon表的所有信息：
    # cursor.execute('use sql_pyc')
    # cursor.execute("select * from watermelon")
    cursor.execute("use "+a)
    cursor.execute("select * from "+b)

    # 将运行结果保存
    data = cursor.fetchall()

    # 退出数据库：
    db.close();

    #print(data[0])
    # print(data[2])
    # print(data)
    #print(type(data[0]))       #输出type里边的东西的类型
    # 字典转数组：(list(****.values()))
    dc1 = []
    for i in range(len(data)):
        dc1.append(list(data[i].values()))
    # """
    return dc1

    # for i in range(len(data)):
    #     print(dc1[i])



def to_mat1(a,b):#a为数据库名；b为表名
    # ___________________________________________________去掉了第一列！！！
    # 链接数据库：
    db = pymysql.connect(
        user="root",
        password="12345678",
        host="127.0.0.1",
        # db="DT_K",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    # """
    # 输出watermelon表的所有信息：
    # cursor.execute('use sql_pyc')
    # cursor.execute("select * from watermelon")
    cursor.execute("use "+a)
    cursor.execute("select * from "+b)

    # 将运行结果保存
    data = cursor.fetchall()

    # 退出数据库：
    db.close();

    #print(data[0])
    # print(data[2])
    # print(data)
    #print(type(data[0]))       #输出type里边的东西的类型
    # 字典转数组：(list(****.values()))
    dc1 = []
    for i in range(len(data)):
        rr=list(data[i].values())
        del(rr[0])
        dc1.append(rr)
    # """
    return dc1

    # for i in range(len(data)):
    #     print(dc1[i])


#输出表结构
def to_mac(a,b):#a为数据库名；b为表名
    # ___________________________________________________数据库相关
    # 链接数据库：
    db = pymysql.connect(
        user="root",
        password="12345678",
        host="127.0.0.1",
        # db="DT_K",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    # """
    # 输出watermelon表的所有信息：
    # cursor.execute('use sql_pyc')
    # cursor.execute("select * from watermelon")
    cursor.execute("use "+a)
    cc="select ",a," from information_schema.COLUMNS where table_name = '",b,"'"
    cursor.execute("show columns from",b)

    # 将运行结果保存
    data = cursor.fetchall()

    # 退出数据库：
    db.close();

    return data

    #print(data[0])
    # print(data[2])
    # print(data)
    #print(type(data[0]))       #输出type里边的东西的类型
    # 字典转数组：(list(****.values()))
    dc1 = []
    for i in range(len(data)):
        dc1.append(list(data[i].values()))
    # """
    return dc1

    # for i in range(len(data)):
    #     print(dc1[i])

# test
# print(to_mac("sql_pyc","stu_w1"))


