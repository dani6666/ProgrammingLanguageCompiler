class Helpers:
    def generate_number(number, id):
        if number == 0:
            return "", 0

        code = ""
        lines = 0
        while number > 0:
            lines+=1
            if number % 2 == 0:
                code = "\nSHL "+id + code
                number = number / 2
            else:
                code = "\nINC "+id + code
                number = number - 1
        
        return code, lines


    def multiplication(arg, free):
        return  "\nINC "+free[0]+\
                "\nSHL "+free[0]+\
                "\nSHL "+arg[0]+\
                "\nADD "+free[2] +" "+ free[0]+\
                "\nSUB "+free[2] +" "+ arg[1]+\
                "\nJZERO "+free[2]+" -4"+\
                "\nRESET "+free[2]+\
                "\nSHR "+free[0]+\
                "\nSHR "+arg[0]+\
                "\nINC "+free[2]+\
                "\nADD "+free[2] +" "+ arg[1]+\
                "\nSUB "+free[2] +" "+ free[0]+\
                "\nJZERO "+free[2]+" 4"+\
                "\nRESET "+free[2]+\
                "\nADD "+free[1]+" "+arg[0]+\
                "\nSUB "+arg[1]+" "+free[0]+\
                "\nSHR "+free[0]+\
                "\nSHR "+arg[0]+\
                "\nJZERO "+arg[1]+" 2"+\
                "\nJUMP -10", free[1], 20

    def division(arg, free):
        return  "\nJZERO "+arg[1]+" 21"+\
                "\nSHL "+arg[1]+\
                "\nINC "+free[0]+\
                "\nADD "+free[2] +" "+ arg[1]+\
                "\nSUB "+free[2] +" "+ arg[0]+\
                "\nJZERO "+free[2]+" -4"+\
                "\nRESET "+free[2]+\
                "\nSHR "+arg[1]+\
                "\nSHL "+free[1]+\
                "\nDEC "+free[0]+\
                "\nJZERO "+arg[1]+" 8"+\
                "\nINC "+free[2]+\
                "\nADD "+free[2] +" "+ arg[0]+\
                "\nSUB "+free[2] +" "+ arg[1]+\
                "\nJZERO "+free[2]+" 4"+\
                "\nRESET "+free[2]+\
                "\nINC "+free[1]+\
                "\nSUB "+arg[0]+" "+arg[1]+\
                "\nSHR "+arg[1]+\
                "\nJZERO "+free[0]+" 2"+\
                "\nJUMP -12", free[1], 21
    
    def modulo(arg, free):
        return  "\nJZERO "+arg[1]+" 18"+\
                "\nSHL "+arg[1]+\
                "\nINC "+free[0]+\
                "\nADD "+free[1] +" "+ arg[1]+\
                "\nSUB "+free[1] +" "+ arg[0]+\
                "\nJZERO "+free[1]+" -4"+\
                "\nRESET "+free[1]+\
                "\nSHR "+arg[1]+\
                "\nDEC "+free[0]+\
                "\nINC "+free[1]+\
                "\nADD "+free[1] +" "+ arg[0]+\
                "\nSUB "+free[1] +" "+ arg[1]+\
                "\nJZERO "+free[1]+" 3"+\
                "\nRESET "+free[1]+\
                "\nSUB "+arg[0]+" "+arg[1]+\
                "\nSHR "+arg[1]+\
                "\nJZERO "+free[0]+" 2"+\
                "\nJUMP -9", arg[0], 18


# a=4,b=2,c=0
# while b <= a
#     shl b
#     inc c

# shr b
# while c > 0
#     dec c
#     if b<=a
#         sub a b
#     shr b

# return a