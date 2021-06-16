from MessageAPI.fightname import FightAction
# 以下為測試用程式碼
test = FightAction("角色A", "角色B")
print(test.getRoleInfoList(test.roleA_Info))
print(test.getRoleInfoList(test.roleB_Info))
while True:
    if test.firstAttack:
        # True則A先攻
        print(test.attackActionAB())
        if test.isAnyHPZero():
            break
        print(test.attackActionBA())
    else:
        print(test.attackActionBA())
        if test.isAnyHPZero():
            break
        print(test.attackActionAB())
    if test.isAnyHPZero():
        break
