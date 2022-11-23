




#摄氏度转绝对温度
# str = float(input("Enter your first input: "))
# print ("Received input is : ", str+273.15)
#
# # 根据半径求面积
# str = float(input("Enter your second input: "))
# print ("Received input is : ", (str*str*3.1415926535))

'''

# # 运煤
str = 29.5-3*4
stc=str/2.5
if stc*2.5<str:
    stc+=1
print ("Received input is : ", stc)
'''

'''#format函数
a=123
b=456
print("\nadf\t{}\nsdf\t{}".format(a,b))
#'''


'''
num=int(input("请输入要转换的整数:\n"))
change=input("请选择转换的进制：二、八、十、十六\n")
if change=='2':
    print(f'进制转换后的数字为：{bin(num)}')
elif change=='8':
    print('进制转换后的数字：%s'%(oct(num)))
elif change=='10':
    print('进制转换后的数字：%d'%int(num))
else:
    print('进制转换后的数字：{}'.format(hex(num)))
#'''

'''#打印进度条
import time
for i in range(101):
    print('\r',f'进度：{i}%[','*'*(i//1),' '*(100-(i)),']',end="")
    time.sleep(.02)
#'''





#'''
p1=[[0 for j in range(2)]for i in range(2)]
p1=[[1,2],
    [3,4]]
A=p1[0][0]*p1[1][1]-p1[1][0]*p1[1][1]
print('矩阵的行列式为：',A)
#'''




