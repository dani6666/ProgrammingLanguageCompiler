from sly import Parser
from language_lexer import LanguageLexer
from variables_manager import VariablesManager
from flow_manager import FlowManager
from helpers import Helpers


class LanguageParser(Parser):
    tokens = LanguageLexer.tokens

    def error(self,t):
        if t is None:
            raise Exception("Line "+str(LanguageLexer.line_count)+": Unexpected end of file")

        raise Exception("Line "+str(LanguageLexer.line_count)+": Unexcpeted token " + str(t.value))

#region program_structure

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return p.commands[0][1:]+"\nHALT"
    
    @_('BEGIN commands END')
    def program(self, p):
        return p.commands[0][1:]+"\nHALT"
    
    @_('declarations COMMA ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)
        return p.declarations
    
    @_('declarations COMMA ID LEFT NUMBER RIGHT')
    def declarations(self, p):
        raise Exception("Line "+str(LanguageLexer.line_count)+": Incorrect table declaration")
    
    @_('ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)
    
    @_('ID LEFT NUMBER RIGHT')
    def declarations(self, p):
        raise Exception("Line "+str(LanguageLexer.line_count)+": Incorrect table declaration")

    @_('declarations COMMA ID')
    def declarations(self, p):
        VariablesManager.declare_variable(p.ID)
        return p.declarations

    @_('ID')
    def declarations(self, p):
        VariablesManager.declare_variable(p.ID)
    
    @_('commands command')
    def commands(self, p):
        all_code, all_lines = p.commands
        add_code, add_lines = p.command
        return all_code + add_code, all_lines + add_lines

    @_('command')
    def commands(self, p):
        return p.command

#endregion

#region variable(_reference)
    @_('ID LEFT NUMBER RIGHT')
    def variable(self, p):
        reg = VariablesManager.get_register()

        gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)

        return reg, \
                "\nRESET "+reg+\
                gen_code+\
                "\nLOAD "+reg+" "+reg,\
                gen_lines+2

    @_('ID LEFT ID RIGHT')
    def variable(self, p):
        var_location = VariablesManager.get_location(p.ID1)
        VariablesManager.check_initialization(p.ID1)

        reg0 = VariablesManager.get_register()

        if FlowManager.check_for_constant(p.ID1):
            gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID0, FlowManager.get_constant_value(p.ID1)), reg0)

            return reg0, \
                    "\nRESET "+reg0+\
                    gen_code+\
                    "\nLOAD "+reg0+" "+reg0,\
                    gen_lines+2

        start_location, start_index = VariablesManager.get_table_data(p.ID0)
        reg1 = VariablesManager.get_register()

        gen_code0, gen_lines0 = Helpers.generate_number(var_location, reg1)
        gen_code1, gen_lines1 = Helpers.generate_number(start_index, reg1)
        gen_code2, gen_lines2 = Helpers.generate_number(start_location, reg1)

        VariablesManager.add_register(reg1)

        return reg0, \
            "\nRESET "+reg1+\
            gen_code0+\
            "\nLOAD "+reg0+" " +reg1+\
            "\nRESET "+reg1+\
            gen_code1+\
            "\nSUB "+reg0+" "+reg1+\
            "\nRESET "+reg1+\
            gen_code2+\
            "\nADD "+reg0+" "+reg1+\
            "\nLOAD "+reg0+" "+reg0,\
            gen_lines0 + gen_lines1 + gen_lines2 + 7

    @_('ID')
    def variable(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_initialization(p.ID)

        reg = VariablesManager.get_register()
        
        gen_code, gen_lines = Helpers.generate_number(var_location, reg)

        return reg,\
            "\nRESET "+reg+\
            gen_code+\
            "\nLOAD "+reg+" " +reg,\
            gen_lines + 2

    @_('ID LEFT NUMBER RIGHT')
    def variable_reference(self, p):
        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1, None

    @_('ID LEFT ID RIGHT')
    def variable_reference(self, p):
        start_location, start_index = VariablesManager.get_table_data(p.ID0)
        VariablesManager.check_initialization(p.ID1)
        reg = VariablesManager.get_register()

        if FlowManager.check_for_constant(p.ID1):
            gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID0, FlowManager.get_constant_value(p.ID1)), reg)

            return reg, "\nRESET "+reg + gen_code, gen_lines+1, None

        reg1 = VariablesManager.get_register()

        gen_code0, gen_lines0 = Helpers.generate_number(VariablesManager.get_location(p.ID1), reg1)
        gen_code1, gen_lines1 = Helpers.generate_number(start_location, reg1)
        gen_code2, gen_lines2 = Helpers.generate_number(start_index, reg1)


        VariablesManager.add_register(reg1)

        return reg,\
            "\nRESET "+reg1+\
            gen_code0+\
            "\nLOAD "+reg+" " +reg1+\
            "\nRESET "+reg1+\
            gen_code1+\
            "\nADD "+reg+" "+reg1+\
            "\nRESET "+reg1+\
            gen_code2+\
            "\nSUB "+reg+" "+reg1,\
            gen_lines0 + gen_lines1 + gen_lines2 + 6, None

    @_('ID')
    def variable_reference(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_for_iterator(p.ID)
        VariablesManager.initialize_variable(p.ID)

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(var_location, reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1, p.ID
    
    @_('ID')
    def write_variable_reference(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_initialization(p.ID)

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(var_location, reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1
    
    @_('ID LEFT NUMBER RIGHT')
    def write_variable_reference(self, p):
        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1

    @_('ID LEFT ID RIGHT')
    def write_variable_reference(self, p):
        start_location, start_index = VariablesManager.get_table_data(p.ID0)
        VariablesManager.check_initialization(p.ID1)
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()

        gen_code0, gen_lines0 = Helpers.generate_number(VariablesManager.get_location(p.ID1), reg1)
        gen_code1, gen_lines1 = Helpers.generate_number(start_location, reg1)
        gen_code2, gen_lines2 = Helpers.generate_number(start_index, reg1)

        VariablesManager.add_register(reg1)

        return reg,\
            "\nRESET "+reg1+\
            gen_code0+\
            "\nLOAD "+reg+" " +reg1+\
            "\nRESET "+reg1+\
            gen_code1+\
            "\nADD "+reg+" "+reg1+\
            "\nRESET "+reg1+\
            gen_code2+\
            "\nSUB "+reg+" "+reg1,\
            gen_lines0 + gen_lines1 + gen_lines2 + 6

#endregion

#region value
    @_('ID LEFT NUMBER RIGHT')
    def value(self, p):
        reg = VariablesManager.get_register()

        gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)

        return False, reg, \
                "\nRESET "+reg+\
                gen_code+\
                "\nLOAD "+reg+" "+reg,\
                gen_lines+2

    @_('ID LEFT ID RIGHT')
    def value(self, p):
        var_location = VariablesManager.get_location(p.ID1)
        VariablesManager.check_initialization(p.ID1)

        start_location, start_index = VariablesManager.get_table_data(p.ID0)
        reg0 = VariablesManager.get_register()

        if FlowManager.check_for_constant(p.ID1):
            gen_code, gen_lines = Helpers.generate_number(
                VariablesManager.get_table_location(p.ID0, FlowManager.get_constant_value(p.ID1)), reg0)

            return False, reg0, \
                "\nRESET "+reg0+\
                gen_code+\
                "\nLOAD "+reg0+" "+reg0,\
                gen_lines+2

        reg1 = VariablesManager.get_register()

        gen_code0, gen_lines0 = Helpers.generate_number(var_location, reg1)
        gen_code1, gen_lines1 = Helpers.generate_number(start_index, reg1)
        gen_code2, gen_lines2 = Helpers.generate_number(start_location, reg1)

        VariablesManager.add_register(reg1)
        # to do
        return False, reg0, \
            "\nRESET "+reg1+\
            gen_code0+\
            "\nLOAD "+reg0+" " +reg1+\
            "\nRESET "+reg1+\
            "\nRESET "+reg1+\
            gen_code1+\
            "\nSUB "+reg0+" "+reg1+\
            "\nRESET "+reg1+\
            gen_code2+\
            "\nADD "+reg0+" "+reg1+\
            "\nLOAD "+reg0+" "+reg0,\
            gen_lines0 + gen_lines1 + gen_lines2 + 8

    @_('ID')
    def value(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_initialization(p.ID)

        reg = VariablesManager.get_register()

        if FlowManager.check_for_constant(p.ID):
            VariablesManager.add_register(reg)
            return True, FlowManager.get_constant_value(p.ID)

        gen_code, gen_lines = Helpers.generate_number(var_location, reg)

        return False, reg,\
            "\nRESET "+reg+\
            gen_code+\
            "\nLOAD "+reg+" " +reg,\
            gen_lines + 2
    
    @_('NUMBER')
    def value(self, p):
        return True , p.NUMBER

#endregion

#region IO    
    @_('READ variable_reference SEMICOLON')
    def command(self, p):
        reg, code, lines, name = p.variable_reference
        if name is not None:
            FlowManager.drop_constant_variable(name)
        VariablesManager.add_register(reg)
        return code+"\nGET "+reg, lines+1


    @_('WRITE NUMBER SEMICOLON')
    def command(self, p):
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        temp_location = VariablesManager.get_temp_location()
        gen_code1, gen_lines1 = Helpers.generate_number(temp_location, reg)
        gen_code2, gen_lines2 = Helpers.generate_number(p.NUMBER, reg1)

        VariablesManager.add_register(reg)
        VariablesManager.add_register(reg1)

        return  "\nRESET " +reg+\
                "\nRESET " +reg1+\
                gen_code1+\
                gen_code2+\
                "\nSTORE "+reg1+" "+reg+\
                "\nPUT "+reg,\
                gen_lines1 + gen_lines2 + 4
    
    @_('WRITE write_variable_reference SEMICOLON')
    def command(self, p):
        ref_reg, ref_code, ref_lines = p.write_variable_reference

        VariablesManager.add_register(ref_reg)

        return  ref_code+\
                "\nPUT "+ref_reg,\
                ref_lines + 1
#endregion

#region expression
    @_('value')
    def expression(self, p):
        return p.value

    @_('value PLUS value')
    def expression(self, p):
        if p.value0[0] and p.value1[0]:
            return True, p.value0[1] + p.value1[1]

        if p.value0[0]:
            return LanguageParser.plus_with_const(p.value1[1:4], p.value0[1])

        if p.value1[0]:
            return LanguageParser.plus_with_const(p.value0[1:4], p.value1[1])

        var_reg0, var_code0, var_lines0 = p.value0[1:4]
        var_reg1, var_code1, var_lines1 = p.value1[1:4]

        VariablesManager.add_register(var_reg1)

        return  False, var_reg0,\
                var_code0+\
                var_code1+\
                "\nADD "+var_reg0+" "+var_reg1,\
                var_lines0 + var_lines1 + 1

    def plus_with_const(variable, const):
        var_reg, var_code, var_lines = variable
        if const == 0:
            return False, var_reg, var_code, var_lines
        elif const == 1:
            return False, var_reg, var_code+"\nINC "+var_reg, var_lines+1
        elif const == 2:
            return False, var_reg, var_code+"\nINC "+var_reg+"\nINC "+var_reg, var_lines+2

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, reg)

        VariablesManager.add_register(reg)

        return  False, var_reg,\
                var_code+\
                "\nRESET "+reg+\
                gen_code+\
                "\nADD "+var_reg+" "+reg,\
                var_lines + gen_lines + 2

    @_('value MINUS value')
    def expression(self, p):
        if p.value0[0] and p.value1[0]:
            return True, max(p.value0[1] - p.value1[1], 0)

        if p.value0[0]:
            return LanguageParser.minus_with_left_const(p.value1[1:4], p.value0[1])

        if p.value1[0]:
            return LanguageParser.minus_with_right_const(p.value0[1:4], p.value1[1])

        var_reg0, var_code0, var_lines0 = p.value0[1:4]
        var_reg1, var_code1, var_lines1 = p.value1[1:4]

        VariablesManager.add_register(var_reg1)

        return  False, var_reg0,\
                var_code0+\
                var_code1+\
                "\nSUB "+var_reg0+" "+var_reg1,\
                var_lines0 + var_lines1 + 1

    def minus_with_right_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0:
            return False, var_reg, var_code, var_lines
        elif const == 1:
            return False, var_reg, var_code+"\nDEC "+var_reg, var_lines+1
        elif const == 2:
            return False, var_reg, var_code+"\nDEC "+var_reg+"\nDEC "+var_reg, var_lines+2

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, reg)

        VariablesManager.add_register(reg)

        return  False, var_reg,\
                var_code+\
                "\nRESET "+reg+\
                gen_code+\
                "\nSUB "+var_reg+" "+reg,\
                var_lines + gen_lines + 2
    
    def minus_with_left_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0:
            VariablesManager.add_register(var_reg)
            return True, 0

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, reg)

        VariablesManager.add_register(var_reg)

        return  False, reg,\
                var_code+\
                "\nRESET "+reg+\
                gen_code+\
                "\nSUB "+reg+" "+var_reg,\
                var_lines + gen_lines + 2
    

    @_('value MULTI value')
    def expression(self, p):
        if p.value0[0] and p.value1[0]:
            return True, p.value0[1] * p.value1[1]

        if p.value0[0]:
            return LanguageParser.multi_with_const(p.value1[1:4], p.value0[1])

        if p.value1[0]:
            return LanguageParser.multi_with_const(p.value0[1:4], p.value1[1])

        reg1 = VariablesManager.get_register()

        var_reg0, var_code0, var_lines0 = p.value0[1:4]
        var_reg1, var_code1, var_lines1 = p.value1[1:4]

        multi_code, result_register, multi_lines = \
            Helpers.multiplication([var_reg0, var_reg1], reg1)

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if var_reg0 != result_register:
            VariablesManager.add_register(var_reg0)
        if var_reg1 != result_register:
            VariablesManager.add_register(var_reg1)

        return  False, result_register,\
                var_code0+\
                var_code1+\
                "\nRESET "+reg1+\
                multi_code,\
                var_lines0 + var_lines1 + multi_lines + 1

    
    def multi_with_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0:
            VariablesManager.add_register(var_reg)
            return True, 0
        
        if const == 1:
            return False, var_reg, var_code, var_lines

        number_power = Helpers.check_for_power_of_two(const)
        if number_power > 0:
            return False, var_reg, var_code+("\nSHL "+var_reg)*number_power, var_lines+number_power

        reg1 = VariablesManager.get_register()

        result_code = var_code+"\nRESET "+reg1
        result_lines = var_lines+ 1
        while const > 0:
            if const % 2 == 1:
                result_code=result_code+"\nADD "+reg1 + " "+var_reg
                result_lines+=1
                const -= 1
            const = const // 2
            result_code =result_code+ "\nSHL "+var_reg
            result_lines+=1

        VariablesManager.add_register(var_reg)
        return False, reg1, result_code, result_lines
    
    @_('value DIV value')
    def expression(self, p):
        if p.value0[0] and p.value1[0]:
            if p.value1[1] == 0:
                return True, 0
            return True, p.value0[1] // p.value1[1]

        if p.value0[0]:
            return LanguageParser.div_with_left_const(p.value1[1:4], p.value0[1])

        if p.value1[0]:
            return LanguageParser.div_with_right_const(p.value0[1:4], p.value1[1])

        var_reg0, var_code0, var_lines0 = p.value0[1:4]
        var_reg1, var_code1, var_lines1 = p.value1[1:4]

        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()

        div_code, result_register, div_lines = \
            Helpers.division([var_reg0, var_reg1],[reg1, reg2, reg3])

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if reg2 != result_register:
            VariablesManager.add_register(reg2)
        if reg3 != result_register:
            VariablesManager.add_register(reg3)
        if var_reg0 != result_register:
            VariablesManager.add_register(var_reg0)
        if var_reg1 != result_register:
            VariablesManager.add_register(var_reg1)

        return  False, result_register,\
                var_code0+\
                var_code1+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                "\nRESET "+reg3+\
                div_code,\
                var_lines0 + var_lines1 + div_lines + 3

    def div_with_right_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0:
            VariablesManager.add_register(var_reg)
            return True, 0
        
        if const == 1:
            return False, var_reg, var_code, var_lines

        number_power = Helpers.check_for_power_of_two(const)
        if number_power > 0:
            return False, var_reg, var_code+("\nSHR "+var_reg)*number_power, var_lines+number_power

        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, num_reg)

        div_code, result_register, div_lines = \
            Helpers.division([var_reg, num_reg],[reg1, reg2, reg3])

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if reg2 != result_register:
            VariablesManager.add_register(reg2)
        if reg3 != result_register:
            VariablesManager.add_register(reg3)
        if var_reg != result_register:
            VariablesManager.add_register(var_reg)
        if num_reg != result_register:
            VariablesManager.add_register(num_reg)

        return  False, result_register,\
                var_code+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                "\nRESET "+reg3+\
                div_code,\
                var_lines + gen_lines + div_lines + 4
    
    def div_with_left_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0:
            VariablesManager.add_register(var_reg)
            return True, 0
        
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, num_reg)

        div_code, result_register, div_lines = \
            Helpers.division([num_reg, var_reg],[reg1, reg2, reg3])

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if reg2 != result_register:
            VariablesManager.add_register(reg2)
        if reg3 != result_register:
            VariablesManager.add_register(reg3)
        if num_reg != result_register:
            VariablesManager.add_register(num_reg)
        if var_reg != result_register:
            VariablesManager.add_register(var_reg)

        return  False, result_register,\
                var_code+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                "\nRESET "+reg3+\
                div_code,\
                var_lines + gen_lines + div_lines + 4
    
    @_('value MOD value')
    def expression(self, p):
        if p.value0[0] and p.value1[0]:
            if p.value1[1] == 0:
                return True, 0
            return True, p.value0[1] % p.value1[1]

        if p.value0[0]:
            return LanguageParser.mod_with_left_const(p.value1[1:4], p.value0[1])

        if p.value1[0]:
            return LanguageParser.mod_with_right_const(p.value0[1:4], p.value1[1])

        var_reg0, var_code0, var_lines0 = p.value0[1:4]
        var_reg1, var_code1, var_lines1 = p.value1[1:4]

        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()

        mod_code, result_register, mod_lines = \
            Helpers.modulo([var_reg0, var_reg1],[reg1, reg2])

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if reg2 != result_register:
            VariablesManager.add_register(reg2)
        if var_reg0 != result_register:
            VariablesManager.add_register(var_reg0)
        if var_reg1 != result_register:
            VariablesManager.add_register(var_reg1)

        return  False, result_register,\
                var_code0+\
                var_code1+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                mod_code,\
                var_lines0 + var_lines1 + mod_lines + 2

    def mod_with_right_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0 or const == 1:
            VariablesManager.add_register(var_reg)
            return True, 0
        
        reg1 = VariablesManager.get_register()

        if const == 2:
            VariablesManager.add_register(var_reg)

            return  False, reg1,\
                    var_code+\
                    "\nRESET "+reg1+\
                    "JODD "+var_reg+" 2"+\
                    "JUMP 2"+\
                    "INC "+reg1,\
                    var_lines + 4

        reg2 = VariablesManager.get_register()
        
        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, num_reg)

        multi_code, result_register, multi_lines = \
            Helpers.modulo([var_reg, num_reg],[reg1, reg2])

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if reg2 != result_register:
            VariablesManager.add_register(reg2)
        if var_reg != result_register:
            VariablesManager.add_register(var_reg)
        if num_reg != result_register:
            VariablesManager.add_register(num_reg)

        return  False, result_register,\
                var_code+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                multi_code,\
                var_lines + gen_lines + multi_lines + 3
    
    def mod_with_left_const(variable, const):
        var_reg, var_code, var_lines = variable

        if const == 0:
            VariablesManager.add_register(var_reg)
            return True, 0

        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(const, num_reg)

        multi_code, result_register, multi_lines = \
            Helpers.modulo([num_reg, var_reg],[reg1, reg2])

        if reg1 != result_register:
            VariablesManager.add_register(reg1)
        if reg2 != result_register:
            VariablesManager.add_register(reg2)
        if num_reg != result_register:
            VariablesManager.add_register(num_reg)
        if var_reg != result_register:
            VariablesManager.add_register(var_reg)

        return  False, result_register,\
                var_code+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                multi_code,\
                var_lines + gen_lines + multi_lines + 3
    
