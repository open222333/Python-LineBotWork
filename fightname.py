import random


class FightRole():

    def __init__(self, RoleName):
        """帶入角色名"""
        self.roleNameAbilityValue = {
            "角色名": RoleName,
            "血量": setRandomValue(200, 400),
            "攻擊": setRandomValue(60, 100),
            "防禦": setRandomValue(60, 100),
            "速度": setRandomValue(60, 100),
            "迴避": setRandomValue(60, 100),
            "運氣": setRandomValue(60, 100),
        }

    def getRoleAbilityValue(self):
        """取得角色能力值"""
        return self.roleNameAbilityValue


class FightAction():

    def __init__(self, roleA, roleB):
        self.roleA = FightRole(roleA)
        self.roleB = FightRole(roleB)
        self.roleA_Info = self.roleA.getRoleAbilityValue()
        self.roleB_Info = self.roleB.getRoleAbilityValue()
        self.firstAttack = whichFirst(
            self.roleA_Info["速度"], self.roleB_Info["速度"])
        self.roleA_criticalRate = getCriticalRate(self.roleA_Info["運氣"])
        self.roleB_criticalRate = getCriticalRate(self.roleB_Info["運氣"])
        self.roleA_agility = getAgility(self.roleA_Info["迴避"])
        self.roleB_agility = getAgility(self.roleB_Info["迴避"])

    def attackActionAB(self):
        """攻擊動作 A攻擊B"""
        if isMiss(self.roleB_Info["迴避"]):
            format = (self.roleA_Info["角色名"], self.roleB_Info["角色名"])
            fightMessage = '%s進行攻擊，%s迴避了！沒受到傷害。' % format
        elif isDoubleDamage(self.roleA_Info["運氣"]):
            damage = getDoubleDamage(
                self.roleA_Info["攻擊"], self.roleB_Info["防禦"])
            resultHP = isHPUnderZero(self.roleB_Info["血量"] - damage)
            self.roleB_Info["血量"] = resultHP
            format = (self.roleA_Info["角色名"],
                      self.roleB_Info["角色名"],
                      damage,
                      self.roleB_Info["角色名"],
                      resultHP)
            fightMessage = '%s使出爆擊，%s受到%d傷害，%s剩餘HP:%d。' % format
            if resultHP == 0:
                fightMessage += '\n%s 獲勝了～' % self.roleA_Info["角色名"]
        else:
            damage = getDamage(self.roleA_Info["攻擊"], self.roleB_Info["防禦"])
            resultHP = isHPUnderZero(self.roleB_Info["血量"] - damage)
            self.roleB_Info["血量"] = resultHP
            format = (self.roleA_Info["角色名"],
                      self.roleB_Info["角色名"],
                      damage,
                      self.roleB_Info["角色名"],
                      resultHP)
            fightMessage = '%s進行攻擊，%s受到%d傷害，%s剩餘HP:%d。' % format
            if resultHP == 0:
                fightMessage += '\n%s 獲勝了～' % self.roleA_Info["角色名"]
        return fightMessage

    def attackActionBA(self):
        """攻擊動作 B攻擊A"""
        if isMiss(self.roleA_Info["迴避"]):
            format = (self.roleB_Info["角色名"], self.roleA_Info["角色名"])
            fightMessage = '%s進行攻擊，%s迴避了！沒受到傷害。' % format
        elif isDoubleDamage(self.roleB_Info["運氣"]):
            damage = getDoubleDamage(
                self.roleB_Info["攻擊"], self.roleA_Info["防禦"])
            resultHP = isHPUnderZero(self.roleA_Info["血量"] - damage)
            self.roleA_Info["血量"] = resultHP
            format = (self.roleB_Info["角色名"],
                      self.roleA_Info["角色名"],
                      damage,
                      self.roleA_Info["角色名"],
                      resultHP)
            fightMessage = '%s使出爆擊，%s受到%d傷害，%s剩餘HP:%d。' % format
            if resultHP == 0:
                fightMessage += '\n%s 獲勝了～' % self.roleB_Info["角色名"]
        else:
            damage = getDamage(self.roleB_Info["攻擊"], self.roleA_Info["防禦"])
            resultHP = isHPUnderZero(self.roleA_Info["血量"] - damage)
            self.roleA_Info["血量"] = resultHP
            format = (self.roleB_Info["角色名"],
                      self.roleA_Info["角色名"],
                      damage,
                      self.roleA_Info["角色名"],
                      resultHP)
            fightMessage = '%s進行攻擊，%s受到%d傷害，%s剩餘HP:%d。' % format
            if resultHP == 0:
                fightMessage += '\n%s 獲勝了～' % self.roleB_Info["角色名"]
        return fightMessage

    def getRoleInfoList(self, roleInfo: dict):
        """列出角色能力值"""
        infoText = ''
        count = 1
        for info in roleInfo:
            infoFormat = (info, roleInfo[info])
            if len(roleInfo) == count:
                infoText += "%s: %s" % infoFormat
            else:
                infoText += "%s: %s\n" % infoFormat
                count += 1
        return infoText

    def isAnyHPZero(self):
        """是否有角色血量為零"""
        if self.roleA_Info["血量"] == 0 or self.roleB_Info["血量"] == 0:
            return True
        else:
            return False


def setRandomValue(min, max):
    """輸出整數亂數"""
    return random.randrange(min, max)


def isHPUnderZero(hp):
    """若數值小於零,則回傳0 若大於零則直接回傳"""
    if hp <= 0:
        return hp == 0
    else:
        return hp


def isDoubleDamage(lucky):
    """判斷是否爆擊"""
    point = setRandomValue(0, 1000)
    if point > lucky:
        return False
    else:
        return True


def isMiss(evade):
    """判斷是否迴避"""
    point = setRandomValue(0, 1000)
    if point > evade * 2:
        return False
    else:
        return True


def isVictory(roleAHP, roleBHP):
    """根據血量判斷勝利"""
    if roleAHP == 0:
        return True
    elif roleBHP == 0:
        return False
    else:
        return None


def getDamage(attack, defence):
    """取得普通攻擊傷害值"""
    return int((attack - (defence / 2)) * random.uniform(1.0, 1.5))


def getDoubleDamage(attack, defence):
    """取得爆擊攻擊傷害值"""
    return int((attack - (defence / 2)) * random.uniform(3.0, 5.0))


def getCriticalRate(lucky):
    """取得爆擊率 """
    return lucky/1000


def getAgility(evade):
    """取得迴避率"""
    return evade/1000


def whichFirst(roleASpeed, roleBSpeed):
    """根據速度決定先攻後攻"""
    if roleASpeed > roleBSpeed:
        return True
    elif roleBSpeed > roleASpeed:
        return False
    else:
        if random.random() > 0.49:
            return True
        else:
            return False
