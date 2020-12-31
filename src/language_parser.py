from sly import Parser
from language_lexer import LanguageLexer
from variables_manager import VariablesManager
from helpers import Helpers


class LanguageParser(Parser):
    tokens = LanguageLexer.tokens

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
        raise Exception("Incorrect table declaration")
    
    @_('ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)
    
    @_('ID LEFT NUMBER RIGHT')
    def declarations(self, p):
        raise Exception("Incorrect table declaration")

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
        reg1 = VariablesManager.get_register()

        gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)

        VariablesManager.add_register(reg)
        return reg1, \
                "\nRESET "+reg+\
                "\nRESET "+reg1+\
                gen_code+\
                "\nLOAD "+reg1+" "+reg,\
                gen_lines+3

    @_('ID LEFT ID RIGHT')
    def variable(self, p):
        var_location = VariablesManager.get_location(p.ID1)
        VariablesManager.check_initialization(p.ID1)

        start_location, start_index = VariablesManager.get_table_data(p.ID0)
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()

        gen_code0, gen_lines0 = Helpers.generate_number(var_location, reg1)
        gen_code1, gen_lines1 = Helpers.generate_number(start_index, reg1)
        gen_code2, gen_lines2 = Helpers.generate_number(start_location, reg1)

        VariablesManager.add_register(reg)
        VariablesManager.add_register(reg1)

        return reg2, \
            "\nRESET "+reg+\
            "\nRESET "+reg1+\
            "\nRESET "+reg2+\
            gen_code0+\
            "\nLOAD "+reg2+" " +reg1+\
            "\nRESET "+reg1+\
            "\nADD "+reg+" "+reg2+\
            "\nRESET "+reg1+\
            gen_code1+\
            "\nSUB "+reg+" "+reg1+\
            "\nRESET "+reg1+\
            gen_code2+\
            "\nADD "+reg+" "+reg1+\
            "\nLOAD "+reg2+" "+reg,\
            gen_lines0 + gen_lines1 + gen_lines2 + 11

    @_('ID')
    def variable(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_initialization(p.ID)

        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        
        gen_code, gen_lines = Helpers.generate_number(var_location, reg1)

        VariablesManager.add_register(reg1)

        return reg2,\
            "\nRESET "+reg1+\
            "\nRESET "+reg2+\
            gen_code+\
            "\nLOAD "+reg2+" " +reg1,\
            gen_lines + 3

    @_('ID LEFT NUMBER RIGHT')
    def variable_reference(self, p):
        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1

    @_('ID LEFT ID RIGHT')
    def variable_reference(self, p):
        start_location, start_index = VariablesManager.get_table_data(p.ID0)
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()

        gen_code0, gen_lines0 = Helpers.generate_number(VariablesManager.get_location(p.ID1), reg1)

        gen_code1, gen_lines1 = Helpers.generate_number(start_location, reg1)

        gen_code2, gen_lines2 = Helpers.generate_number(start_index, reg1)


        VariablesManager.add_register(reg1)

        return reg,\
            "\nRESET "+reg+\
            "\nRESET "+reg1+\
            gen_code0+\
            "\nLOAD "+reg+" " +reg1+\
            "\nRESET "+reg1+\
            gen_code1+\
            "\nADD "+reg+" "+reg1+\
            "\nRESET "+reg1+\
            gen_code2+\
            "\nSUB "+reg+" "+reg1,\
            gen_lines0 + gen_lines1 + gen_lines2 + 7

    @_('ID')
    def variable_reference(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_for_iterator(p.ID)
        VariablesManager.initialize_variable(p.ID)

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(var_location, reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1
    
    @_('ID')
    def write_variable_reference(self, p):
        var_location = VariablesManager.get_location(p.ID)
        VariablesManager.check_initialization(p.ID)

        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(var_location, reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1

#endregion

#region value
    @_('variable')
    def value(self, p):
        return p.variable

    @_('NUMBER')
    def value(self, p):
        reg = VariablesManager.get_register()
        gen_code, gen_lines = Helpers.generate_number(p.NUMBER, reg)
        return reg, "\nRESET "+reg + gen_code, gen_lines+1

#endregion

#region IO    
    @_('READ variable_reference SEMICOLON')
    def command(self, p):
        reg, code, lines = p.variable_reference
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

#region ASSIGNments
    @_('variable_reference ASSIGN value SEMICOLON')
    def command(self, p):
        ref_reg, ref_code, ref_lines = p.variable_reference
        val_reg, val_code, val_lines = p.value

        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(val_reg)

        return  ref_code+\
                val_code+\
                "\nSTORE "+val_reg+" "+ref_reg,\
                ref_lines + val_lines + 1
    
    @_('variable_reference ASSIGN value PLUS value SEMICOLON')
    def command(self, p):
        ref_reg, ref_code, ref_lines = p.variable_reference
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  ref_code+\
                val_code0+\
                val_code1+\
                "\nADD "+val_reg0+" "+val_reg1+\
                "\nSTORE "+val_reg0+" "+ref_reg,\
                ref_lines + val_lines0 + val_lines1 + 2

    @_('variable_reference ASSIGN value MINUS value SEMICOLON')
    def command(self, p):
        ref_reg, ref_code, ref_lines = p.variable_reference
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  ref_code+\
                val_code0+\
                val_code1+\
                "\nSUB "+val_reg0+" "+val_reg1+\
                "\nSTORE "+val_reg0+" "+ref_reg,\
                ref_lines + val_lines0 + val_lines1 + 2
    
    @_('variable_reference ASSIGN value MULTI value SEMICOLON')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()

        ref_reg, ref_code, ref_lines = p.variable_reference
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        multi_code, result_register, multi_lines = \
            Helpers.multiplication([val_reg0, val_reg1],[reg1, reg2, reg3])

        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(reg3)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  ref_code+\
                val_code0+\
                val_code1+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                "\nRESET "+reg3+\
                multi_code+\
                "\nSTORE "+result_register+" "+ref_reg,\
                ref_lines + val_lines0 + val_lines1 + multi_lines + 4
    
    @_('variable_reference ASSIGN value DIV value SEMICOLON')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()

        ref_reg, ref_code, ref_lines = p.variable_reference
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        div_code, result_register, div_lines = \
            Helpers.division([val_reg0, val_reg1],[reg1, reg2, reg3])

        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(reg3)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)
        
        return  ref_code+\
                val_code0+\
                val_code1+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                "\nRESET "+reg3+\
                div_code+\
                "\nSTORE "+result_register+" "+ref_reg,\
                ref_lines + val_lines0 + val_lines1 + div_lines + 4
    
    @_('variable_reference ASSIGN value MOD value SEMICOLON')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()

        ref_reg, ref_code, ref_lines = p.variable_reference
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        mod_code, result_register, mod_lines = Helpers.modulo([val_reg0, val_reg1],[reg1, reg2])

        VariablesManager.add_register(ref_reg)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)
        return  ref_code+\
                val_code0+\
                val_code1+\
                "\nRESET "+reg1+\
                "\nRESET "+reg2+\
                mod_code+\
                "\nSTORE "+result_register+" "+ref_reg,\
                ref_lines + val_lines0 + val_lines1 + mod_lines + 3
#endregion

#region condition
    @_('value EQUAL value')
    def condition(self, p):
        reg = VariablesManager.get_register()

        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  val_code0+\
                val_code1+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+val_reg0+\
                "\nSUB "+reg+" "+val_reg1+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 4"+\
                "\nADD "+reg+" "+val_reg1+\
                "\nSUB "+reg+" "+val_reg0+\
                "\nJZERO "+reg+" 2",\
                val_lines0 + val_lines1 + 8
    
    @_('value NOTEQUAL value')
    def condition(self, p):
        reg = VariablesManager.get_register()

        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  val_code0+\
                val_code1+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+val_reg0+\
                "\nSUB "+reg+" "+val_reg1+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 4"+\
                "\nADD "+reg+" "+val_reg1+\
                "\nSUB "+reg+" "+val_reg0+\
                "\nJZERO "+reg+" 2"+\
                "\nJUMP 2",\
                val_lines0 + val_lines1 + 9

    @_('value LESSTHAN value')
    def condition(self, p):
        reg = VariablesManager.get_register()

        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1
        
        VariablesManager.add_register(reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  val_code0+\
                val_code1+\
                "\nRESET "+reg+\
                "\nINC "+reg+\
                "\nADD "+reg+" "+val_reg0+\
                "\nSUB "+reg+" "+val_reg1+\
                "\nJZERO "+reg+" 2",\
                val_lines0 + val_lines1 + 5

    @_('value GREATERTHAN value')
    def condition(self, p):
        reg = VariablesManager.get_register()

        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  val_code0+\
                val_code1+\
                "\nRESET "+reg+\
                "\nINC "+reg+\
                "\nADD "+reg+" "+val_reg1+\
                "\nSUB "+reg+" "+val_reg0+\
                "\nJZERO "+reg+" 2",\
                val_lines0 + val_lines1 + 5
    
    @_('value LESSEQUAL value')
    def condition(self, p):
        reg = VariablesManager.get_register()

        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  val_code0+\
                val_code1+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+val_reg0+\
                "\nSUB "+reg+" "+val_reg1+\
                "\nJZERO "+reg+" 2",\
                val_lines0 + val_lines1 + 4
    
    @_('value GREATEREQUAL value')
    def condition(self, p):
        reg = VariablesManager.get_register()

        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        VariablesManager.add_register(reg)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  val_code0+\
                val_code1+\
                "\nRESET "+reg+\
                "\nADD "+reg+" "+val_reg1+\
                "\nSUB "+reg+" "+val_reg0+\
                "\nJZERO "+reg+" 2",\
                val_lines0 + val_lines1 + 4
#endregion

#region IF
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        cond_code, cond_lines = p.condition
        com_code0, com_lines0 = p.commands0
        com_code1, com_lines1 = p.commands1
        return  cond_code+\
                "\nJUMP "+str(com_lines0+2)+\
                com_code0+\
                "\nJUMP "+str(com_lines1+1)+\
                com_code1,\
                cond_lines + com_lines0 + com_lines1 + 2

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        cond_code, cond_lines = p.condition
        com_code, com_lines = p.commands
        return  cond_code+\
                "\nJUMP "+str(com_lines+1)+\
                com_code,\
                cond_lines + com_lines + 1
#endregion

#region WHILE_REPEAT
    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        cond_code, cond_lines = p.condition
        com_code, com_lines = p.commands
        return  cond_code+\
                "\nJUMP "+str(com_lines+2)+\
                com_code+\
                "\nJUMP -"+str(com_lines+cond_lines+1),\
                cond_lines + com_lines + 2

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        cond_code, cond_lines = p.condition
        com_code, com_lines = p.commands
        return  com_code+\
                cond_code+\
                "\nJUMP -"+str(com_lines+cond_lines),\
                cond_lines + com_lines + 1
#endregion

#region FOR
    @_('FOR ID')
    def for_declaration(self, p):
        VariablesManager.initialize_variable(p.ID)
        return VariablesManager.declare_for(p.ID)
    
    @_('ENDFOR')
    def end_of_for(self, p):
        VariablesManager.undeclare_last_for()

    @_('FOR ID FROM value TO value')
    def for_asc_range(self, p):
        VariablesManager.initialize_variable(p.ID)
        for_location = VariablesManager.declare_for(p.ID)

        reg0 = VariablesManager.get_register()
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  for_location, val_code0+\
                val_code1+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nSTORE "+val_reg0+" "+reg0+\
                "\nINC "+reg0+\
                "\nSTORE "+val_reg0+" "+reg0+\
                "\nINC "+reg0+\
                "\nSTORE "+val_reg1+" "+reg0,\
                val_lines0 + val_lines1 + gen_lines0 + 6
    
    @_('FOR ID FROM value DOWNTO value')
    def for_desc_range(self, p):
        VariablesManager.initialize_variable(p.ID)
        for_location = VariablesManager.declare_for(p.ID)

        reg0 = VariablesManager.get_register()
        val_reg0, val_code0, val_lines0 = p.value0
        val_reg1, val_code1, val_lines1 = p.value1

        gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(val_reg0)
        VariablesManager.add_register(val_reg1)

        return  for_location, val_code0+\
                val_code1+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nSTORE "+val_reg0+" "+reg0+\
                "\nINC "+reg0+\
                "\nSTORE "+val_reg0+" "+reg0+\
                "\nINC "+reg0+\
                "\nSTORE "+val_reg1+" "+reg0,\
                val_lines0 + val_lines1 + gen_lines0 + 6


    @_('for_asc_range DO commands end_of_for')
    def command(self, p):
        reg0 = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()

        com_code, com_lines = p.commands

        for_location, range_code, range_lines = p.for_asc_range

        gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)

        return  range_code+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nLOAD "+reg1+" "+reg0+\
                "\nINC "+reg0+\
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
                "\nJUMP -"+str(com_lines+gen_lines0+12),\
                range_lines + com_lines + gen_lines0*2 + 15
    
    @_('for_desc_range DO commands end_of_for')
    def command(self, p):
        reg0 = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()

        com_code, com_lines = p.commands

        for_location, range_code, range_lines = p.for_desc_range

        gen_code0, gen_lines0 = Helpers.generate_number(for_location, reg0)
        gen_code1, gen_lines1 = Helpers.generate_number(for_location + 2, reg0)

        VariablesManager.add_register(reg0)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)

        return  range_code+\
                "\nRESET "+reg0+\
                gen_code0+\
                "\nLOAD "+reg1+" "+reg0+\
                "\nINC "+reg0+\
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
                "\nJUMP -"+str(com_lines+gen_lines0+13),\
                range_lines + com_lines + gen_lines0*2  + 16

 
#endregion