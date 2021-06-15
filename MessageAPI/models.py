from django.db import models


class LineUser(models.Model):
    lineID = models.TextField()
    userLevel = models.IntegerField()
    userAmount = models.FloatField()
    userPermissionsTuple = [
        (100, 'Admin'), (30, 'Common Member'), (0, 'New Member')]
    userPermissions = models.IntegerField(choices=userPermissionsTuple)
    createDate = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    groupID = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)


class Association(models.Model):
    lineID = models.TextField()
    groupID = models.TextField()