#endregion

#region ASSIGNments
    @_('variable_reference ASSIGN expression SEMICOLON')
    def command(self, p):
        ref_reg, ref_code, ref_lines, var_name = p.variable_reference
        if p.expression[0]:
            if var_name is not None:
                FlowManager.set_constant_variable(var_name, p.expression[1])
            
            reg = VariablesManager.get_register()

            gen_code, gen_lines = Helpers.generate_number(p.expression[1], reg) 

            VariablesManager.add_register(ref_reg)
            VariablesManager.add_register(reg)

            return  ref_code+\
                "\nRESET "+reg+\
                gen_code+\
                "\nSTORE "+reg+" "+ref_reg,\
                ref_lines + gen_lines + 2

        if var_name is not None:
            FlowManager.drop_constant_variable(var_name)

        exp_reg, exp_code, exp_lines = p.expression[1:4]
        
        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(exp_reg)

        return  ref_code+\
                exp_code+\
                "\nSTORE "+exp_reg+" "+ref_reg,\
                ref_lines + exp_lines + 1
#endregion

#region condition

# jesli tru to przeskakuje nastepna instrukcje
    @_('variable EQUAL variable')
    def condition(self, p):
        reg = VariablesManager.get_register()

        var_reg0, var_code0, var_lines0 = p.variable0
        var_reg1, var_code1, var_lines1 = p.variable1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(var_reg0)
        VariablesManager.add_register(var_reg1)

        return  var_code0+\
                var_code1+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+var_reg0+\
                "\nSUB "+reg+" "+var_reg1+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 3"+\
                "\nSUB "+var_reg1+" "+var_reg0+\
                "\nJZERO "+var_reg1+" 2",\
                var_lines0 + var_lines1 + 7
    
    @_('variable EQUAL NUMBER')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2", var_lines0 + 1

        reg = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(reg)
        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+num_reg+\
                "\nSUB "+reg+" "+var_reg+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 3"+\
                "\nSUB "+var_reg+" "+num_reg+\
                "\nJZERO "+reg+" 2",\
                var_lines0 + gen_lines + 8
    
    @_('NUMBER EQUAL variable')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2", var_lines0 + 1

        reg = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(reg)
        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+var_reg+\
                "\nSUB "+reg+" "+num_reg+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 3"+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+reg+" 2",\
                var_lines0 + gen_lines + 8
    
    @_('NUMBER EQUAL NUMBER')
    def condition(self, p):
        if p.NUMBER0 == p.NUMBER1:
            return "\nJUMP 2", 1
        
        return "", 0

    @_('variable NOTEQUAL variable')
    def condition(self, p):
        reg = VariablesManager.get_register()

        var_reg0, var_code0, var_lines0 = p.variable0
        var_reg1, var_code1, var_lines1 = p.variable1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(var_reg0)
        VariablesManager.add_register(var_reg1)

        return  var_code0+\
                var_code1+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+var_reg0+\
                "\nSUB "+reg+" "+var_reg1+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 3"+\
                "\nSUB "+var_reg1+" "+var_reg0+\
                "\nJZERO "+var_reg1+" 2"+\
                "\nJUMP 2",\
                var_lines0 + var_lines1 + 8
    
    @_('variable NOTEQUAL NUMBER')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2"+"\nJUMP 2", var_lines0 + 2

        reg = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(reg)
        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+var_reg+\
                "\nSUB "+reg+" "+num_reg+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 3"+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+num_reg+" 2"+\
                "\nJUMP 2",\
                var_lines0 + gen_lines + 9
    
    @_('NUMBER NOTEQUAL variable')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2"+"\nJUMP 2", var_lines0 + 2

        reg = VariablesManager.get_register()

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(reg)
        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+var_reg+\
                "\nSUB "+reg+" "+num_reg+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 3"+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+num_reg+" 2"+\
                "\nJUMP 2",\
                var_lines0 + gen_lines + 9
    
    @_('NUMBER NOTEQUAL NUMBER')
    def condition(self, p):
        if p.NUMBER0 != p.NUMBER1:
            return "\nJUMP 2", 1
        
        return "", 0

    @_('variable LESSTHAN variable')
    def condition(self, p):

        var_reg0, var_code0, var_lines0 = p.variable0
        var_reg1, var_code1, var_lines1 = p.variable1

        VariablesManager.add_register(var_reg0)
        VariablesManager.add_register(var_reg1)

        return  var_code0+\
                var_code1+\
                "\nINC "+var_reg0+\
                "\nSUB "+var_reg0+" "+var_reg1+\
                "\nJZERO "+var_reg0+" 2",\
                var_lines0 + var_lines1 + 3
    
    @_('variable LESSTHAN NUMBER')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return "", 0
        
        if p.NUMBER == 1:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2", var_lines0 + 1

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nINC "+var_reg+\
                "\nSUB "+var_reg+" "+num_reg+\
                "\nJZERO "+var_reg+" 2",\
                var_lines0 + gen_lines + 4
    
    @_('NUMBER LESSTHAN variable')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2"+"\nJUMP 2", var_lines0 + 2

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER+1, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+num_reg+" 2",\
                var_lines0 + gen_lines + 3
    
    @_('NUMBER LESSTHAN NUMBER')
    def condition(self, p):
        if p.NUMBER0 < p.NUMBER1:
            return "\nJUMP 2", 1
        
        return "", 0

    @_('variable GREATERTHAN variable')
    def condition(self, p):

        var_reg0, var_code0, var_lines0 = p.variable0
        var_reg1, var_code1, var_lines1 = p.variable1

        VariablesManager.add_register(var_reg0)
        VariablesManager.add_register(var_reg1)

        return  var_code0+\
                var_code1+\
                "\nINC "+var_reg1+\
                "\nSUB "+var_reg1+" "+var_reg0+\
                "\nJZERO "+var_reg1+" 2",\
                var_lines0 + var_lines1 + 3
    
    @_('variable GREATERTHAN NUMBER')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2"+"\nJUMP 2", var_lines0 + 2
        
        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER+1, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+num_reg+" 2",\
                var_lines0 + gen_lines + 3
    
    @_('NUMBER GREATERTHAN variable')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return "", 0
        
        if p.NUMBER == 1:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2", var_lines0 + 1

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nINC "+var_reg+\
                "\nSUB "+var_reg+" "+num_reg+\
                "\nJZERO "+var_reg+" 2",\
                var_lines0 + gen_lines + 4
    
    @_('NUMBER GREATERTHAN NUMBER')
    def condition(self, p):
        if p.NUMBER0 > p.NUMBER1:
            return "\nJUMP 2", 1
        
        return "", 0

    
    @_('variable LESSEQUAL variable')
    def condition(self, p):

        var_reg0, var_code0, var_lines0 = p.variable0
        var_reg1, var_code1, var_lines1 = p.variable1

        VariablesManager.add_register(var_reg0)
        VariablesManager.add_register(var_reg1)

        return  var_code0+\
                var_code1+\
                "\nSUB "+var_reg0+" "+var_reg1+\
                "\nJZERO "+var_reg0+" 2",\
                var_lines0 + var_lines1 + 2
    
    @_('variable LESSEQUAL NUMBER')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2", var_lines0 + 1
        
        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nSUB "+var_reg+" "+num_reg+\
                "\nJZERO "+var_reg+" 2",\
                var_lines0 + gen_lines + 3
    
    @_('NUMBER LESSEQUAL variable')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return "\nJUMP 2", 1

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+num_reg+" 2",\
                var_lines0 + gen_lines + 3
    
    @_('NUMBER LESSEQUAL NUMBER')
    def condition(self, p):
        if p.NUMBER0 <= p.NUMBER1:
            return "\nJUMP 2", 1
        
        return "", 0
    
    @_('variable GREATEREQUAL variable')
    def condition(self, p):

        var_reg0, var_code0, var_lines0 = p.variable0
        var_reg1, var_code1, var_lines1 = p.variable1

        VariablesManager.add_register(var_reg0)
        VariablesManager.add_register(var_reg1)

        return  var_code0+\
                var_code1+\
                "\nSUB "+var_reg1+" "+var_reg0+\
                "\nJZERO "+var_reg1+" 2",\
                var_lines0 + var_lines1 + 2
    
    @_('variable GREATEREQUAL NUMBER')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return "\nJUMP 2", 1
        
        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nSUB "+num_reg+" "+var_reg+\
                "\nJZERO "+num_reg+" 2",\
                var_lines0 + gen_lines + 3
    
    @_('NUMBER GREATEREQUAL variable')
    def condition(self, p):
        var_reg, var_code0, var_lines0 = p.variable

        if p.NUMBER == 0:
            VariablesManager.add_register(var_reg)
            return var_code0+"\nJZERO "+ var_reg+" 2", var_lines0 + 1

        num_reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, num_reg)

        VariablesManager.add_register(var_reg)
        VariablesManager.add_register(num_reg)

        return  var_code0+\
                "\nRESET "+num_reg+\
                gen_code+\
                "\nSUB "+var_reg+" "+num_reg+\
                "\nJZERO "+var_reg+" 2",\
                var_lines0 + gen_lines + 3
    
    @_('NUMBER GREATEREQUAL NUMBER')
    def condition(self, p):
        if p.NUMBER0 >= p.NUMBER1:
            return "\nJUMP 2", 1
        
        return "", 0
