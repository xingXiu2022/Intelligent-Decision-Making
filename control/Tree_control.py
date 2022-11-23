
import os



while True:
    a = int(input("请选择：\n1:ID3\n2:C45\n3:Cart\n0:exit\n"))
    if a == 1:
        os.system("python ../ID3/Jc1K_DB.py")
    elif a == 2:
        os.system("python ../C45/C45b_DB.py")
    elif a == 3:
        os.system("python ../Cart/cart_a_DB.py")
    else:
        break





