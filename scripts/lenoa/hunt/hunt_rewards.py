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
if type(args.get('name')) is not str:
    desc += f'{t.error["invalid_type"]} (-name) args must be a string'
    base += f' -desc "{desc}"'
    return base
nameArg=args.last('name')
desc += f'**Adventure**: {nameArg}\n'

if ctx.author.id is None:
    desc += f'{t.error["author"]}'
    base += f' -desc "{desc}"'
    return base
if type(ctx.author.id) is not str:
    desc += f'{t.error["invalid_type"]} Author ID must be a string'
    base += f' -desc "{desc}"'
    return base
dmNameArg='<@'+ctx.author.id+'>'
desc += f'**DM**: {dmNameArg}'

base += f' -desc "{desc}"'

xpTotals = exp.totals(char)
lvlDivisor = t.h_rewards["amtToLvlDivisor"]

# PC section
lvlTotal=0
pcData=[]
if args.get('p') is None:
    error = t.error["missing_args"] + "(-p) args expected"
    base += f' -f "{error}"'
    return base

for pcArgs in args.get('p'):
    pcArgItems=pcArgs.split('|')
    len_pcArgItems = len(pcArgItems)
    
    if len_pcArgItems not in {2,3}:
        error = t.error["inc_args"] + "3 or 4 arguments expected: <name|level|player|[banked/fled/dead]>"
        base += f' -f "{error}"'
        return base

    pcLvl = int(pcArgItems[1])
    
    minLvl = t.h_rewards["minLvl"]
    maxLvl = t.h_rewards["maxLvl"]
    if not t.Num_In_Range(minLvl, maxLvl, pcLvl):
        error = t.error["level"] + f"{minLvl} through {maxLvl}."
        base += f' -f "{error}"'
        return base

    lvlTotal += pcLvl
    xpDiff = t.XP_Diff_For_Curr_Lvl(exp.totals(char), pcLvl)
    xp_reward = xpDiff / lvlDivisor
        
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
if not t.Num_In_Range(minMatCR, maxMatCR, crArg):
    error = t.error["range"] + f"CR must be between {minMatCR} and {maxMatCR} for tier {tier}."
    base += f' -f "{error}"'
    return base
pcCR = crArg
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
        reward += rewardType[pcStateArg]
    fIndiv+=f'- {pc["player"]} as {pc["name"]} Lvl.{pc["level"]}{colon}\n{reward}'
fIndiv+='"'
base += f' {fIndiv}'
# PC section END

# Party section
partyGP=partyLvlAvg * t.h_rewards["gpMultiplier"]
partyDT=t.h_rewards["baseDT"]
if failedArg:
    fParty=f'-f "Party Rewards|Adventure failed, {partyDT} DT"'
else:
    fParty=f'-f "Party Rewards|{partyGP} GP, CR{crArg} Token, {partyDT} DT"'
base += f' {fParty}'
# Party section END

# DM section
##  -dm <name|level|[banked]>
### name : string
### level : int (1-20)
if args.get('dm') is None:
    error = t.error["missing_args"] + "(-dm) args expected"
    base += f' -f "{error}"'
    return base
if type(args.get('dm')) is not str:
    desc += f'{t.error["invalid_type"]} (-dm) args must be a string'
    base += f' -f "{desc}"'
    return base

dmArg=args.last('dm')
dmArgItems=dmArg.split('|')
len_dmArgItems = len(dmArgItems)

##correct num args?
if len_dmArgItems not in {2,3}: 
    error = t.error["inc_args"] + "3 or 4 arguments expected: <name|level|[banked]>"
    base += f' {error}'
    return base
fDM=f'-f "DM Rewards|'

dmName = str(dmArgItems[0])
dmLvl = int(dmArgItems[1])

## correct DM Char Lvl range?
minLvl = t.h_rewards["minLvl"]
maxLvl = t.h_rewards["maxLvl"]
if not t.Num_In_Range(minLvl, maxLvl, dmLvl):
    error = t.error["level"] + f"{minLvl} through {maxLvl}."
    base += f' -f "{error}"'
    return base
fDM+=f'For {dmName} Lvl.{dmLvl}:\n> '

## XP Calc
xpDiff = t.XP_Diff_For_Curr_Lvl(xpTotals, dmLvl)
xp_reward = xpDiff / lvlDivisor
dmXP = xp_reward

dmState = str(dmArgItems[2]) if len(dmArgItems) > 2 else 'normal'
dmDT=t.h_rewards["baseDT"]

## Gold Calc
bankedMultiplier = t.h_rewards["bankedMultiplier"]
dmGP = dmLvl * t.h_rewards["gpMultiplier"]

## If banked, double gold and no XP
if dmState=='banked':
    dmGP*=bankedMultiplier
    dmXP=0
fDM+=f'{dmXP} XP, {dmGP} GP, {dmDT} DT, '

dmTier=t.lvl_tiering[dmLvl]
##A CR Token, the CR of which is determined by the following:
dmCR = 0
if tier<dmTier: ###If the game tier is lower than the tier of your chosen character, then it is the lowest tier appropriate token for your character
    dmCR=t.tiered_mat_cr_min[dmTier]
elif tier>dmTier: ###If the game tier is higher than the tier of your chosen character, then it is the highest tier appropriate token for your character
    dmCR=t.tiered_mat_cr_max[dmTier]
else: ###If the game tier is equal to the tier of your chosen character, then it is the same token give to the PCs that participated
    dmCR=int(pcCR)
fDM+=f'CR{dmCR} Token"'

base += f' {fDM}'
# DM section END

return f'embed {base}'
</drac2>