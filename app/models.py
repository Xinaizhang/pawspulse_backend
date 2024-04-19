from django.db import models
from django.utils import timezone


# 用户模型
class User(models.Model):
    # 用户唯一标识
    userId = models.AutoField(primary_key=True)
    # 电话号码，唯一约束
    phoneNumber = models.CharField(max_length=15, unique=True, verbose_name="电话号码")
    # 邮箱地址，可为空，唯一约束
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, verbose_name="邮箱地址")
    # 用户昵称
    nickname = models.CharField(max_length=50, verbose_name="用户昵称")
    # 用户头像
    avatar = models.CharField(max_length=200, verbose_name="用户头像")
    # 地址
    address = models.CharField(max_length=255, verbose_name="地址")
    # 密码散列值
    passwordHash = models.CharField(max_length=128, verbose_name="密码散列值")
    # 账户创建日期，默认为当前时间
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="账户创建日期")


# 关注关系模型
class UserFollows(models.Model):
    # 关注关系的唯一标识
    followId = models.AutoField(primary_key=True)
    # 关注者ID
    followerId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name="关注者ID")
    # 被关注者ID
    followeeId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name="被关注者ID")


# 用户消息模型
class UserMessage(models.Model):
    # 用户消息的唯一标识
    messageId = models.AutoField(primary_key=True)
    # 接收者ID
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                                    verbose_name="接收者ID")
    # 发送者ID
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="发送者ID")
    # 消息内容
    messageContent = models.TextField(verbose_name="消息内容")
    # 发送时间
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="发送时间")


# 宠物模型
class Pet(models.Model):
    # 宠物唯一标识
    petId = models.AutoField(primary_key=True)
    # 关联的用户ID
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联的用户ID")
    # 宠物名字
    petName = models.CharField(max_length=50, verbose_name="宠物名字")
    # 类别（0-猫 1-狗 2-其他）
    petType = models.IntegerField(verbose_name="类别")
    # 品种
    speciesId = models.IntegerField(verbose_name="品种")
    # 性别（0-母 1-公 2-其他）
    sex = models.IntegerField(verbose_name="性别")
    # 年龄
    age = models.IntegerField(verbose_name="年龄")
    # 体重
    weight = models.FloatField(verbose_name="体重")
    # 宠物身份证二维码
    qrCode = models.CharField(max_length=255, unique=True, verbose_name="宠物身份证二维码")


# 宠物百科模型
class PetEncyclopedia(models.Model):
    # 品种唯一标识
    speciesId = models.AutoField(primary_key=True)
    # 类别（0-猫 1-狗 2-其他）
    petType = models.IntegerField(verbose_name="类别")
    # 品种名
    speciesName = models.CharField(max_length=255, verbose_name="品种名")
    # 特征
    characteristic = models.TextField(verbose_name="特征")
    # 护理建议
    careInstruction = models.TextField(verbose_name="护理建议")


# 宠物护理日记模型
class PetCareDiary(models.Model):
    # 护理日记唯一标识
    diaryId = models.AutoField(primary_key=True)
    # 关联的宠物ID
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="关联的宠物ID")
    # 日记内容
    content = models.TextField(verbose_name="日记内容")
    # 宠物体重
    weight = models.FloatField(verbose_name="宠物体重")


# 系统通知模型
class Notification(models.Model):
    # 系统通知的唯一标识
    notificationId = models.AutoField(primary_key=True)
    # 接收用户
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="接收用户")
    # 消息内容
    message = models.TextField(verbose_name="消息内容")


# 论坛帖子模型
class Post(models.Model):
    # 帖子的唯一标识符
    postId = models.AutoField(primary_key=True)
    # 发布人
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发布人")
    # 标题
    title = models.CharField(max_length=255, verbose_name="标题")
    # 正文
    content = models.TextField(verbose_name="正文")
    # 图片（最多6张）
    pictureUrl = models.JSONField(blank=True, null=True, verbose_name="图片")


# 互助模型
class Help(models.Model):
    # 互助帖子的唯一标识
    helpId = models.AutoField(primary_key=True)
    # 需要帮助的宠物ID
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="需要帮助的宠物ID")
    # 发布互助的用户
    requester_id = models.ForeignKey(User, related_name='help_requests', on_delete=models.CASCADE,
                                     verbose_name="发布互助的用户")
    # 提供帮助的用户
    provider_id = models.ForeignKey(User, related_name='help_provided', on_delete=models.CASCADE,
                                    verbose_name="提供帮助的用户")
    # 互助状态（0-待接取 1-进行中 2-已完成）
    status = models.IntegerField(default=0, verbose_name="互助状态")
    # 互助详情
    detail = models.TextField(verbose_name="互助详情")
    # 佣金
    cost = models.CharField(max_length=255, verbose_name="佣金")
