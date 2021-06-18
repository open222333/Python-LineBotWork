import random


class Role():
    """角色資訊 參數：角色名"""

    knightSkill = [
        ["重力斬", 1, 1, 2, 5, 20],
        ["神龍斬", 1, 1, 4, 10, 22],
        ["突擊刺", 1, 1, 8, 15, 25],
        ["地裂斬", 1, 1, 12, 20, 28],
        ["體能強化", 1, 1, 24, 25, 18],
        ["火龍巨斬", 1, 1, 57, 30, 9]
    ]

    fairySkill = [
        ["猛力射擊", 1, 1, 1, 5, 20],
        ["毒箭射擊", 1, 1, 2, 10, 22],
        ["雙重射擊", 1, 1, 6, 15, 25],
        ["精靈之力", 1, 1, 10, 20, 28],
        ["精靈之風", 1, 1, 18, 25, 18],
        ["風龍噴射", 1, 1, 43, 30, 9]
    ]

    magicSkill = [
        ["地獄火", 1, 1, 2, 8, 20],
        ["隕石術", 1, 1, 4, 16, 22],
        ["黑龍波", 1, 1, 8, 22, 25],
        ["賽爾波之光", 1, 1, 30, 20, 28],
        ["雷神之電", 1, 1, 24, 62, 18],
        ["水龍冰凍", 1, 1, 57, 98, 9]
    ]

    royalSkill = [
        ["增強防禦", 1, 3, 2, 6, 20],
        ["增強攻擊", 1, 3, 4, 4, 22],
        ["治癒術", 2, 2, 8, 1, 25],
        ["群體治癒術", 2, 2, 12, 5, 28],
        ["君主神威", 1, 1, 24, 20, 18],
        ["地龍尖刺", 1, 1, 57, 35, 9]
    ]

    positionSkill = {"騎士": knightSkill,
                     "妖精": fairySkill,
                     "法師": magicSkill,
                     "王族": royalSkill
                     }

    def __init__(self, RoleName):
        """設定角色名 參數：角色名"""
        self.roleAbilityValue = {"角色名": RoleName}

    def getRoleInfo(self):
        """取得角色資訊"""
        self.roleAbilityValue["職業"] = self.getPosition()[1]  # 加入職業
        self.roleAbilityValue.update(self.getRoleAbilityValue())  # 加入能力值
        self.roleAbilityValue["技能列表"] = self.getSkill(self.roleAbilityValue["職業"])
        return self.roleAbilityValue

    def getRoleAbilityValue(self):
        """取得角色能力值"""
        return AbilityValue().getAbilityValueInfo()

    def getPosition(self):
        """取得角色職位"""
        pList = []
        for i in self.positionSkill:
            pList.append(i)
        return Position(pList).getPositionInfo()

    def getSkill(self, position):
        """取得技能資訊"""
        skList = self.positionSkill[position]
        skillList = []
        for item in skList:
            skill = Skill(skillName=item[0], valueType=item[1],
                          skillType=item[2], value=item[3],
                          skillNeedMP=item[4], triggerRate=item[5]
                          )
            skillList.append(skill.getSkillInfo())
        return skillList


class Position():
    """職業資訊"""

    def __init__(self, positions: list):
        """ 參數為list 範例:["騎士","妖精","法師","王族"....]"""
        self.positionDict = {}
        for i, position in enumerate(positions, 1):
            self.positionDict[i] = position

    def getPositionInfo(self):
        """隨機取得職業 回傳List:[Pkey, PValues]"""
        Pkey = random.randint(1, len(self.positionDict))
        PValues = self.positionDict[Pkey]
        return [Pkey, PValues]


class AbilityValue():
    """角色能力值"""

    def getAbilityValueInfo(self, HPmin=200, HPmax=400, MPmin=100, MPmax=200):
        """取得能力值 回傳Dict"""
        AbilityValue = {
            "血量": self.setValue(HPmin, HPmax),
            "魔力": self.setValue(MPmin, MPmax),
            "攻擊": self.setValue(60, 100),
            "防禦": self.setValue(60, 100),
            "速度": self.setValue(60, 100),
            "迴避": self.setValue(60, 100),
            "運氣": self.setValue(60, 100),
        }
        return AbilityValue

    def setValue(self, min, max):
        """回傳整數隨機數"""
        return random.randint(min, max)


class Skill():
    """技能資訊"""

    def __init__(self, skillName: str, value: int, skillNeedMP: int, triggerRate: int, skillType=1, valueType=1):
        """skillName:技能名, value:效果數值, skillNeedMP:消耗MP,
        valueType:類型(1:數值(預設) 2:百分比),triggerRate:機率(1-100),
        skillType:類型(1:傷害(預設) 2:治癒 3:增幅)"""
        skillTypeDict = {1: "傷害", 2: "治癒", 3: "增幅"}
        valueTypeDict = {1: "數值", 2: "百分比"}
        self.skillInfo = {
            "技能名稱": skillName,
            "技能類型": skillTypeDict[skillType],
            "效果數值": value,
            "數值類型": valueTypeDict[valueType],
            "消耗魔力": skillNeedMP,
            "觸發機率": triggerRate,
        }

    def getSkillInfo(self):
        return self.skillInfo


class FightAction():
    """執行戰鬥動作 回傳戰鬥訊息"""

    def __init__(self, roleA, roleB):
        """角色名A, 角色名B"""
        self.roleA = Role(roleA)
        self.roleB = Role(roleB)

    def getDamageValues(self):
        """取得最終傷害數值"""
        pass

    def isFirstAttack(self):
        """是否先攻"""
        pass

    def isMiss(self, evade):
        """是否成功迴避"""
        return self.setRate(evade / 5)

    def isDouble(self, lucky):
        """是否爆擊"""
        return self.setRate(lucky / 10)

    def isSkillAttack(self, rate):
        """是否觸發技能"""
        return self.setRate(rate)

    def isHPZero(self, hp):
        """是否HP歸零"""
        if hp == 0 and hp < 0:
            return True
        else:
            return False

    def isMPZero(self, mp):
        """是否MP歸零"""
        if mp == 0 and mp < 0:
            return True
        else:
            return False

    def setRate(self, rateNum):
        """輸入整數 觸發機率 rateNum %"""
        point = random.randint(1, 100)
        if point > rateNum:
            return False
        else:
            return True
