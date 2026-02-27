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

char = character()
hr = t.hunt_rewards
e = t.error

title = hr["title"]
footer = t.command_prefix + hr["footer_postfix"] + t.credits + hr["credits"]
base = f'embed -title "{title}" -footer "{footer}"'

desc = f''

args=argparse(&ARGS&)
failedArg=args.get('fail')

crArg=args.last('cr')
if crArg is None:
    desc += e["missing_args"] + f' (-cr)'
    base += f' -desc "{desc}"'
    return base

nameArg=args.last('name')
if nameArg is None:
    desc += e["missing_args"] + f' (-name)'
    base += f' -desc "{desc}"'
    return base

desc += f'**Adventure**: {nameArg}\n'

if ctx.author.id is None:
    desc += e["author"] + f'Unexpected error, notify staff.'
    base += f' -desc "{desc}"'
    return base
dmNameArg='<@'+ctx.author.id+'>'
desc += f'**DM**: {dmNameArg}\n'

base += f' -desc "{desc}"'

xpTotals = exp.totals(char)
lvlDivisor = hr["amtToLvlDivisor"]

# PC section
lvlTotal=0
pcData=[]
if len(args.get('p')) < 1:
    error = e["missing_args"] + "(-p)"
    base += f' -f "{error}"'
    return base

minLvl = int(hr["minLvl"])
maxLvl = int(hr["maxLvl"])

for pcArgs in args.get('p'):
    pcArgItems=pcArgs.split('|')
    len_pcArgItems = len(pcArgItems)
    
    if len_pcArgItems not in {3,4}:
        error = e["inc_args"] + f'3 or 4'
        base += f' -f "{error}"'
        return base

    pcLvl = int(pcArgItems[1])
    
    if not t.Num_In_Range(minLvl, maxLvl, pcLvl):
        error = e["level"] + f'in the (-pc) argument is {minLvl} through {maxLvl}.'
        base += f' -f "{error}"'
        return base

    lvlTotal += pcLvl
    xpDiff = t.XP_Diff_For_Curr_Lvl(exp.totals(char), pcLvl)
    xp_reward = xpDiff / lvlDivisor
    
    if len(pcArgItems) == 3:
        pcArgItems.append('normal')
    
    if pcArgItems[3] not in hr["reward_types"].keys():
        error = e["range"] + f'(-p)!. [banked/fled/dead] argument must be either be present or left empty!.'
        base += f' -f "{error}"'
        return base
    
        
    pcData.append({
        'name': str(pcArgItems[0]),
        'level': pcLvl,
        'player': str(pcArgItems[2]),
        'state': str(pcArgItems[3]),
        'xp': xp_reward,
    })

partyLvlAvg = round(lvlTotal / len(pcData))
tier=t.lvl_tiering[partyLvlAvg]

minMatCR = int(t.tiered_mat_cr_min[tier])
maxMatCR = int(t.tiered_mat_cr_max[tier])
crArg = int(crArg)

if crArg > maxMatCR:
    pcCR = maxMatCR
elif crArg < minMatCR:
    pcCR = minMatCR
else:
    pcCR = crArg
    
rewardType = hr["reward_types"]

fIndiv='-f "Individual Rewards|'
for pc in pcData:
    pcStateArg = pc['state']
    colon=':' if not failedArg else ''
    reward=''
    if not failedArg:
        if pcStateArg=='normal':
            reward=f'> Gains {pc["xp"]} '
        reward += rewardType[pcStateArg]
    fIndiv+=f'- {pc["player"]} as {pc["name"]} Lvl.{pc["level"]}{colon}\n{reward}'
fIndiv+='"'
base += f' {fIndiv}'
# PC section END

# Party section
partyGP=partyLvlAvg * hr["gpMultiplier"]
partyDT=hr["baseDT"]
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
dmArg=args.last('dm')
if dmArg is None:
    desc += e["missing_args"] + f' (-dm)'
    base += f' -desc "{desc}"'
    return base


dmArgItems=dmArg.split('|')
len_dmArgItems = len(dmArgItems)

##correct num args?
if len_dmArgItems not in {2,3}: 
    error = e["inc_args"] + "2 or 3 arguments expected for (-dm)!"
    base += f' "{error}"'
    return base
fDM=f'-f "DM Rewards|'

dmName = str(dmArgItems[0])
dmLvl = int(dmArgItems[1])

## correct DM Char Lvl range?
minLvl = hr["minLvl"]
maxLvl = hr["maxLvl"]
if not t.Num_In_Range(minLvl, maxLvl, dmLvl):
    error = e["level"] + f'in the (-dm) argument is {minLvl} through {maxLvl}.'
    base += f' -f "{error}"'
    return base
fDM+=f'For {dmName} Lvl.{dmLvl}:\n> '

## XP Calc
xpDiff = t.XP_Diff_For_Curr_Lvl(xpTotals, dmLvl)
xp_reward = xpDiff / lvlDivisor
dmXP = xp_reward

dmState = str(dmArgItems[2]) if len(dmArgItems) > 2 else 'normal'
if dmState not in {'banked', 'normal'}:
    error = e["range"] + f'(-dm)! [banked] argument must be either be present or left empty!'
    base += f' -f "{error}"'
    return base
dmDT=hr["baseDT"]

## Gold Calc
bankedMultiplier = hr["bankedMultiplier"]
dmGP = dmLvl * hr["gpMultiplier"]

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

return base
</drac2>