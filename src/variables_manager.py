class VariablesManager:
    variables_locations={}
    tables_locations={}
    next_location = 0
    availble_registers = ['a','b','c','d','e','f']

    def declare_variable(id):
        if id in VariablesManager.variables_locations.keys() or id in VariablesManager.tables_locations.keys():
            raise Exception("Variable already declared")

        VariablesManager.variables_locations[id]=VariablesManager.next_location
        VariablesManager.next_location+=1
    
    # def declare_table(id, size):sni
    #     if id in VariablesManager.variables_locations.keys() or id in VariablesManager.tables_locations.keys():
    #         raise Exception("Variable already declared")

    #     VariablesManager.variables_locations[id]=(VariablesManager.next_location,0,size-1)
    #     VariablesManager.next_location+=size
    
    def declare_table(id, start, end):
        if end < start:
            raise Exception("End index bigger than start index")

        if id in VariablesManager.variables_locations.keys() or id in VariablesManager.tables_locations.keys():
            raise Exception("Variable already declared")

        VariablesManager.tables_locations[id]=(VariablesManager.next_location,start,end)
        VariablesManager.next_location+=end-start+1

    def get_table_location(id, index):
        if id in VariablesManager.variables_locations.keys():
            raise Exception("Variable is a variable")

        if id not in VariablesManager.tables_locations.keys():
            raise Exception("Undeclared variable")
        
        table_data = VariablesManager.tables_locations[id]

        if index>table_data[2] or index<table_data[1]:
            raise Exception("Index out of range")

        return table_data[0]+index-table_data[1]
    
    def get_table_data(id):
        if id in VariablesManager.variables_locations.keys():
            raise Exception("Variable is a variable")

        if id not in VariablesManager.tables_locations.keys():
            raise Exception("Undeclared variable")
        
        table_data = VariablesManager.tables_locations[id]

        return table_data[0], table_data[1]

    def get_location(id):
        if id in VariablesManager.tables_locations.keys():
            raise Exception("Variable is a table")

        if id not in VariablesManager.variables_locations.keys():
            raise Exception("Undeclared variable")
        
        return VariablesManager.variables_locations[id]
    
    def get_temp_location():
        return VariablesManager.next_location

    def get_register():
        return VariablesManager.availble_registers.pop(0)
    
    def add_register(register):
        print("RESET "+register)
        return VariablesManager.availble_registers.append(register)
        
