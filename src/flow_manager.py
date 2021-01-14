class FlowManager:
    max_iterations_to_expand_for = 10
    variables_values = {}
    tables_values = []
    ifs = 0
    loops = 0
    repeat_loops = 0

    def drop_constant_variable(variable):
        if variable in FlowManager.variables_values.keys():
            FlowManager.variables_values.pop(variable)

    def drop_constant_table(table_to_drop, index_to_drop):
        for (table, index, value) in list(FlowManager.tables_values):
            if table == table_to_drop and index == index_to_drop:
                FlowManager.tables_values.remove((table, index, value))

    def drop_whole_constant_table(table_to_drop):
        for (table, index, value) in list(FlowManager.tables_values):
            if table == table_to_drop:
                FlowManager.tables_values.remove((table, index, value))

    def set_constant_variable(variable, value):
        if FlowManager.ifs == 0 and FlowManager.loops == 0:
            FlowManager.variables_values[variable] = value
        else:
            FlowManager.drop_constant_variable(variable)
    
    def set_constant_table(table, index, value):
        if FlowManager.ifs == 0 and FlowManager.loops == 0:
            FlowManager.drop_constant_table(table, index)
            FlowManager.tables_values.append((table, index, value))
        else:
            FlowManager.drop_constant_table(table, index)
    
    def check_for_constant(variable):
        return variable in FlowManager.variables_values.keys() and FlowManager.loops == 0 and FlowManager.repeat_loops == 0
    
    def check_for_table_constant(table, index):
        if FlowManager.loops != 0 and FlowManager.repeat_loops != 0:
            return False
        
        for (cur_table, cur_index, cur_value) in FlowManager.tables_values:
            if cur_table == table and cur_index == index:
                return True

        return False

    def get_constant_value(variable):
        return FlowManager.variables_values[variable]

    def get_constant_table_value(table, index):
        for (cur_table, cur_index, cur_value) in FlowManager.tables_values:
            if cur_table == table and cur_index == index:
                return cur_value