from sly import Parser
from language_lexer import LanguageLexer
from variables_manager import VariablesManager
from helpers import Helpers


class LanguageParser(Parser):
    tokens = LanguageLexer.tokens

#region program_structure

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        print("HALT")
    
    @_('declarations COMMA ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)
        return p.declarations
    
    @_('ID LEFT NUMBER COLON NUMBER RIGHT')
    def declarations(self, p):
        VariablesManager.declare_table(p.ID, p.NUMBER0, p.NUMBER1)

    @_('declarations COMMA ID')
    def declarations(self, p):
        VariablesManager.declare_variable(p.ID)
        return p.declarations

    @_('ID')
    def declarations(self, p):
        VariablesManager.declare_variable(p.ID)
    
    @_('commands command')
    def commands(self, p):
        return p.commands

    @_('command')
    def commands(self, p):
        pass

#endregion

#region variable(_reference)
    @_('ID LEFT NUMBER RIGHT')
    def variable(self, p):
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)
        print("LOAD "+reg1+" "+reg)
        VariablesManager.add_register(reg)
        return reg1

    @_('ID LEFT variable RIGHT')
    def variable(self, p):
        start_location, start_index = VariablesManager.get_table_data(p.ID)
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        print("ADD "+reg+" "+p.variable)
        Helpers.generate_number(start_index, reg1)
        print("SUB "+reg+" "+reg1)
        Helpers.generate_number(start_location, reg1)
        print("ADD "+reg+" "+reg1)
        print("LOAD "+p.variable+" "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(reg1)
        return p.variable

    @_('ID')
    def variable(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        
        Helpers.generate_number(VariablesManager.get_location(p.ID), reg1)
        print("LOAD "+reg2+" " +reg1)
        VariablesManager.add_register(reg1)
        return reg2

    @_('ID LEFT NUMBER RIGHT')
    def variable_reference(self, p):
        reg = VariablesManager.get_register()
        Helpers.generate_number(VariablesManager.get_table_location(p.ID, p.NUMBER), reg)
        return reg

    @_('ID LEFT variable RIGHT')
    def variable_reference(self, p):
        start_location, start_index = VariablesManager.get_table_data(p.ID)
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        print("ADD "+reg+" "+p.variable)
        Helpers.generate_number(start_index, reg1)
        print("SUB "+reg+" "+reg1)
        Helpers.generate_number(start_location, reg1)
        print("ADD "+reg+" "+reg1)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(p.variable)
        return reg

    @_('ID')
    def variable_reference(self, p):
        reg = VariablesManager.get_register()
        Helpers.generate_number(VariablesManager.get_location(p.ID), reg)
        return reg

#endregion

#region value
    @_('variable')
    def value(self, p):
        return p.variable

    @_('NUMBER')
    def value(self, p):
        reg = VariablesManager.get_register()
        Helpers.generate_number(p.NUMBER, reg)
        return reg

#endregion

#region IO    
    @_('READ variable_reference')
    def command(self, p):
        print("GET "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)

    @_('WRITE NUMBER')
    def command(self, p):
        reg = VariablesManager.get_register()
        reg1 = VariablesManager.get_register()
        temp_location = VariablesManager.get_temp_location()
        Helpers.generate_number(temp_location, reg)
        Helpers.generate_number(p.NUMBER, reg1)
        print("STORE "+reg1+" "+reg)
        print("PUT "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(reg1)
    
    @_('WRITE variable')
    def command(self, p):
        reg = VariablesManager.get_register()
        temp_location = VariablesManager.get_temp_location()
        Helpers.generate_number(temp_location, reg)
        print("STORE "+p.variable+" "+reg)
        print("PUT "+reg)
        VariablesManager.add_register(reg)
        VariablesManager.add_register(p.variable)
#endregion

    @_('variable_reference ASSIGN value')
    def command(self, p):
        print("STORE "+p.value+" "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)
        VariablesManager.add_register(p.value)
    
    @_('variable_reference ASSIGN value PLUS value')
    def command(self, p):
        print("ADD "+p.value0+" "+p.value1)
        print("STORE "+p.value0+" "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)

    @_('variable_reference ASSIGN value MINUS value')
    def command(self, p):
        print("SUB "+p.value0+" "+p.value1)
        print("STORE "+p.value0+" "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)
    
    @_('variable_reference ASSIGN value MULTI value')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()
        result_register = Helpers.multiplication([p.value0, p.value1],[reg1, reg2, reg3])
        print("STORE "+result_register+" "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(reg3)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)
    
    @_('variable_reference ASSIGN value DIV value')
    def command(self, p):
        reg1 = VariablesManager.get_register()
        reg2 = VariablesManager.get_register()
        reg3 = VariablesManager.get_register()
        result_register = Helpers.division([p.value0, p.value1],[reg1, reg2, reg3])
        print("STORE "+result_register+" "+p.variable_reference)
        VariablesManager.add_register(p.variable_reference)
        VariablesManager.add_register(reg1)
        VariablesManager.add_register(reg2)
        VariablesManager.add_register(reg3)
        VariablesManager.add_register(p.value0)
        VariablesManager.add_register(p.value1)

