
'''
https://blog.csdn.net/weixin_56705224/article/details/122578379
'''

import pymysql

#键盘输入
import sys

#___________________________________________________输入传值




sno= "201215129"
Sname= "李alkhjfksadfkjl"
Ssex= "男"
Sage= "20"
Sdept= "CS"



#___________________________________________________数据库相关
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

#创建sql语句（这里是查询SQL版本）：
sql='select version()'
#查看当前用户能够查看的所有数据库：
sql1='SHOW DATABASES'
#查看student表中所有数据：
sql2='use dt_k'
cursor.execute(sql2)
sql2=("select * from student")
#查询student表的表结构：
sql3='use dt_k'
cursor.execute(sql3)
sql3=('desc student')


#在student表中插入一条数据:____________________________________________增
'''
sql3='use dt_k'
cursor.execute(sql3)
in1=[(sno,Sname,Ssex,Sage,Sdept)]
try:
    cursor.executemany("insert into student(sno,Sname,Ssex,Sage,Sdept) values(%s,%s,%s,%s,%s)",in1)
    # 执行sql语句,插入多条数据
    db.commit()
    # 提交数据
except:
    db.rollback()
    # 发生错误时回滚
#'''



#在student表中删除一条数据（sno= "201215129"）:____________________________________________删
'''
#删除前的对比
cursor.execute(sql2)
print(cursor.fetchall())

cursor.execute('use dt_k')
in2=[(sno)]
try:
    cursor.executemany("delete from student where sno like %s",in2)
    # 执行sql语句,删除多条数据
    db.commit()
    # 提交数据
except:
    db.rollback()
    # 发生错误时回滚
#'''





#在student表中修改一条数据（sno= "201215129"）——姓名改为（赵1024）:____________________________________________改
'''
#修改前的对比
cursor.execute(sql2)
print(cursor.fetchall(),'\n')

cursor.execute('use dt_k')
Sname="赵1024"
in3=[(Sname,sno)]
try:
    cursor.executemany("update student set Sname=%s where sno like %s",in3)
    # 执行sql语句,修改数据
    db.commit()
    # 提交数据
except:
    db.rollback()
    # 发生错误时回滚
#'''



#执行SQL语句：
#cursor.executemany(sql4)

cursor.execute(sql2)

#提交数据


#将运行结果保存
data=cursor.fetchall()

#退出数据库：
db.close();

print(data)

