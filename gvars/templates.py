# Lenoa Command Templates

command_prefix = f"{{ctx.prefix+ctx.alias}} "
credits =  f" || alias by chaoshyper, Henpus, Mister Man, Roonana Roomimi"

error = {
    "level" : f"[Error] : character level is not in the valid range! >> ",
    "data_type_bool" : f"[Error] : Following argument must be 'True' or 'False' >> "
}

time = {
    "second" : 1,
    "minute" : 60,
    "hour" : 60*60,
    "day" : 60*60*24,
    "week" : 60*60*24*7,
    "month" : 60*60*24*30,
    "year" : 60*60*24*365,
}   

def Invalid_Level(minLvl, maxLvl, char_level):
    if char_level < minLvl:
        return True
    elif char_level > maxLvl:
        return True
    else:
        return False

def Is_Arg_Bool_Interpretable(value):
    if value in ["true", "True", True, "false", "False", False]:
        return True
    else:
        return False

def Interpret_Arg_As_Bool(value):
    if value in ["true", "True", True]:
        return True
    elif value in ["false", "False", False]:
        return False
    else:
        return bool(value)

def Cast_Var_To_Type(var, var_type):
    if var_type == "int":
        return int(var)
    elif var_type == "float":
        return float(var)
    elif var_type == "str":
        return str(var)
    elif var_type == "bool":
        return Interpret_Arg_As_Bool(var)
    else:
        return var

def Validate_CVar(char, cvar_name, cvar_data_type, default_value):
    cvar_value = char.get_cvar(cvar_name)
    if cvar_value is None:
        casted_default = Cast_Var_To_Type(default_value, cvar_data_type)
        char.set_cvar(cvar_name, casted_default)
        cvar_value = casted_default
    return Cast_Var_To_Type(cvar_value, cvar_data_type)

def To_Timestamp_String(epoch_seconds):
    return "<t:" + str(epoch_seconds) + ":F>"

duel = {
    "title" : f"How much have you learned from this bout?",
    "footer_postfix" : f"spar -win <'True' or 'False'>",
    "minLvl" : 1,
    "maxLvl" : 16,
    "reset_offset_hours" : 4 * time["hour"],
    "previous_use_date_cvar" : "previous_spar_date",
    "amtToLvlDivisor" : 10, # amount of times character must win to level up
    "loseDivisor" : 2 # divisor for win multiplier to determine lose multiplier
}