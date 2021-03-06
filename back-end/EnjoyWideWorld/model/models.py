# This file includes all models i.e. database tables.
# ZHOU Kunpeng, 14 Dec 2018

from django.db import models

# 物品信息
class Item(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    name = models.CharField(max_length = 32, null = True)    # Name
    description = models.TextField(null = True)    # Description
    addExp = models.PositiveIntegerField(default = 0)   # 加经验值
    addHealth = models.PositiveIntegerField(default = 0) # 加生命值
    addAttack = models.PositiveIntegerField(default = 0) # 加攻击力
    addDefend = models.PositiveIntegerField(default = 0) # 加防御力
    addSpeed = models.PositiveIntegerField(default = 0) # 加速度
    addDodgeRate = models.PositiveIntegerField(default = 0) # 加闪避率

    def __str__(self):
        return "{0},{1}".format(self.id, self.name)

# 地点信息
class Position(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    name = models.CharField(max_length = 32, null = True)   # Position name
    longitude = models.DecimalField(max_digits = 20, decimal_places = 15) # 经度
    latitude = models.DecimalField(max_digits = 20, decimal_places = 15) # 纬度
    pictureAddr =  models.CharField(max_length = 256, null = True) # 地点图片地址
    description = models.TextField(default = "到此一游", null = True) # 地点简介

    # The item that the user obtains when checking in this position.
    itemLinked = models.ForeignKey(Item, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return "{0},{1}".format(self.id, self.name)

# 用户信息
class User(models.Model):
    wechatId = models.CharField(max_length = 32, primary_key = True) # 主键
    nickname = models.CharField(max_length = 32, default = '')
    avatarUrl = models.TextField(   \
        default = 'http://pic.51yuansu.com/pic3/cover/01/69/80/595f67bf2026f_610.jpg')
    province = models.CharField(max_length=32, default='', null=True)
    city = models.CharField(max_length=32, default='', null=True)



    totalLikes = models.PositiveIntegerField(default = 0)   # 获得的总赞数

    # default value of lon&lat is at the center of Tsinghua U
    lastLongitude = models.DecimalField(max_digits = 20, decimal_places = 15, default = 40.0) # 经度
    lastLatitude = models.DecimalField(max_digits = 20, decimal_places = 15, default = 116.3) # 纬度

    # Many-to-one field to Pet. Related name: pets

    # Many-to-may fields are linked to CheckInRecord
    checkInPositions = models.ManyToManyField(Position, through = "CheckInRecord")

    # Many-to-may fields are linked to LikeRecord
    # Related name: likes - beingLikeds
    likes = models.ManyToManyField('User', through = "LikeRecord")

    # Many-to-may fields are linked to BattleRecord
    # Related name: battleTargets - beingBattleds
    # Problem: conflict to likes. Ignore that
    # battleTargets = models.ManyToManyField('User', through = "BattleRecord")

    def __str__(self):
        return self.wechatId

# 宠物信息
class Pet(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID

    master = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'pets')  # 主人: Many-to-one for now

    name = models.CharField(max_length = 32)    # 昵称
    experience = models.PositiveIntegerField(default = 0) # 经验值

    appearanceId = models.PositiveIntegerField(default = 0) # 角色形象编号（由客户端编写者决定具体格式）

    health = models.PositiveIntegerField(default = 0) # 生命值
    attack = models.PositiveIntegerField(default = 0) # 攻击力
    defend = models.PositiveIntegerField(default = 0) # 防御力
    speed = models.PositiveIntegerField(default = 0) # 速度
    dodgeRate = models.PositiveIntegerField(default = 0) # 闪避率
    # updateTime = models.DateField(default = None) # 宠物最后一次修改时间

    def __str__(self):
        return "{0},{1}".format(self.id, self.name)


# 打卡信息
class CheckInRecord(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    point = models.ForeignKey(Position, on_delete = models.CASCADE)

    def __str__(self):
        return "{0}:({1}, {2})".format(self.id, self.user.wechatId, self.point.name)


# 点赞信息
class LikeRecord(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    userFrom = models.ForeignKey(User, on_delete = models.CASCADE)
    userTo = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "beingLikeds")

    def __str__(self):
        return "{0}:({1}, {2})".format(self.id, self.userFrom.wechatId, self.userTo.wechatId)

# 战斗信息
class BattleRecord(models.Model):
    id = models.AutoField(primary_key = True)  # Auto increment ID
    userFrom = models.ForeignKey(User, on_delete = models.CASCADE)
    userTo = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "beingBattleds")
    
    def __str__(self):
        return "{0}:({1}, {2})".format(self.id, self.userFrom.wechatId, self.userTo.wechatId)