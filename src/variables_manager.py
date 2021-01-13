from language_lexer import LanguageLexer

class VariablesManager:
    variables_locations={}
    initialized_variables=[]
    tables_locations={}
    for_locations={}
    declared_fors=[]
    next_location = 0
    availble_registers = ['a','b','c','d','e','f']

    def declare_variable(id):
        if id in VariablesManager.variables_locations.keys() or id in VariablesManager.tables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Variable already declared: "+id)

        VariablesManager.variables_locations[id]=VariablesManager.next_location
        VariablesManager.next_location+=1
    
    def initialize_variable(id):
        VariablesManager.initialized_variables.append(id)
    
    def check_initialization(id):
        if id not in VariablesManager.initialized_variables:
            raise Exception("Line "+str(LanguageLexer.line_count)+": Use of not initialized variable: "+id)
    
    def declare_table(id, start, end):
        if end < start:
            raise Exception("Line "+str(LanguageLexer.line_count)+": End index bigger than start index")

        if id in VariablesManager.variables_locations.keys() or id in VariablesManager.tables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Variable already declared: "+id)

        VariablesManager.tables_locations[id]=(VariablesManager.next_location,start,end)
        VariablesManager.next_location+=end-start+1
    
    def declare_for(id):
        if id in VariablesManager.variables_locations.keys() or \
            id in VariablesManager.tables_locations.keys() or \
            id in VariablesManager.for_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Variable already declared: "+id)

        VariablesManager.declared_fors.append(id)
        VariablesManager.for_locations[id]=VariablesManager.next_location
        VariablesManager.next_location+=2

        return VariablesManager.for_locations[id]
    
    def check_for_iterator(id):
        if id in VariablesManager.for_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": For iterator modified: "+id)
    
    def undeclare_last_for():
        last_for = VariablesManager.declared_fors[-1]
        VariablesManager.declared_fors = VariablesManager.declared_fors[:-1]
        last_location = VariablesManager.for_locations.pop(last_for)
        if last_location == VariablesManager.next_location - 2:
            VariablesManager.next_location-=2

    def get_table_location(id, index):
        if id in VariablesManager.variables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Variable used as table: "+id)

        if id not in VariablesManager.tables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Undeclared variable: "+id)
        
        table_data = VariablesManager.tables_locations[id]

        if index>table_data[2] or index<table_data[1]:
            raise Exception("Line "+str(LanguageLexer.line_count)+": Index out of range")

        return table_data[0]+index-table_data[1]
    
    def get_table_data(id):
        if id in VariablesManager.variables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Variable used as table: "+id)

        if id not in VariablesManager.tables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Undeclared variable: "+id)
        
        table_data = VariablesManager.tables_locations[id]

        return table_data[0], table_data[1]

    def get_location(id):
        if id in VariablesManager.tables_locations.keys():
            raise Exception("Line "+str(LanguageLexer.line_count)+": Table used as variable: "+id)

        if id not in VariablesManager.variables_locations.keys():
            if id in VariablesManager.for_locations.keys():
                return VariablesManager.for_locations[id]        
            raise Exception("Line "+str(LanguageLexer.line_count)+": Undeclared variable: "+id)
        
        return VariablesManager.variables_locations[id]
    
    def get_for_location(id):
        return VariablesManager.for_locations[id]
    
    def get_last_for_location():
        last_for_id = VariablesManager.declared_fors[-1]
        return VariablesManager.for_locations[last_for_id]
    
    def get_temp_location():
        return VariablesManager.next_location

    def get_register():
        return VariablesManager.availble_registers.pop(0)
    
    def add_register(register):
        VariablesManager.availble_registers.append(register)
        
