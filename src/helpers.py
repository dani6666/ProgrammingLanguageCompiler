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
                number = number // 2
            else:
                code = "\nINC "+id + code
                number = number - 1
        
        return code, lines

    def multiplication(args, free):
        return  "\nJZERO "+args[1]+" 8"+\
                "\nJODD "+args[1]+" 2"+\
                "\nJUMP 3"+\
                "\nADD "+free+" "+args[0]+\
                "\nDEC "+args[1]+\
                "\nSHR "+args[1]+\
                "\nSHL "+args[0]+\
                "\nJUMP -7", free, 8

    # a b    c d e
    # c = 1
    # do
    #   SHL a
    #   SHL c
    # while c <= b
    # SHR a
    # SHR c
    # do
    #   if b <= c
    #       ADD d a
    #       SUB b c
    #   SHR c
    #   SHR a
    # while b > 0;
    #
    # return d

    # int a=4, b=2, c=0, d=0, e=0;
    # c = 1;
    # do
    #   a *= 2
    #   c *= 2
    # while c <= b;
    # a /=2
    # c /=2
    # do
    #   if (b <= c)
    #       d += a
    #       b -= c
    #   c /= 2
    #   a /= 2
    # while b > 0;
    
    # return d

    # "\nJODD "+arg[1]+" 4"+\
                # "\nSHR "+arg[0]+\
                # "\nSHR "+arg[1]+\
                # "\nJUMP -3"+\
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
    # int a=4, b=2, c=0, d=0, e=0;
    # if b == 0
    #     return 0
    # do
    #   b *= 2
    #   c += 1
    # while b <= a;
    # b /=2
    # do
    #   d *= 2
    #   c -= 1
    #   if (b > 0)
    #       if (a >= b)
    #         d += 1
    #         a -= b
    #   b /= 2
    # while c > 0;
    
    # return d
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
                "\nJZERO "+free[0]+" 3"+\
                "\nJUMP -9"+\
                "\nRESET "+arg[0], arg[0], 19

    def check_for_power_of_two(number):
        power_result = 2
        power = 1
        while power_result < number:
            power_result = power_result * 2
            power = power + 1
        
        if power_result == number:
            return power
        
        return 0

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