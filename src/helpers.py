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
        return  "\nJODD "+args[1]+" 2"+\
                "\nJUMP 3"+\
                "\nADD "+free+" "+args[0]+\
                "\nDEC "+args[1]+\
                "\nJZERO "+args[1]+" 8"+\
                "\nSHR "+args[1]+\
                "\nSHL "+args[0]+\
                "\nJODD "+args[1]+" 2"+\
                "\nJUMP 3"+\
                "\nADD "+free+" "+args[0]+\
                "\nDEC "+args[1]+\
                "\nJUMP -7", free, 12

    def division(arg, free):
        return  "\nJZERO "+arg[1]+" 20"+\
                "\nSHL "+arg[1]+\
                "\nINC "+free[0]+\
                "\nADD "+free[2] +" "+ arg[1]+\
                "\nSUB "+free[2] +" "+ arg[0]+\
                "\nJZERO "+free[2]+" -4"+\
                "\nRESET "+free[2]+\
                "\nSHR "+arg[1]+\
                "\nSHL "+free[1]+\
                "\nDEC "+free[0]+\
                "\nINC "+free[2]+\
                "\nADD "+free[2] +" "+ arg[0]+\
                "\nSUB "+free[2] +" "+ arg[1]+\
                "\nJZERO "+free[2]+" 4"+\
                "\nRESET "+free[2]+\
                "\nINC "+free[1]+\
                "\nSUB "+arg[0]+" "+arg[1]+\
                "\nSHR "+arg[1]+\
                "\nJZERO "+free[0]+" 2"+\
                "\nJUMP -11", free[1], 20

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