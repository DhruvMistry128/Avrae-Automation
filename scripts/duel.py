embed

<drac2>
using (
    exp="bd5e6af1-55e9-4c5b-b814-8f9b447091e7",
    time_lib="74a21a79-bc4c-4b03-9b21-a16e2b591a89",
    t="f60313a3-fe57-4354-8b3c-b0a8cb4c5926" # templates
)

#EXP
#update_old(char), get_xp()
#set_xp(new_val, char, return), modify_xp(val_mod, char, return)
#next_lvl(compare_xp, char)-> (next_lvl, xp_to_next_lvl, next_lvl_xp_diff)
#level(lvl, xp, char)-> (lvl, xp_total, xp_total_diff_from_lvl_xp)
#totals(xp, char)-> (lvl_xp)
#xp_name(char), cc_name(char)

#TIME LIBRARY
# currTime, days_in_month, emoji_map, weather_and_sideevent_DC_mod_yaml, currMidnight, timeOfDay
# is_daytime(), prettyCurrentSeason(), get_current_season(), get_moon_phase(), roll_weather(), get_weather_effects(), get_weather_emoji(), get_wind_direction(), get_strange_phenomena(), todays_weather(), get_weather_title(), update_weather(), one_day_passed()

# [T]EMPLATES

title = t.duel["title"]
footer = t.footer_prefix + t.duel["footer_postfix"] + t.credits.credited_names()
desc = ""
</drac>

-thumb <image>
-title "{{title}}"
-footer "{{footer}}"

-desc "<drac2>
char_level, _, _ = exp.level()
minLvl = t.duel["minLvl"]
maxLvl = t.duel["maxLvl"]

if t.Invalid_Level(minLvl, maxLvl, char_level):
    desc = t.error["level"]
    desc += f" Valid Range : {minLvl} through {maxLvl}. Level Provided: {char_level}."
    return(desc)

args = argparse(&ARGS&)
is_winner = args.last("win")

if not t.Is_Arg_Bool_Interpretable(is_winner):
    desc = t.error["data_type_bool"]
    desc += f"\"-win\"\nValue Provided: {str(is_winner)}."
    return(desc)
        
is_winner = t.Interpret_Arg_As_Bool(is_winner)

char = character()

spar_cvar = t.duel["previous_use_date_cvar"]
last_day_command_used = t.Validate_CVar(
    char, spar_cvar, "int", 0
)

day_offset = t.time["day"]
hours_offset = t.duel["reset_offset_hours"]
reset_time = time_lib.currMidnight + hours_offset
next_day = reset_time + day_offset

if last_day_command_used >= reset_time:
    desc = f"It's too soon for this character to earn experience again, you can spar again after {t.To_Timestamp_String(next_day)}"
    return(desc)

last_day_command_used = reset_time
char.set_cvar(spar_cvar, str(last_day_command_used))
    
amtToLvlDivisor = t.duel["amtToLvlDivisor"]
loseDivisor = t.duel["loseDivisor"]
winMult = round(
    (1.0 / amtToLvlDivisor), 
    4
)
loseMult = round(
    (winMult / loseDivisor),
    4
)

lvl_xp_totals = exp.totals(char)
current_lvl_xp_total = lvl_xp_totals[char_level - 1]
next_lvl_xp_total = lvl_xp_totals[char_level]
xp_diff  = next_lvl_xp_total - current_lvl_xp_total
xp_earned = 0

duel_status = ""

if is_winner is True:
    xp_earned = round(xp_diff * winMult, 0)
    duel_status = f"won"
else: # if is_winner is False:
    xp_earned = round(xp_diff * loseMult, 0)
    duel_status = f"lost"

char_xp = exp.get_xp()
new_xp_total = char_xp + xp_earned

exp.set_xp(new_xp_total, char)

desc = f"{name} has {duel_status} the duel and earns {xp_earned} XP.\n"
desc += f"Current Level: {char_level}, Original XP: {char_xp} -> New XP: {new_xp_total}.\n"
desc += f"Next available spar date: {t.To_Timestamp_String(next_day)}"

return(desc)

</drac2>"
