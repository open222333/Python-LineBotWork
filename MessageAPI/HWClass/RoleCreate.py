import random

# 創建角色流程


class CreateRole():
    def __init__(self, roleName, job) -> None:
        self.roleName = roleName
        self.job = job

    def createRole(self):
        roleDict = {
            "角色名": self.roleName,
            "職業": self.job,
        }
        roleDict.update(CreateAbilityPoint(self.job).setDefaultAP())
        return roleDict


class CreateAbilityPoint():
    def __init__(self, job):
        self.job = job
        self.AP = {}

    def setDefaultAP(self):
        """設置職業創建的能力初始值"""
        try:
            # 正式用
            # if self.job == "騎士":
            #     self.AP = {"HP": 120, "MP": 30, "Str": 20,
            #             "Dex": 8, "Vit": 10, "Spi": 2}
            # elif self.job == "妖精":
            #     self.AP = {"HP": 80, "MP": 60, "Str": 8,
            #             "Dex": 20, "Vit": 2, "Spi": 5}
            # elif self.job == "法師":
            #     self.AP = {"HP": 60, "MP": 120, "Str": 8,
            #             "Dex": 5, "Vit": 8, "Spi": 24}
            # elif self.job == "王族":
            #     self.AP = {"HP": 100, "MP": 50, "Str": 15,
            #             "Dex": 5, "Vit": 8, "Spi": 8}
            ###############################################
            # 測試用
            if self.job == "騎士":
                self.AP = {"HP": 400, "MP": 400, "Str": random.randint(300, 400),
                           "Dex": random.randint(300, 400), "Vit": random.randint(300, 400), "Spi": random.randint(300, 400)}
            elif self.job == "妖精":
                self.AP = {"HP": random.randint(300, 400), "MP": random.randint(300, 400), "Str": random.randint(300, 400),
                           "Dex": random.randint(300, 400), "Vit": random.randint(300, 400), "Spi": random.randint(300, 400)}
            elif self.job == "法師":
                self.AP = {"HP": random.randint(300, 400), "MP": random.randint(300, 400), "Str": random.randint(300, 400),
                           "Dex": random.randint(300, 400), "Vit": random.randint(300, 400), "Spi": random.randint(300, 400)}
            elif self.job == "王族":
                self.AP = {"HP": random.randint(300, 400), "MP": random.randint(300, 400), "Str": random.randint(300, 400),
                           "Dex": random.randint(300, 400), "Vit": random.randint(300, 400), "Spi": random.randint(300, 400)}
        except TypeError:
            "參數內職業不存在"
        return self.AP
