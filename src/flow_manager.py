class FlowManager:
    variables_values = {}
    flow_modifier_encountered = False

    def set_constant_variable(variable, value):
        FlowManager.variables_values[variable] = value
    
    def check_for_assignable_constant(variable):
        return not FlowManager.flow_modifier_encountered

    def check_for_constant(variable):
        return variable in FlowManager.variables_values.keys()

    def get_constant_value(variable):
        return FlowManager.variables_values[variable]