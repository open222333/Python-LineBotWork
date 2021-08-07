# 取得角色資料(戰鬥)
class RoleInfo():
    """角色資訊"""

    def __init__(self, roleAP: dict):
        """輸入能力值字典"""
        self.roleAP = roleAP
        self.job = self.roleAP["職業"]
        # self.emquirement = emquirement # 裝備數值

    def setVitAddExtraHP(self):
        """體質增加的HP"""
        hp = 0
        if self.job == "騎士":
            hp = self.roleAP["Vit"] * 3
        elif self.job == "妖精":
            hp = self.roleAP["Vit"] * 1
        elif self.job == "法師":
            hp = self.roleAP["Vit"] * 1
        elif self.job == "王族":
            hp = self.roleAP["Vit"] * 2
        return hp

    def setSpiAddExtraMP(self):
        """精神增加的MP"""
        mp = 0
        if self.job == "騎士":
            mp = self.roleAP["Spi"] * 1
        elif self.job == "妖精":
            mp = self.roleAP["Spi"] * 2
        elif self.job == "法師":
            mp = self.roleAP["Spi"] * 3
        elif self.job == "王族":
            mp = self.roleAP["Spi"] * 1
        return mp

    def getRoleInfo(self):
        """取得基本資訊"""
        self.roleAP.update(self.setAtkInfo())
        self.roleAP.update(self.setDefInfo())
        self.roleAP.update(self.setCritInfo())
        self.roleAP["HP"] += self.setVitAddExtraHP()
        self.roleAP["MP"] += self.setSpiAddExtraMP()
        return self.roleAP

    def setAtkInfo(self):
        """設置傷害值"""
        defaultAtk = 0  # 初始值
        try:
            if self.job == "騎士":
                defaultAtk += (self.roleAP["Str"]/4)
            elif self.job == "妖精":
                defaultAtk += (self.roleAP["Dex"]/4)
            elif self.job == "法師":
                defaultAtk += (self.roleAP["Str"]/5) + (self.roleAP["Spi"]/4)
            elif self.job == "王族":
                defaultAtk += (self.roleAP["Str"]/5) + (self.roleAP["Spi"]/6)
        except Exception:
            "攻擊力設置"
        return {"攻擊力": round(defaultAtk)}

    def setDefInfo(self):
        """設置防禦值"""
        defaultDef = 0  # 初始值
        try:
            if self.job == "騎士":
                defaultDef += (self.roleAP["Dex"]/3)
            elif self.job == "妖精":
                defaultDef += (self.roleAP["Dex"]/5)
            elif self.job == "法師":
                defaultDef += (self.roleAP["Dex"]/3)
            elif self.job == "王族":
                defaultDef += (self.roleAP["Dex"]/2)
        except Exception:
            "防禦值設置"
        return {"防禦值": round(defaultDef)}

    def setCritInfo(self):
        """設置爆擊率"""
        defaultCrit = 0  # 初始值
        try:
            if self.job == "騎士":
                defaultCrit += (self.roleAP["Str"]/180)
            elif self.job == "妖精":
                defaultCrit += (self.roleAP["Dex"]/180)
            elif self.job == "法師":
                defaultCrit
            elif self.job == "王族":
                defaultCrit += (self.roleAP["Str"]/230)
        except Exception:
            "爆擊率設置"
        return {"爆擊率": round(defaultCrit)}

    def getSkillList(self):
        pass
