


'''
#输入数组并排序
l=[]
for i in range(4):
    x=int(input("please enter a int:"))
    l.append(x)
l.sort(reversed())
print(l)

'''

# 画五角星
import turtle as t
def draw_fiveStars(leng):
    count=1
    while count<=5:
        t.forward(leng)
        t.right(144)        #向右旋转144度
        count+=1
    leng+=16
    if leng<=128:
        draw_fiveStars(leng)


def main():
    t.penup()               #抬起画笔
    t.back(100)             #像素位移量100
    t.pendown()
    t.pensize(2)
    t.pencolor('red')
    segment=64              #五角星初始长度
    draw_fiveStars(segment)
    t.textinput()

if __name__=="__main__":
    main()