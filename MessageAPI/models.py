from django.db import models


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


class FightData(models.Model):
    creatorUserId = models.TextField()
    creatorRoleName = models.TextField()
    participantUserId = models.TextField()
    participantRoleName = models.TextField()
    fightID = models.TextField()
    fightingCreateDateTime = models.DateTimeField()
    fightDetial = models.TextField()
    fightState = models.CharField(max_length=10, default="Undone")
