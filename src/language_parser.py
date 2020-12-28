from sly import Parser
from language_lexer import LanguageLexer
from variables_manager import VariablesManager

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

# a=4,b=2,c=0, d=0
# while b <= a
#     shl b
#     inc c

# shr b
# while c > 0
#     shl d
#     dec c
#     if b<=a
#         inc d
#         sub a b
#         shr b

# return d


class LanguageParser(Parser):
    tokens = LanguageLexer.tokens


    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        print("HALT")
    
    @_('declarations COMMA ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)
        return p.declarations
    
    @_('COMMA ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)

    @_('declarations COMMA ID')
    def declarations(self, p):
        VariablesManager.declare_variable(p.ID)
        return p.declarations

    @_('ID')
    def declarations(self, p):
        VariablesManager.declare_variable(p.ID)

    @_('ID')
    def variable(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        
        generate_number(VariablesManager.get_location(p.ID), reg1)
        print("LOAD "+reg2+" " +reg1)
        VariablesManager.add_register(reg1)
        return reg2

    @_('ID')
    def variable_reference(self, p):
        reg = VariablesManager.get_register()
        generate_number(VariablesManager.get_location(p.ID), reg)
        return reg

    @_('variable')
    def value(self, p):
        return p.variable

    @_('NUMBER')
    def value(self, p):
        reg = VariablesManager.get_register()
        
        generate_number(p.NUMBER, reg)
        return reg
    
    @_('ID LEFT NUMBER RIGHT')
    def variable(self, p):
        return VariablesManager.get_table_location(p.ID, p.NUMBER)

    @_('ID LEFT variable RIGHT')
    def variable(self, p):
        start_location, start_index = VariablesManager.get_table_data(p.ID)
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        print("ADD "+reg+" "+p.variable)
        generate_number(start_index, reg1)
        print("SUB "+reg+" "+reg1)
        generate_number(start_location, reg1)
        print("ADD "+reg+" "+reg1)
        print("STORE "+p.variable+" "+reg)

    # @_('ID LEFT LOCATION RIGHT')
    # def special_location(self, p):
    #     # jestem w dupie
    #     VariablesManager.declare_variable(p.ID)

    @_('commands command')
    def commands(self, p):
        return p.commands

    @_('command')
    def commands(self, p):
        pass

    @_('ID ASSIGN value')
    def command(self, p):
        reg = VariablesManager.get_register()
        generate_number(VariablesManager.get_location(p.ID), reg)
        print("STORE "+p.value+" "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(p.value)

    # @_('ID ASSIGN location')
    # def command(self, p):
    #     generate_number(p.location, "a")
    #     print("LOAD b a")
    #     generate_number(VariablesManager.get_location(p.ID), "a")
    #     print("STORE b a")
    
    @_('ID ASSIGN value PLUS value')
    def command(self, p):
        print("ADD "+p.value0+" "+p.value1)
        reg = VariablesManager.get_register()
        generate_number(VariablesManager.get_location(p.ID), reg)
        print("STORE "+p.value0+" "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)

    @_('ID ASSIGN value MINUS value')
    def command(self, p):
        reg = VariablesManager.get_register()
        generate_number(VariablesManager.get_location(p.ID), reg)
        print("SUB "+p.value0+" "+p.value1)
        print("STORE "+p.value0+" "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)
    
    @_('ID ASSIGN value MULTI value')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()
        result_register = multiplication([p.value0, p.value1],[reg1, reg2, reg3])
        reg = reg1
        if reg == result_register:
            reg = reg2
        generate_number(VariablesManager.get_location(p.ID), reg)
        print("STORE "+result_register+" "+reg)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(reg3)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)




        # generate_number(VariablesManager.get_location(p.ID1), "a")
        # print("LOAD b a")
        # generate_number(VariablesManager.get_location(p.ID2), "c")
        # print("LOAD d c")
        # result_register = multiplication(['b', 'd'],['a', 'c', 'e'])
        # generate_number(VariablesManager.get_location(p.ID0), "a")
        # print("STORE "+result_register+" a")
    
    @_('ID ASSIGN value DIV value')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()
        result_register = division([p.value0, p.value1],[reg1, reg2, reg3])
        reg = reg1
        if reg == result_register:
            reg = reg2
        generate_number(VariablesManager.get_location(p.ID), reg)
        print("STORE "+result_register+" "+reg)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(reg3)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)


    # @_('ID')
    # def expression(self, p):
    #     generate_number(VariablesManager.get_location(p.ID), "a")
    #     generate_number(p.NUMBER, "b")
    #     print("STORE a b")
    
    @_('READ variable_reference')
    def command(self, p):
        print("GET "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)

    @_('WRITE NUMBER')
    def command(self, p):
        reg = VariablesManager.get_register()
        generate_number(p.NUMBER, reg)
        print("PUT "+reg)
        VariablesManager.add_register(reg)
    
    @_('WRITE variable')
    def command(self, p):
        reg = VariablesManager.get_register()
        temp_location = VariablesManager.get_temp_location()
        generate_number(temp_location, reg)
        print("STORE "+p.variable+" "+reg)
        print("PUT "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(p.variable)