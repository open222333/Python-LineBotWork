from django.db import models
import uuid


class LineUser(models.Model):
    lineID = models.TextField()
    userLevel = models.IntegerField()
    userAmount = models.FloatField()
    userPermissionsTuple = [
        (100, 'Admin'), (30, 'Common Member'), (0, 'New Member')]
    userPermissions = models.IntegerField(choices=userPermissionsTuple)
    createDate = models.DateTimeField()


class Group(models.Model):
    groupID = models.TextField()
    createDate = models.DateTimeField()


class Association(models.Model):
    lineID = models.TextField()
    groupID = models.TextField()


class RoleData(models.Model):
    RoleID = models.UUIDField(default=uuid.uuid4, primary_key=True)  # 角色ID
    creatorLineId = models.TextField()  # 創建角色的LineID
    RoleName = models.TextField()  # 角色名
    RoleLevel = models.IntegerField()  # 角色等級
    RoleExp = models.IntegerField()  # 角色經驗
    RoleTolExp = models.BigIntegerField()  # 角色總經驗
    JobID = models.ForeignKey("Job", on_delete=models.DO_NOTHING)  # 角色職業ID
    FriendListID = models.BigIntegerField()  # 好友名單ID
    GuildID = models.BigIntegerField()  # 公會ID
    EquipmentID = models.BigIntegerField()  # 裝備ID
    RoleCreateDateTime = models.DateTimeField()  # 創建日期
    HP = models.IntegerField()  # 血量
    MP = models.IntegerField()  # 魔力
    Str = models.IntegerField()  # 力
    Dex = models.IntegerField()  # 敏
    Vit = models.IntegerField()  # 體
    Spi = models.IntegerField()  # 精
    JusticeValue = models.IntegerField()  # 正義值


class Job(models.Model):
    JobID = models.AutoField(primary_key=True)  # 職業ID
    JobName = models.TextField()  # 職業名
    JobDetial = models.TextField()  # 職業敘述


class Skill(models.Model):
    JobID = models.ForeignKey("Job", on_delete=models.CASCADE)
    SkillName = models.TextField()  # 技能名
    SkillType = models.TextChoices("SkillType", "傷害 輔助")  # 技能類型
    SkillOnAP = models.TextField()  # 技能類型輔助時 作用的屬性
    SkillValue = models.IntegerField()  # 技能數值
    SkillValueType = models.TextChoices("SkillValueType", "數值 百分比")  # 技能數值類型
    SkillMP = models.IntegerField()  # 技能消耗MP
    SkillDetial = models.TextField()  # 技能文字敘述


class Level(models.Model):
    Level = models.IntegerField()  # 等級
    NextLVReqExp = models.IntegerField()  # 升級所需經驗值
    TotalExp = models.BigIntegerField()  # 總經驗值
