from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import models
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImagemapArea, ImagemapSendMessage, URIImagemapAction, BaseSize, messages
from linebot import LineBotApi, WebhookParser
from linebot.models.imagemap import MessageImagemapAction
from .models import LineUser, Group, Association, FightData
import os
from .fightname import FightAction
import uuid


basePath = os.path.abspath(os.path.dirname(__name__))
# 套用settings.py 的屬性
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECERT)

image_url = 'https://www.moneypoker.cc/static/images/QQQ-3.png?'
click_link_1 = "https://drive.google.com/file/d/1U3qbnO-TAh08neC8DtveOM9mSw7Gu9f1/view?usp=sharing"

commandAdmin = {
    "A0000": "設置管理員",
    "A0001": "查詢所有餘額",
    "A9999": "測試用指令",
}

commandMember = {
    "C0000": "查看權限等級",
    "C0001": "查詢群組ID",
    "C0002": "查詢用戶ID",
    "C0003": "查詢餘額",
    "C0004": "下載連結",
    "C0005": "查看可用指令",
    "C0006": "建立對戰",
    "C0007": "加入對戰",
    "C0008": "取得對戰紀錄",
}


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
    for event in events:
        if isinstance(event, MessageEvent):  # 如果有訊息事件
            # 會員資料庫
            if isInLineUserData(event.source.user_id) is False:
                addUserData(event)
            # 群組資料庫
            if isInGroupData(event.source.group_id) is False:
                addGroupData(event)
            # 關聯表資料庫
            if isInAssociationData(event.source.user_id, event.source.group_id) is False:
                addAssociationData(event)
            # 判斷是否管理員權限 設定指令列表
            command = str(event.message.text).split(":")[0]
            if command in setUserCommandList(commandAdmin, commandMember):
                if command in setUserCommandList(commandAdmin) and not isAdministrator(event):
                    returnText = "ID:%s\n沒有管理者權限" % event.source.user_id
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=returnText)
                    )
                else:
                    if command == commandAdmin["A0000"]:
                        setAdminUser(event)
                    elif command == commandAdmin["A0001"]:
                        getAllUserAmount(event)
                    elif command == commandAdmin["A9999"]:
                        pass
                    elif command == commandMember["C0000"]:
                        getUserPermissions(event)
                    elif command == commandMember["C0001"]:
                        getGroupID(event)
                    elif command == commandMember["C0002"]:
                        getLineUserID(event)
                    elif command == commandMember["C0003"]:
                        getUserAmount(event)
                    elif command == commandMember["C0004"]:
                        getDownloadLink(event)
                    elif command == commandMember["C0005"]:
                        getUsefulCommand(event)
                    elif command == commandMember["C0006"]:
                        getFightID(event)
                    elif command == commandMember["C0007"]:
                        getStartFight(event)
            else:
                pass
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def isAdministrator(event):
    '''檢查是否管理員'''
    userPMdict = LineUser.objects.filter(
        lineID=event.source.user_id).values('userPermissions').get()
    if userPMdict['userPermissions'] == 100:
        return True
    else:
        return False


def isInLineUserData(userId):
    '''檢查lineID是否存在LineUser'''
    return LineUser.objects.filter(lineID=userId).exists()


def isInGroupData(groupId):
    '''檢查groupID是否存在Group'''
    return Group.objects.filter(groupID=groupId).exists()


def isInAssociationData(userId, groupId):
    '''檢查AssociationData是否存在'''
    lineIDExists = Association.objects.filter(
        lineID=userId).exists()
    groupIDExists = Association.objects.filter(
        groupID=groupId).exists()
    return (lineIDExists and groupIDExists)


def isUserInGroup(userId, groupId):
    '''檢查userId在AssociationData是否有匹配groupId'''
    return Association.objects.filter(lineID=userId, groupID=groupId).exists()


def addUserData(event):
    '''添加使用者至資料表 LineUser'''
    userLineId = event.source.user_id
    addDataTemp = LineUser(
        lineID=userLineId,
        userLevel=0,
        userAmount=0,
        userPermissions=0
    )
    addDataTemp.save()


def addGroupData(event):
    '''添加群組ID至資料表 Group'''
    userGroupId = event.source.group_id
    addDataTemp = Group(groupID=userGroupId)
    addDataTemp.save()


def addAssociationData(event):
    '''建立在關聯表 Association'''
    userLineId = event.source.user_id
    userGroupId = event.source.group_id
    addAssociationDataTemp = Association(
        lineID=userLineId,
        groupID=userGroupId
    )
    addAssociationDataTemp.save()