#endregion

#region IF

    @_('IF')
    def if_start(self, p):
        FlowManager.ifs = FlowManager.ifs + 1

    @_('if_start condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        FlowManager.ifs = FlowManager.ifs - 1

        cond_code, cond_lines = p.condition
        com_code0, com_lines0 = p.commands0
        com_code1, com_lines1 = p.commands1
        return  cond_code+\
                "\nJUMP "+str(com_lines0+2)+\
                com_code0+\
                "\nJUMP "+str(com_lines1+1)+\
                com_code1,\
                cond_lines + com_lines0 + com_lines1 + 2

    @_('if_start condition THEN commands ENDIF')
    def command(self, p):
        FlowManager.ifs = FlowManager.ifs - 1

        cond_code, cond_lines = p.condition
        com_code, com_lines = p.commands
        return  cond_code+\
                "\nJUMP "+str(com_lines+1)+\
                com_code,\
                cond_lines + com_lines + 1
#endregion

#region WHILE_REPEAT
    @_('WHILE')
    def while_start(self, p):
        FlowManager.loops = FlowManager.loops + 1

    @_('while_start condition DO commands ENDWHILE')
    def command(self, p):
        FlowManager.loops = FlowManager.loops - 1

        cond_code, cond_lines = p.condition
        com_code, com_lines = p.commands
        return  cond_code+\
                "\nJUMP "+str(com_lines+2)+\
                com_code+\
                "\nJUMP -"+str(com_lines+cond_lines+1),\
                cond_lines + com_lines + 2

    @_('REPEAT')
    def repeat_start(self, p):
        FlowManager.repeat_loops = FlowManager.repeat_loops + 1

    @_('repeat_start commands UNTIL condition SEMICOLON')
    def command(self, p):
        FlowManager.repeat_loops = FlowManager.repeat_loops - 1

        cond_code, cond_lines = p.condition
        com_code, com_lines = p.commands
        return  com_code+\
                cond_code+\
                "\nJUMP -"+str(com_lines+cond_lines),\
                cond_lines + com_lines + 1
#endregion

#region FOR
    @_('ENDFOR')
    def end_of_for(self, p):
        return VariablesManager.undeclare_last_for()

    @_('FOR ID FROM value TO value')
    def for_asc_range(self, p):
        VariablesManager.initialize_variable(p.ID)
        for_location = VariablesManager.declare_for(p.ID)

        FlowManager.loops = FlowManager.loops + 1

        if p.value0[0] and p.value1[0]:
            return True, True, for_location, p.value0[1], p.value1[1]
        
        if p.value0[0]:
            return True, False, for_location, p.value0[1], p.value1[1:4] 

        if p.value1[0]:
            return False, True, for_location, p.value0[1:4], p.value1[1]

        reg0 = VariablesManager.get_register()

        gen_code, gen_lines = Helpers.generate_number(for_location, reg0)

        val_reg0, val_code0, val_lines0 = p.value0[1:4]
        val_reg1, val_code1, val_lines1 = p.value1[1:4]

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  False, False, for_location, val_code0+\
                val_code1+\
                "\nRESET "+reg0+\
                gen_code+\
                "\nSTORE "+val_reg0+" "+reg0+\
                "\nINC "+reg0+\
                "\nSTORE "+val_reg1+" "+reg0,\
                val_lines0 + val_lines1 + gen_lines + 4
    
    
    @_('FOR ID FROM value DOWNTO value')
    def for_desc_range(self, p):
        VariablesManager.initialize_variable(p.ID)
        for_location = VariablesManager.declare_for(p.ID)

        FlowManager.loops = FlowManager.loops + 1

        if p.value0[0] and p.value1[0]:
            return True, True, for_location, p.value0[1], p.value1[1]
        
        if p.value0[0]:
            return True, False, for_location, p.value0[1], p.value1[1:4] 

        if p.value1[0]:
            return False, True, for_location, p.value0[1:4], p.value1[1]

        reg0 = VariablesManager.get_register()

        gen_code, gen_lines = Helpers.generate_number(for_location, reg0)

        val_reg0, val_code0, val_lines0 = p.value0[1:4]
        val_reg1, val_code1, val_lines1 = p.value1[1:4]

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  False, False, for_location, val_code0+\
                val_code1+\
                "\nRESET "+reg0+\
                gen_code+\
                "\nSTORE "+val_reg0+" "+reg0+\
                "\nINC "+reg0+\
                "\nSTORE "+val_reg1+" "+reg0,\
                val_lines0 + val_lines1 + gen_lines + 4

    @_('for_asc_range DO commands end_of_for')
    def command(self, p):
        FlowManager.loops = FlowManager.loops - 1

        com_code, com_lines = p.commands

        reg0 = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()

        if p.for_asc_range[0] and p.for_asc_range[1]:
            for_location, value0, value1 = p.for_asc_range[2:5]

            gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
            gen_code1, gen_lines1 = Helpers.generate_number(value0, reg1)
            gen_code2, gen_lines2 = Helpers.generate_number(value1+1, reg0)

            VariablesManager.add_register(reg0)
            VariablesManager.add_register(reg1)

            if (value1 - value0) < FlowManager.max_iterations_to_expand_for:
                if not VariablesManager.check_for_used_iterator(p.end_of_for):
                    return com_code*(value1 - value0 + 1), com_lines*(value1 - value0 + 1)

                result_code = "\nRESET "+reg0+\
                                gen_code0+\
                                "\nRESET "+reg1+\
                                gen_code1+\
                                "\nSTORE "+ reg1 + " "+reg0
                result_lines = gen_lines0 + gen_lines1 + 3

                for i in range(value1 - value0):
                    result_code +=  com_code+\
                                    "\nRESET "+reg0+\
                                    gen_code0+\
                                    "\nLOAD "+reg1+" "+reg0+\
                                    "\nINC "+reg1+\
                                    "\nSTORE "+reg1+" "+reg0
                    result_lines += com_lines + gen_lines0 + 4
                
                if value1 - value0 >= 0:
                    result_code += com_code
                    result_lines += com_lines
                
                return result_code, result_lines

            return  "\nRESET "+reg0+\
                    gen_code0+\
                    "\nRESET "+reg1+\
                    gen_code1+\
                    "\nSTORE "+ reg1 + " "+reg0+\
                    "\nRESET "+reg0+\
                    gen_code2+\
                    "\nSUB "+reg0+" "+reg1+\
                    "\nJZERO "+reg0+" "+str(com_lines+gen_lines0+6)+\
                    com_code+\
                    "\nRESET "+reg0+\
                    gen_code0+\
                    "\nLOAD "+reg1+" "+reg0+\
                    "\nINC "+reg1+\
                    "\nSTORE "+reg1+" "+reg0+\
                    "\nJUMP -"+str(gen_lines0+gen_lines2+ com_lines+7),\
                    gen_lines0 * 2 + gen_lines1 + gen_lines2 + com_lines + 11
                    
        if p.for_asc_range[0]:
            for_location, value0, variable = p.for_asc_range[2:5]

            var_reg, var_code, var_lines = variable

            gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
            gen_code1, gen_lines1 = Helpers.generate_number(value0, reg1)

            VariablesManager.add_register(reg0)
            VariablesManager.add_register(reg1)
            VariablesManager.add_register(var_reg)

            return  "\nRESET "+reg0+\
                    gen_code0+\
                    "\nRESET "+reg1+\
                    gen_code1+\
                    "\nSTORE "+ reg1 + " "+reg0+\
                    "\nINC "+reg0+\
                    var_code+\
                    "\nINC "+var_reg+\
                    "\nSTORE "+ var_reg + " "+reg0+\
                    "\nJUMP "+str(3)+\
                    "\nINC "+reg0+\
                    "\nLOAD "+ var_reg + " "+reg0+\
                    "\nSUB "+var_reg+" "+reg1+\
                    "\nJZERO "+var_reg+" "+str(com_lines+gen_lines0+6)+\
                    com_code+\
                    "\nRESET "+reg0+\
                    gen_code0+\
                    "\nLOAD "+reg1+" "+reg0+\
                    "\nINC "+reg1+\
                    "\nSTORE "+reg1+" "+reg0+\
                    "\nJUMP -"+str(gen_lines0+ com_lines+8),\
                    gen_lines0 * 2 + gen_lines1 + var_lines + com_lines + 16

        if p.for_asc_range[1]:# totest FOR FROM a TO 10
            for_location, variable, value1  = p.for_asc_range[2:5]

            var_reg, var_code, var_lines = variable

            gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
            gen_code1, gen_lines1 = Helpers.generate_number(value1+1, reg0)

            VariablesManager.add_register(reg0)
            VariablesManager.add_register(reg1)
            VariablesManager.add_register(var_reg)

            return  "\nRESET "+reg0+\
                    gen_code0+\
                    var_code+\
                    "\nSTORE "+ var_reg + " "+reg0+\
                    "\nRESET "+reg0+\
                    gen_code1+\
                    "\nSUB "+reg0+" "+var_reg+\
                    "\nJZERO "+reg0+" "+str(com_lines+gen_lines0+6)+\
                    com_code+\
                    "\nRESET "+reg0+\
                    gen_code0+\
                    "\nLOAD "+var_reg+" "+reg0+\
                    "\nINC "+var_reg+\
                    "\nSTORE "+var_reg+" "+reg0+\
                    "\nJUMP -"+str(gen_lines0+gen_lines1+ com_lines+7),\
                    gen_lines0 * 2 + var_lines + gen_lines1 + com_lines + 10

        
        reg2 = VariablesManager.get_register()

        for_location, range_code, range_lines = p.for_asc_range[2:5]

        gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)

        return  range_code+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nLOAD "+reg1+" "+reg0+\
                "\nINC "+reg0+\
                "\nLOAD "+reg2+" "+reg0+\
                "\nRESET "+reg0+\
                "\nINC "+reg0+\
                "\nADD "+reg0+" "+reg2+\
                "\nSUB "+reg0+" "+reg1+\
                "\nJZERO "+reg0+" "+str(com_lines+gen_lines0+6)+\
                com_code+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nLOAD "+reg1+" "+reg0+\
                "\nINC "+reg1+\
                "\nSTORE "+reg1+" "+reg0+\
                "\nJUMP -"+str(com_lines+gen_lines0+11),\
                range_lines + com_lines + gen_lines0*2 + 14
    
    @_('for_desc_range DO commands end_of_for')
    def command(self, p):
        FlowManager.loops = FlowManager.loops - 1

        com_code, com_lines = p.commands

        reg0 = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()

        if p.for_desc_range[0] and p.for_desc_range[1]:
            for_location, value0, value1 = p.for_desc_range[2:5]

            gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
            gen_code1, gen_lines1 = Helpers.generate_number(value0, reg1)
            gen_code2, gen_lines2 = Helpers.generate_number(value1, reg0)

            VariablesManager.add_register(reg0)
            VariablesManager.add_register(reg1)

            if (value0 - value1) < FlowManager.max_iterations_to_expand_for:
                if not VariablesManager.check_for_used_iterator(p.end_of_for):
                    return com_code*(value0 - value1 + 1), com_lines*(value0 - value1 + 1)

                result_code =   "\nRESET "+reg0+\
                                gen_code0+\
                                "\nRESET "+reg1+\
                                gen_code1+\
                                "\nSTORE "+ reg1 + " "+reg0
                result_lines = gen_lines0 + gen_lines1 + 3

                for i in range(value0 - value1):
                    result_code +=  com_code+\
                                    "\nRESET "+reg0+\
                                    gen_code0+\
                                    "\nLOAD "+reg1+" "+reg0+\
                                    "\nDEC "+reg1+\
                                    "\nSTORE "+reg1+" "+reg0
                    result_lines += com_lines + gen_lines0 + 4
                
                if value0 - value1 >= 0:
                    result_code += com_code
                    result_lines += com_lines
                
                return result_code, result_lines

            return  "\nRESET "+reg0+\
                    gen_code0+\
                    "\nRESET "+reg1+\
                    gen_code1+\
                    "\nSTORE "+ reg1 + " "+reg0+\
                    "\nRESET "+reg0+\
                    gen_code2+\
                    "\nINC "+reg1+\
                    "\nSUB "+reg1+" "+reg0+\
                    "\nJZERO "+reg1+" "+str(com_lines+gen_lines0+7)+\
                    com_code+\
                    "\nRESET "+reg0+\
                    gen_code0+\
                    "\nLOAD "+reg1+" "+reg0+\
                    "\nJZERO "+reg1+" 4"+\
                    "\nDEC "+reg1+\
                    "\nSTORE "+reg1+" "+reg0+\
                    "\nJUMP -"+str(gen_lines0+gen_lines2+ com_lines+9),\
                    gen_lines0 * 2 + gen_lines1 + gen_lines2 + com_lines + 13
                    
        if p.for_desc_range[0]:
            for_location, value0, variable = p.for_desc_range[2:5]

            var_reg, var_code, var_lines = variable

            gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
            gen_code1, gen_lines1 = Helpers.generate_number(value0, reg1)

            VariablesManager.add_register(reg0)
            VariablesManager.add_register(reg1)
            VariablesManager.add_register(var_reg)

            return  "\nRESET "+reg0+\
                    gen_code0+\
                    "\nRESET "+reg1+\
                    gen_code1+\
                    "\nSTORE "+ reg1 + " "+reg0+\
                    "\nINC "+reg0+\
                    var_code+\
                    "\nSTORE "+ var_reg + " "+reg0+\
                    "\nJUMP "+str(3)+\
                    "\nINC "+reg0+\
                    "\nLOAD "+ var_reg + " "+reg0+\
                    "\nINC "+reg1+\
                    "\nSUB "+reg1+" "+var_reg+\
                    "\nJZERO "+reg1+" "+str(com_lines+gen_lines0+7)+\
                    com_code+\
                    "\nRESET "+reg0+\
                    gen_code0+\
                    "\nLOAD "+reg1+" "+reg0+\
                    "\nJZERO "+reg1+" 4"+\
                    "\nDEC "+reg1+\
                    "\nSTORE "+reg1+" "+reg0+\
                    "\nJUMP -"+str(gen_lines0+ com_lines+10),\
                    gen_lines0 * 2 + gen_lines1 + var_lines + com_lines + 17

        if p.for_desc_range[1]:
            for_location, variable, value1  = p.for_desc_range[2:5]

            var_reg, var_code, var_lines = variable

            gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
            gen_code1, gen_lines1 = Helpers.generate_number(value1, reg0)

            VariablesManager.add_register(reg0)
            VariablesManager.add_register(reg1)
            VariablesManager.add_register(var_reg)

            return  "\nRESET "+reg0+\
                    gen_code0+\
                    var_code+\
                    "\nSTORE "+ var_reg + " "+reg0+\
                    "\nRESET "+reg0+\
                    gen_code1+\
                    "\nINC "+var_reg+\
                    "\nSUB "+var_reg+" "+reg0+\
                    "\nJZERO "+var_reg+" "+str(com_lines+gen_lines0+7)+\
                    com_code+\
                    "\nRESET "+reg0+\
                    gen_code0+\
                    "\nLOAD "+var_reg+" "+reg0+\
                    "\nJZERO "+var_reg+" 4"+\
                    "\nDEC "+var_reg+\
                    "\nSTORE "+var_reg+" "+reg0+\
                    "\nJUMP -"+str(gen_lines0+gen_lines1+ com_lines+9),\
                    gen_lines0 * 2 + var_lines + gen_lines1 + com_lines + 13

        
        reg2 = VariablesManager.get_register()

        for_location, range_code, range_lines = p.for_desc_range[2:5]

        gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)

        return  range_code+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nLOAD "+reg1+" "+reg0+\
                "\nINC "+reg0+\
                "\nLOAD "+reg2+" "+reg0+\
                "\nRESET "+reg0+\
                "\nINC "+reg0+\
                "\nADD "+reg0+" "+reg1+\
                "\nSUB "+reg0+" "+reg2+\
                "\nJZERO "+reg0+" "+str(com_lines+gen_lines0+7)+\
                com_code+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nLOAD "+reg1+" "+reg0+\
                "\nJZERO "+reg1+" 4"+\
                "\nDEC "+reg1+\
                "\nSTORE "+reg1+" "+reg0+\
                "\nJUMP -"+str(com_lines+gen_lines0+12),\
                range_lines + com_lines + gen_lines0*2 + 15

 
#endregion