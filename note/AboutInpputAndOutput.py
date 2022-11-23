



#输入方案_通过引用方法____________________________________
'''
# import sys
# x=sys.stdin.readline(16)
# print(x)
'''


'''
from pip._vendor.distlib.compat import raw_input
str = raw_input("Enter your input: ")
print ("Received input is : ", str)
#input() 函数和raw_input() 函数基本能够互换。可是input会如果你的输入是一个有效的Python表达式，并返回运算结果。这应该是两者的最大差别。
'''



#常规输入方案___________________________________________
'''
#单行输入
n=input()                       #无参数 默认返回字符串
n=input("有提示参数的输入")         #有提示性输入语句的输入，仍以str类型结尾
n=int(input())                  #根据给定的类型输入，返回值类型  int
n=float(input())                #根据给定的类型输入，返回值类型  float
n=eval(input())                 #eveal() 函数用来执行一个字符串表达式，并返回表达式的值。也可用于返回数据本身的类型
'''


'''
#多行输入
a,b=input().split(" ")          #输入字符串（默认返回类型）a和b以（空格）分开
a,b,c=eval(input())             #分别输入三个值（任何类型） 中间由逗号分隔
a,b,c=int(input())              #输入三个值（int） 中间由逗号分隔
a,b,c=map(eval,input().split(" "))      #输入三个值（任何类型）中间由（空格）分隔
a,b,c=map(int,input().split(" "))       #输入三个值（int）  中间由（空格）分隔
'''


'''
#一行输入
#方法1
lst=list(map(int,input().split(" ")))       #输入一个值（int）由（空格）分隔 存入列表

#方法2  输入n个数
n=int(input())
s=input()   #将数一行输入  空格分隔
lst=[]
for i in s.split(" "):
    lst.append(int(i))

#两种输出方式：
for i in list:
    print(i+" ")

for i in range(n):
    print(lst[i]+" ")
'''


#
#
#




