class FlowManager:
    max_iterations_to_expand_for = 10
    variables_values = {}
    tables_values = {}
    ifs = 0
    loops = 0
    repeat_loops = 0

    def drop_constant_variable(variable):
        if variable in FlowManager.variables_values.keys():
            FlowManager.variables_values.pop(variable)

    def drop_constant_table(table, index):
        if (table, index) in FlowManager.tables_values.keys():
            FlowManager.tables_values.pop((table, index))
            
    def drop_constant_table(table_to_drop):
        for (table, index) in FlowManager.tables_values.keys():
            if table == table_to_drop:
                FlowManager.tables_values.pop((table, index))

    def set_constant_variable(variable, value):
        if FlowManager.ifs == 0 and FlowManager.loops == 0:
            FlowManager.variables_values[variable] = value
    
    def set_constant_table(table, index, value):
        if FlowManager.ifs == 0 and FlowManager.loops == 0:
            FlowManager.tables_values[(table, index)] = value
    
    def check_for_constant(variable):
        return variable in FlowManager.variables_values.keys() and FlowManager.loops == 0 and FlowManager.repeat_loops == 0
    
    def check_for_table_constant(table, index):
        return (table, index) in FlowManager.variables_values.keys() and FlowManager.loops == 0 and FlowManager.repeat_loops == 0

    def get_constant_value(variable):
        return FlowManager.variables_values[variable]

    def get_constant_table_value(table, index):
        return FlowManager.variables_values[(table, index)]