def setUserCommandList(*args: dict):
    '''設置指令列表'''
    commandList = []
    for arg in args:
        for command in arg.values():
            commandList.append(command)
    return commandList


def setUserPermissions(event, lineID):
    '''設置會員權限'''
    if isAdministrator(event):
        if isInLineUserData(lineID):
            LineUser.objects.filter(lineID=lineID).update(userPermissions=100)
            returnText = "ID:%s,已添加管理者權限" % event.source.user_id
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=returnText)
            )
        else:
            returnText = "ID不在資料庫內"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=returnText)
            )
    else:
        returnText = "ID:%s,沒有管理者權限" % event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=returnText)
        )


def setAdminUser(event):
    """根據ID設置管理員"""
    userList = getCommandArgument(event.message.text)
    if userList[0] == commandAdmin["A0000"]:
        message = "請依照以下格式輸入指令\n%s:Line ID" % commandAdmin["A0000"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    else:
        setUserPermissions(event, userList[0])


def getCommandList(*args):
    '''取得目前可用指令'''
    flag = len(args)
    commandList = ''
    for arg in args:
        commandDict = dict(arg)
        count = 1  # 換行計數
        for commandCode in commandDict:
            if count == len(commandDict):
                commandList += "%s" % (commandDict[commandCode])
            else:
                commandList += "%s\n" % (commandDict[commandCode])
                count += 1
        flag -= 1
        # 兩個指令字典間的換行
        if flag != 0:
            commandList += "\n"
        else:
            pass
    return commandList


def getGroupID(event):
    '''取得使用者的目前群組ID'''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="此群組ID：" + event.source.group_id),
    )


def getLineUserID(event):
    '''取得使用者的LineID'''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="你的用戶ID：" + event.source.user_id),
    )


def getUserAmount(event):
    '''根據LineID取得餘額'''
    UserlineID = event.source.user_id
    UserAmount = LineUser.objects.filter(
        lineID=UserlineID).values_list('userAmount')
    textGetAmount = "目前餘額\n%s : %s\n" % (UserlineID, str(UserAmount[0][0]))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textGetAmount)
    )


def getUserPermissions(event):
    '''查看LineID角色'''
    UserlineID = event.source.user_id
    userPMdict = LineUser.objects.filter(
        lineID=UserlineID).values('userPermissions').get()
    textGetAmount = "%s : %s\n" % (
        UserlineID, str(userPMdict["userPermissions"]))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textGetAmount)
    )


def getAllUserAmount(event):
    '''取得所有使用者的LineID以及餘額'''
    lineIDQuerySet = LineUser.objects.all()
    textGetAmount = ''
    for UserlineID, UserAmount in lineIDQuerySet.values_list('lineID', 'userAmount'):
        if UserlineID:
            textGetAmount += "%s : %s\n" % (UserlineID, str(UserAmount))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textGetAmount)
    )


def getDownloadLink(event):
    '''取得圖片 左半邊是回覆文字訊息 右半開啟連結'''
    line_bot_api.reply_message(
        event.reply_token,
        ImagemapSendMessage(
            base_url=image_url,
            alt_text='下載測試',
            base_size=BaseSize(height=372, width=1102),
            actions=[
                MessageImagemapAction(
                    text='測試回覆：無設定資源',
                    area=ImagemapArea(
                        x=0, y=0, width=551, height=186
                    )
                ),
                URIImagemapAction(
                    link_uri=click_link_1,
                    area=ImagemapArea(
                        x=551, y=0, width=551, height=186
                    )
                )
            ]
        )
    )


def getCommandArgument(commandText):
    """將指令內的參數內容 以串列返回"""
    commandList = str(commandText).split(":")
    if len(commandList) == 1:
        return commandList
    else:
        argumentList = str(commandList[1]).split(",")
        return argumentList


def getUsefulCommand(event):
    """取得可用指令"""
    if isAdministrator(event):
        returnText = "你目前可用指令：\n" + \
            getCommandList(commandAdmin, commandMember)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=returnText)
        )
    else:
        returnText = "你目前可用指令：\n" + \
            getCommandList(commandMember)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=returnText)
        )


# 以下為戰場小遊戲使用
def getFightID(event):
    """建立對戰資料庫並回傳戰場ID"""
    roleName = getCommandArgument(event.message.text)
    if roleName[0] == commandMember["C0006"]:
        message = "請依照以下格式輸入指令\n\n%s:角色名" % commandMember["C0006"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    else:
        inviteId = uuid.uuid4()
        creatorLineId = event.source.user_id
        addDataTemp = FightData(
            creatorUserId=creatorLineId,
            creatorRoleName=roleName[0],
            fightID=inviteId
        )
        addDataTemp.save()
        message = "此次戰場ID:%s\n另一位參戰者請輸入以下指令\n\n加入對戰:角色名,%s" % (
            inviteId, inviteId)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )


def joinFight(event):
    """根據戰場ID加入對戰資料庫"""
    argumentList = getCommandArgument(event.message.text)
    if len(argumentList) < 2:
        message = "請依照以下格式輸入指令\n%s:角色名,戰場ID" % commandMember["C0007"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    elif FightData.objects.filter(fightID=argumentList[1]).exists():
        fightQueryset = FightData.objects.filter(fightID=argumentList[1])
        participantUserId = event.source.user_id
        fightQueryset.update(
            participantUserId=participantUserId,
            participantRoleName=argumentList[0]
        )
    else:
        message = "查無此戰場ID : %s" % argumentList[1]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )


def isFightIDExists(fightId):
    """判斷戰場ID是否存在"""
    querySet = FightData.objects.filter(fightID=fightId)
    return querySet.exists()


def isFinishGame(fightId):
    """判斷是否為完成的戰場"""
    querySet = FightData.objects.filter(fightID=fightId).values("fightState")
    if querySet[0]["fightState"] == "Undone":
        return False
    elif querySet[0]["fightState"] == "Finish":
        return True


def startFight(event, fightId):
    """開始戰鬥 可逐一發送消息 使用Push可能需要費用"""
    fightDetailText = ''
    fightDetailList = []
    fightQuerySet = FightData.objects.filter(fightID=fightId)
    creatorRoleName = fightQuerySet.values_list('creatorRoleName')
    participantRoleName = fightQuerySet.values_list('participantRoleName')
    fight = FightAction(creatorRoleName[0][0], participantRoleName[0][0])
    fightDetailList.append(fight.getRoleInfoList(fight.roleA_Info) + "\n\n")
    fightDetailList.append(fight.getRoleInfoList(fight.roleB_Info) + "\n")
    while True:
        if fight.firstAttack:
            fightDetailList.append(fight.attackActionAB() + "\n")
            if fight.isAnyHPZero():
                for detail in fightDetailList:
                    line_bot_api.push_message(
                        event.source.group_id,
                        TextSendMessage(text=detail)
                    )
                break
            fightDetailList.append(fight.attackActionBA() + "\n")
        else:
            fightDetailList.append(fight.attackActionBA() + "\n")
            if fight.isAnyHPZero():
                for detail in fightDetailList:
                    line_bot_api.push_message(
                        event.source.group_id,
                        TextSendMessage(text=detail)
                    )
                break
            fightDetailList.append(fight.attackActionAB() + "\n")
        if fight.isAnyHPZero():
            for detail in fightDetailList:
                line_bot_api.push_message(
                    event.source.group_id,
                    TextSendMessage(text=detail)
                )
            break
        for detail in fightDetailList:
            fightDetailText += detail
        FightData.objects.filter(fightID=fightId).update(
            fightDetial=fightDetailText, fightState="Finish")


def startFight2(event, fightId):
    """開始戰鬥 使用reply直接發送結果"""
    fightMessageText = ''
    fightQuerySet = FightData.objects.filter(fightID=fightId)
    creatorRoleName = fightQuerySet.values_list('creatorRoleName')
    participantRoleName = fightQuerySet.values_list('participantRoleName')
    fight = FightAction(creatorRoleName[0][0], participantRoleName[0][0])
    fightMessageText += fight.getRoleInfoList(fight.roleA_Info) + "\n\n"
    fightMessageText += fight.getRoleInfoList(fight.roleB_Info) + "\n\n"
    while True:
        if fight.firstAttack:
            # True則A先攻
            fightMessageText += fight.attackActionAB() + "\n"
            if fight.isAnyHPZero():
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=fightMessageText)
                )
                break
            fightMessageText += fight.attackActionBA() + "\n"
        else:
            fightMessageText += fight.attackActionBA() + "\n"
        if fight.isAnyHPZero():
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=fightMessageText)
            )
            break
        fightMessageText += fight.attackActionAB() + "\n"
        if fight.isAnyHPZero():
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=fightMessageText)
            )
            break
    FightData.objects.filter(fightID=fightId).update(
        fightDetial=fightMessageText, fightState="Finish")


def getStartFight(event):
    """開始戰鬥"""
    argumentList = getCommandArgument(event.message.text)
    if isFightIDExists(argumentList[1]):
        if isFinishGame(argumentList[1]):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="此戰場已結束。")
            )
        else:
            joinFight(event)
            startFight2(event, argumentList[1])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此戰場ID不存在。")
        )
