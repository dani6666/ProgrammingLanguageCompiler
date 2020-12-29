class Helpers:
    def generate_number(number, id):
        print("RESET "+id)
        if number == 0:
            return

        val = 1
        print("INC "+id)
        while val*2<=number:
            print("SHL "+id)
            val *= 2

        while val<number:
            print("INC "+id)
            val *= 2


    def multiplication(arg_registers, free_registers):
        print("RESET "+free_registers[0])
        print("RESET "+free_registers[1])
        print("RESET "+free_registers[2])

        print("INC "+free_registers[0])

        print("SHL "+free_registers[0])
        print("SHL "+arg_registers[0])

        print("ADD "+free_registers[2] +" "+ free_registers[0])
        print("SUB "+free_registers[2] +" "+ arg_registers[1])
        print("JZERO "+free_registers[2]+" -4")
        print("RESET "+free_registers[2])

        print("SHR "+free_registers[0])
        print("SHR "+arg_registers[0])

        print("INC "+free_registers[2])
        print("ADD "+free_registers[2] +" "+ arg_registers[1])
        print("SUB "+free_registers[2] +" "+ free_registers[0])
        
        print("JZERO "+free_registers[2]+" 4")
        print("RESET "+free_registers[2])
        print("ADD "+free_registers[1]+" "+arg_registers[0])
        print("SUB "+arg_registers[1]+" "+free_registers[0])

        print("SHR "+free_registers[0])
        print("SHR "+arg_registers[0])

        print("JZERO "+arg_registers[1]+" 2")
        print("JUMP -10")

        return free_registers[1]


    def division(arg_registers, free_registers):
        print("RESET "+free_registers[0])
        print("RESET "+free_registers[1])
        print("RESET "+free_registers[2])
        print("JZERO "+arg_registers[1]+" 21")

        print("SHL "+arg_registers[1])
        print("INC "+free_registers[0])

        print("ADD "+free_registers[2] +" "+ arg_registers[1])
        print("SUB "+free_registers[2] +" "+ arg_registers[0])
        print("JZERO "+free_registers[2]+" -4")
        print("RESET "+free_registers[2])

        print("SHR "+arg_registers[1])

        print("SHL "+free_registers[1])
        print("DEC "+free_registers[0])
        
        print("JZERO "+arg_registers[1]+" 8")
        print("INC "+free_registers[2])
        print("ADD "+free_registers[2] +" "+ arg_registers[0])
        print("SUB "+free_registers[2] +" "+ arg_registers[1])
        print("JZERO "+free_registers[2]+" 4")
        print("RESET "+free_registers[2])
        
        print("INC "+free_registers[1])
        print("SUB "+arg_registers[0]+" "+arg_registers[1])

        print("SHR "+arg_registers[1])

        print("JZERO "+free_registers[0]+" 2")
        print("JUMP -12")

        return free_registers[1]
    
    def modulo(arg_registers, free_registers):
        print("RESET "+free_registers[0])
        print("RESET "+free_registers[1])
        print("JZERO "+arg_registers[1]+" 21")

        print("SHL "+arg_registers[1])
        print("INC "+free_registers[0])

        print("ADD "+free_registers[1] +" "+ arg_registers[1])
        print("SUB "+free_registers[1] +" "+ arg_registers[0])
        print("JZERO "+free_registers[1]+" -4")
        print("RESET "+free_registers[1])

        print("SHR "+arg_registers[1])

        print("DEC "+free_registers[0])
        
        print("INC "+free_registers[1])
        print("ADD "+free_registers[1] +" "+ arg_registers[0])
        print("SUB "+free_registers[1] +" "+ arg_registers[1])
        print("JZERO "+free_registers[1]+" 3")
        print("RESET "+free_registers[1])
        
        print("SUB "+arg_registers[0]+" "+arg_registers[1])
        print("SHR "+arg_registers[1])

        print("JZERO "+free_registers[0]+" 2")
        print("JUMP -9")

        return arg_registers[0]


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