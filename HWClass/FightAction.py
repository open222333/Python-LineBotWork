from RoleInfo import RoleInfo
import random

# 戰鬥流程


class FightRole():
    """戰鬥判斷"""

    def __init__(self, role: dict):
        """所有能力值"""
        self.role = RoleInfo(role).getRoleInfo()
        self.MP = self.role["MP"]

    def whoFirst(self):
        """先攻"""
        point = random.randint(1, 100)
        if point >= 50:
            return True
        else:
            return False

    def getSkillActivate(self, skilllist):
        """判斷技能是否發動 若MP足夠發動MP消耗最大"""
        activateSkill = []
        for skill in skilllist:
            if self.setRate(skill["技能觸發機率"]):
                if self.MP >= skill["技能消耗MP"]:
                    if len(activateSkill) == 0:
                        activateSkill.append(skill)
                    else:
                        activateSkill[0] = skill
        if len(activateSkill) == 1:
            return activateSkill[0]
        else:
            return None

    def isHPZero(self):
        """判斷HP是否為0"""
        if self.role["HP"] == 0:
            return True
        else:
            return False

    def setAtk(self):
        """傷害值"""
        AtkValue = 0  # 初始值
        try:
            if self.role["職業"] == "騎士":
                AtkValue += (self.role["Str"]/4)
            elif self.role["職業"] == "妖精":
                AtkValue += (self.role["Dex"]/4)
            elif self.role["職業"] == "法師":
                AtkValue += (self.role["Str"]/5) + (self.role["Spi"]/4)
            elif self.role["職業"] == "王族":
                AtkValue += (self.role["Str"]/5) + (self.role["Spi"]/6)
        except Exception:
            "攻擊力"
        return round(AtkValue)

    def setDef(self):
        """防禦值"""
        DefValue = 0  # 初始值
        try:
            if self.role["職業"] == "騎士":
                DefValue += (self.role["Dex"]/3)
            elif self.role["職業"] == "妖精":
                DefValue += (self.role["Dex"]/5)
            elif self.role["職業"] == "法師":
                DefValue += (self.role["Dex"]/3)
            elif self.role["職業"] == "王族":
                DefValue += (self.role["Dex"]/2)
        except Exception:
            "防禦值"
        return round(DefValue)

    def setCrit(self):
        """設置爆擊率"""
        CritValue = 0  # 初始值
        try:
            if self.role["職業"] == "騎士":
                CritValue += (self.role["Str"]/180)
            elif self.role["職業"] == "妖精":
                CritValue += (self.role["Dex"]/180)
            elif self.role["職業"] == "法師":
                CritValue
            elif self.role["職業"] == "王族":
                CritValue += (self.role["Str"]/230)
        except Exception:
            "爆擊率設置"
        return CritValue

    def setRate(self, rate):
        """機率"""
        point = random.randint(1, 100)
        if point <= rate:
            return True
        else:
            return False


class FightMessage():
    def __init__(self) -> None:
        pass
        # self.roleA = FightRole(rolaA)
        # self.roleB = FightRole(roleB)

    def getAttackMessage(self, attack, attackSkill, defence):
        text = ""
        attack = FightRole(attack)
        defence = FightRole(defence)
        attackName = attack.role["角色名"]
        defenceName = defence.role["角色名"]
        defValue = round(defence.setDef() / 2)
        activateSkill = attack.getSkillActivate(attackSkill)
        if activateSkill == None:
            damage = attack.setAtk()
            message = f"{attackName} 發動攻擊，攻擊力為{damage}\n"
        else:
            skillName = activateSkill["技能名"]
            skillType = activateSkill["技能類型"]
            skillValue = activateSkill["技能數值"]
            skillValueType = activateSkill["技能數值類型"]
            skillMP = activateSkill["技能消耗MP"]
            if skillType == "傷害":
                if skillValueType == "數值":
                    damage = attack.setAtk() + skillValue
                    message = f"{attackName} 發動技能 {skillName}，消耗 {skillMP} MP，攻擊力為{damage}\n"
                elif skillValueType == "百分比":
                    damage = round(attack.setAtk()
                                   * (1 + (skillValue / 100)))
                    message = f"{attackName} 發動技能 {skillName}，消耗 {skillMP} MP，攻擊力為{damage}\n"
            else:
                pass
        if attack.setRate(attack.setCrit()):
            damage = round(damage * 1.2)
            message += "爆擊! "
        defence.role["HP"] -= (damage - defValue)
        defHP = defence.role["HP"]
        text += message + f"造成傷害{(damage - defValue)}，{defenceName} HP剩餘{defHP}"
        return text
