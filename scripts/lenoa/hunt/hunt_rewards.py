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

# [T]EMPLATES

title = t.h_rewards["title"]
footer = t.command_prefix + t.h_rewards["footer_postfix"] + t.credits.credited_names() + ', ☢️'
base = f'-title "{title}" -footer "{footer}"'

desc = f''

args=argparse(&ARGS&)
failedArg=args.get('fail')
crArg=args.last('cr')

if args.get('name') is None:
    desc += f'{t.error["missing_args"]} (-name) args expected'
    base += f' -desc "{desc}"'
    return base
nameArg=args.last('name')
desc += f'**Adventure**: {nameArg}\n'

if ctx.author.id is None:
    desc += f'{t.error["author"]}'
    base += f' -desc "{desc}"'
    return base
dmNameArg='<@'+ctx.author.id+'>'
desc += f'**DM**: {dmNameArg}'

base += f' -desc "{desc}"'

xpTotals = exp.totals(char)
lvlDivisor = t.h_rewards["amtToLvlDivisor"]

# DM section with double gold and no XP if double
if args.get('dm') is None:
    error = t.error["missing_args"] + "(-dm) args expected"
    base += f' {error}'
    return base

dmArg=args.last('dm')
dmArgItems=dmArg.split('|')
len_dmArgItems = len(dmArgItems)

##correct num args?
if len_dmArgItems not in {2,3}: 
    error = t.error["inc_args"] + "3 or 4 arguments expected: <name|level|[double]>"
    base += f' {error}'
    return base
    
dmLvl = int(dmArgItems[1])

## correct DM Char range?
minLvl = t.h_rewards["minLvl"]
maxLvl = t.h_rewards["maxLvl"]
if t.Invalid_Level(minLvl, maxLvl, dmLvl):
    error = t.error["level"] + f"{minLvl} through {maxLvl}."
    base += f' {error}'
    return base
    
xpDiff = t.XP_Diff_For_Curr_Lvl(xpTotals, dmLvl)

xp_reward = xpDiff / lvlDivisor
while len(dm_data)<3: dm_data.append('normal')
dm_name=dm_data[0]
dm_level=int(dm_data[1])
dm_state=dm_data[2].lower()

dm_xp=level_xp.get(dm_data[1],0)
dm_gold=dm_level*60

if dm_state=='double':
    dm_gold*=2
    dm_xp=0

dm_tier=level_tier.get(str(dm_level),1)
if tier<dm_tier:
    dm_cr=tier_cr_ranges[str(dm_tier)][0]
elif tier==dm_tier:
    dm_cr=int(a_cr)
else:
    dm_cr=tier_cr_ranges[str(dm_tier)][1]

dm_line=f'For {dm_name} Lvl.{dm_level}:\n'
dm_parts=[]
if dm_state != 'double':
    dm_parts.append(f'{dm_xp} XP')
dm_parts.append(f'{dm_gold} GP')
dm_parts.append(f'CR{dm_cr} Token')
dm_parts.append(f'{partyDT} DT')

fDM=f'-f "DM Rewards|{dm_line}> '+', '.join(dm_parts)+'"'

base += f' {fDM}'


base=f'-title "{title}" -desc "**Adventure**: {nameArg}\n**DM**: {dmArg}" -footer "{footer}, ☢️"'

# PC section
lvlTotal=0
pcData=[]
if args.get('p') is None:
    return t.error["missing_args"] + "(-p) args expected"

for pcArgs in args.get('p'):
    pcArgItems=pcArgs.split('|')
    len_pcArgItems = len(pcArgItems)
    
    if len_pcArgItems not in {2,3}:
        return t.error["inc_args"] + "3 or 4 arguments expected: <name|level|player|[banked/fled/dead]>"
      
    pcLvl = int(pcArgItems[1])
    
    if t.Invalid_Level(t.h_rewards["minLvl"], t.h_rewards["maxLvl"], pcLvl):
        return t.error["level"] + f"{t.h_rewards['minLvl']} through {t.h_rewards['maxLvl']}."
        
    lvlTotal += pcLvl
    xpDiff = t.XP_Diff_For_Curr_Lvl(exp.totals(char), pcLvl)
    xpDiv = t.h_rewards["amtToLvlDivisor"]
    xp_reward = xpDiff / xpDiv
        
    pcData.append({
        'name': str(pcArgItems[0]),
        'level': pcLvl,
        'player': str(pcArgItems[2]),
        'state': str(pcArgItems[3]) if len(pcArgItems) > 2 else 'normal',
        'xp': xp_reward,
    })
    
partyLvlAvg = lvlTotal / len(pcData)

tier=t.lvl_tiering[partyLvlAvg]

minMatCR = t.tiered_mat_cr_min[tier]
maxMatCR = t.tiered_mat_cr_max[tier]

if crArg < minMatCR or crArg > maxMatCR:
    return t.error["range"] + f"CR must be between {minMatCR} and {maxMatCR} for tier {tier}."
    
matCR = crArg
rewardType = t.h_rewards["reward_types"]

fIndiv='-f "Individual Rewards|'
for pc in pcData:
    pcStateArg = pc['state']
    colon=':' if not failedArg else ''
    if failedArg:
        reward=''
    else:
        if pcStateArg=='normal':
            reward=f'> Gains {pc["xp"]} '
        reward  += rewardType[pcStateArg]
    fIndiv+=f'- {pc["player"]} as {pc["name"]} Lvl.{pc["level"]}{colon}\n{reward}'
fIndiv+='"'
# PC section END

# Party section
partyGP=partyLvlAvg * t.h_rewards["gpMultiplier"]
partyDT=t.h_rewards["baseDT"]
if failedArg:
    fParty=f'-f "Party Rewards|Adventure failed, {partyDT} DT"'
else:
    fParty=f'-f "Party Rewards|{partyGP} GP, CR{crArg} Token, {partyDT} DT"'
# Party section END

return f'embed {base} {fIndiv} {fParty} {fDM}'
</drac2>