class FlowManager:
    max_iterations_to_expand_for = 10
    variables_values = {}
    ifs = 0
    loops = 0
    repeat_loops = 0

    def drop_constant_variable(variable):
        if variable in FlowManager.variables_values.keys():
            FlowManager.variables_values.pop(variable)

    def set_constant_variable(variable, value):
        if FlowManager.ifs == 0 and FlowManager.loops == 0:
            FlowManager.variables_values[variable] = value
    
    def check_for_constant(variable):
        return variable in FlowManager.variables_values.keys() and FlowManager.loops == 0 and FlowManager.repeat_loops == 0

    def get_constant_value(variable):
        return FlowManager.variables_values[variable]

    def drop_constants(variable):
        FlowManager.flow_modifier_encountered = True
        FlowManager.variables_values = {}