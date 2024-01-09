# errata'd feats
# contains the list of all erratad feats

# 0 - feat name
# 1 - notes
# 2 - pre-requisites
# 3 - description
feats = [
    ["Close Quarters Shooter [CQS] ‼️",  "Replaces Crossbow Expert and Sharpshooter",                            "none", "* Being within 5 feet of a hostile creature doesn't impose disadvantage on your ranged attack rolls.\n* Your ranged attacks ignore half cover and three-quarters cover against targets within 30 feet of you.\n* When you use the Attack action and attack with a one-handed weapon, you can use a bonus action to attack with a one-handed ranged weapon you are holding.\n* While wielding a one-handed ranged weapon, if your other hand is wielding a one-handed weapon, it is treated as being a free hand for the Ammunition property."],
    ["Crossbow Expert [CE] ❌",         "Removed: Replaced by Close Quarters Shooter and Loaded Arms Training", "-",    "-"],
    ["Dual Wielder [DuW] ⚠️",            "Errata for Dueal Wielder",                                             "none", "You master fighting with two weapons, gaining the following benefits:\n* You can use one-handed weapons as if they have the light property for you.\n* If a weapon already has the light property innately, you can treat it as also having the Nick [Mastery] property.\n* You can draw or stow two one-handed weapons when you would normally be able to draw or stow only one.\n* You gain a +1 bonus to AC while you are wielding a separate melee weapon in each hand."],
    ["Grappler [Gra] ⚠️",               "Errata for Grappler",                                                  "none", "You've developed the skills necessary to hold your own in close-quarters grappling. You gain the following benefits:\n* While you are grappling only one creature, your speed is not halved.\n* You have advantage on attack rolls against a creature you are grappling.\n* You can use your action to try to pin a creature grappled by you. To do so, make another grapple check. If you succeed, the creature is restrained until the grapple ends."],
    ["Great Weapon Master [GWM] ⚠️",    "Errata for Great Weapon Master",                                       "none", "You've learned to put the weight of a weapon to your advantage, letting its momentum empower your strikes. You gain the following benefits while wielding a melee weapon using two hands (requiring either the two-handed property or being wielded with two hands if it has the versatile property):\n* You gain a +2 bonus to the damage roll of attacks made with the weapon.\n* Once on your turn, when you score a critical hit or reduce a creature to 0 hit points with the weapon, you can make one melee weapon attack as a part of the same action or reaction.\n* As a bonus action, you can unleash a sweeping strike around you with the weapon. All creatures within 5 feet of you must make a Dexterity saving throw, the DC equal to 8 + your attack bonus with that weapon. On a failed save, creatures take one damage roll from the weapon + your proficiency bonus in damage of the weapon's damage type."],
    ["Gunner [GUN] ❌",                 "Removed: Replaced by CloseQuarters Shooter and Loaded Arms Training",  "-",    "-"],
    ["Loaded Arm Training [LAT] ‼️",     "Replaces Crossbow Expert and Gunner",                                  "none", "You have a quick hand and keen eye when employing loaded weapons, granting you the following benefits:\n* Increase your Dexterity score by 1, to a maximum of 20.\n* You become proficient with all weapons that have the loading property if you are not already.\n* When wielding a weapon with the loading property, it is treated as having the Brutal property.\n* You ignore the loading property."],
    ["Mage Slayer [MaS] ⚠️",            "Errata for Mage Slayer",                                              "none", "You have practiced techniques useful in melee combat against spellcasters, gaining the following benefits:\n* When you see a creature within 5 feet of you casting a spell, you can use your reaction to make a melee weapon attack against that creature. When you take this reaction, you make the attack before the spell is finished casting.\n* When you use your reaction to make a melee weapon attack against a creature while they are casting a spell, that creature must make a concentration check. If that creature's concentration is broken, the spell fails.\n* When you damage a creature that is concentrating on a spell, that creature has disadvantage on the saving throw it makes to maintain its concentration.\n* You have advantage on saving throws against spells cast by creatures within 5 feet of you."],
    # ["", "", "", ""],
]

def getFeat(arguments):
    returnFeat = []
    for targetFeat in feats:
        if arguments.casefold() in targetFeat[0].casefold():
            returnFeat = targetFeat
    return returnFeat

def featList():
    returnList = []
    
    for targetFeat in feats:
        returnList.append(targetFeat[0])
    return returnList