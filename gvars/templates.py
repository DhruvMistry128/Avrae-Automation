# Lenoa Command Templates

command_prefix = f"{ctx.prefix+ctx.alias} "
credits =  f" || alias by chaoshyper, Henpus, Mister Man, Roonana Roomimi"

error = {
    "level" : f"[Error] : character level is not in the valid range! >> ",
    "data_type_bool" : f"[Error] : Following argument must be 'True' or 'False' >> ",
    "missing_args" : f"[Error] : Missing required arguments! >> ",
    "inc_args" : f"[Error] : Incorrect number of arguments provided! >> ",
    "range" : f"[Error] : Argument out of valid range! >> ",
    "author" : f"[Error] : Command author not detected! >> ",
    "invalid_type" : f"[Error] : Argument type is invalid! >> "
}

unix_time_intervals = {
    "second" : 1,
    "minute" : 60,
    "hour" : 60*60,
    "day" : 60*60*24,
    "week" : 60*60*24*7,
    "month" : 60*60*24*30,
    "year" : 60*60*24*365,
}   

lvl_tiering = {
    1:1,
    2:1,
    3:1,
    4:1,
    5:2,
    6:2,
    7:2,
    8:2,
    9:3,
    10:3,
    11:3,
    12:3,
    13:4,
    14:4,
    15:4,
    16:4,
    17:5,
    18:5,
    19:5,
    20:6
}

tiered_mat_cr_min = {
    1: 1,
    2: 4,
    3: 9,
    4: 13,
    5: 19,
    6: 19
}

tiered_mat_cr_max = {
    1: 3,
    2: 8,
    3: 12,
    4: 18,
    5: 25,
    6: 30
}

def Num_In_Range(min, max, num):
    if num < min:
        return True
    elif num > max:
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

def XP_Diff_For_Curr_Lvl(lvl_xp_totals, level):
    current_lvl_xp_total = lvl_xp_totals[level - 1]
    next_lvl_xp_total = lvl_xp_totals[level]
    xp_diff  = next_lvl_xp_total - current_lvl_xp_total
    return xp_diff

lenoa = {
    "name" : "lenoa",
    "title" : f"Lenoa Home Command List",
    "footer_postfix" : f"lenoa",
}

lookup = {
    "name" : "lookup",
    "title" : f"Lookup Lenoa Game Information",
    "footer_postfix" : f"lookup <category name>",
}

rpgp = {
    "name" : "rpgp",
    "title" : f"Convert Mee6 Levels from RP into GP for PCs!",
    "footer_postfix" : f"rpgp <mee6 levels>",
}

rpxp = {
    "name" : "rpxp",
    "title" : f"Convert Mee6 Levels from RP into XP for PCs!",
    "footer_postfix" : f"rpxp <mee6 levels>",
}

scgp = {
    "name" : "scgp",
    "title" : f"Convert number of checked character sheets into GP for PCs!",
    "footer_postfix" : f"scgp <sheets checked>",
}

scxp = {
    "name" : "scxp",
    "title" : f"Convert number of checked character sheets into XP for PCs!",
    "footer_postfix" : f"scxp <sheets checked>",
    "maxLvl" : 19,
}

feat = {
    "name" : "feat",
    "title" : f"Automation for Lenoa Feats",
    "footer_postfix" : f"feat <feat name>",
}

mastery = {
    "name" : "mastery",
    "title" : f"Automation for Lenoa Weapon Masteries",
    "footer_postfix" : f"mastery <weapon mastery name>",
}

explore = {
    "name" : "explore",
    "title" : f"Explore the Lenoa World!",
    "footer_postfix" : f"explore -distance <number of hexes to travel> -time <time to cross each hex>",
}

hunt_rewards = {
    "name" : "hunt_rewards",
    "title" : f"Hunt Rewards",
    "footer_postfix" : f"hunt_rewards -name <name> -cr <cr> -p <name|level|player|[banked/fled/dead]> -dm <name|level[|double]> [fail]",
    "reward_types" : {
        'dead':'> Died, no rewards\n',
        'fled':'> Fled, only DT\n',
        'banked':'> Forgoes XP for double gold\n',
        'normal':'XP\n'
    },
    "minLvl" : 1,
    "maxLvl" : 19,
    "amtToLvlDivisor" : 5,
    "gpMultiplier" : 60,
    "bankedMultiplier" : 2,
    "baseDT" : 2
}

spar = {
    "name" : "spar",
    "title" : f"How much have you learned from this bout?",
    "footer_postfix" : f"spar -win <'True' or 'False'>",
    "minLvl" : 1,
    "maxLvl" : 16,
    "reset_offset_hours" : 4,
    "previous_use_date_cvar" : "previous_spar_date",
    "amtToLvlDivisor" : 10, # amount of times character must win to level up
    "loseDivisor" : 2 # divisor for win multiplier to determine lose multiplier
}

commands = {
    "lenoa" : lenoa, 
    "lookup" : lookup,
    "rpxp" : rpxp,
    "rpgp" : rpgp,
    "scxp" : scxp,
    "scgp" : scgp,
    "feat" : feat,
    "mastery" : mastery,
    "explore" : explore,
    "hrewards" : hunt_rewards,
    "spar" : spar
}