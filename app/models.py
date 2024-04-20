from django.db import models
from django.utils import timezone


# 用户模型
class user(models.Model):
    # 用户唯一标识
    user_id = models.AutoField(primary_key=True)
    # 电话号码，唯一约束
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="电话号码")
    # 邮箱地址，可为空，唯一约束
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, verbose_name="邮箱地址")
    # 用户昵称
    nickname = models.CharField(max_length=50, verbose_name="用户昵称")
    # 用户头像
    avatar = models.CharField(max_length=200, verbose_name="用户头像")
    # 地址
    address = models.CharField(max_length=255, verbose_name="地址")
    # 密码散列值
    password_hash = models.CharField(max_length=128, verbose_name="密码散列值")
    # 账户创建日期，默认为当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="账户创建日期")


# 关注关系模型
class user_follows(models.Model):
    # 关注关系的唯一标识
    follow_id = models.AutoField(primary_key=True)
    # 关注者ID
    follower = models.ForeignKey(user, on_delete=models.CASCADE, related_name='following', verbose_name="关注者ID")
    # 被关注者ID
    followee = models.ForeignKey(user, on_delete=models.CASCADE, related_name='followers', verbose_name="被关注者ID")


# 用户消息模型
class user_message(models.Model):
    # 用户消息的唯一标识
    message_id = models.AutoField(primary_key=True)
    # 接收者ID
    receiver = models.ForeignKey(user, on_delete=models.CASCADE, related_name='received_messages',
                                 verbose_name="接收者ID")
    # 发送者ID
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="发送者ID")
    # 消息内容
    message_content = models.TextField(verbose_name="消息内容")
    # 发送时间
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="发送时间")


# 宠物模型
class pet(models.Model):
    # 宠物唯一标识
    pet_id = models.AutoField(primary_key=True)
    # 关联的用户ID
    user = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name="关联的用户ID")
    # 宠物名字
    pet_name = models.CharField(max_length=50, verbose_name="宠物名字")
    # 类别（0-猫 1-狗 2-其他）
    pet_type = models.IntegerField(verbose_name="类别")
    # 品种
    species_id = models.IntegerField(verbose_name="品种")
    # 性别（0-母 1-公 2-其他）
    sex = models.IntegerField(verbose_name="性别")
    # 年龄
    age = models.IntegerField(verbose_name="年龄")
    # 体重
    weight = models.FloatField(verbose_name="体重")
    # 宠物身份证二维码
    qr_code = models.CharField(max_length=255, unique=True, verbose_name="宠物身份证二维码")


# 宠物百科模型
class pet_encyclopedia(models.Model):
    # 品种唯一标识
    species_id = models.AutoField(primary_key=True)
    # 类别（0-猫 1-狗 2-其他）
    pet_type = models.IntegerField(verbose_name="类别")
    # 品种名
    species_name = models.CharField(max_length=255, verbose_name="品种名")
    # 特征
    characteristic = models.TextField(verbose_name="特征")
    # 护理建议
    care_instruction = models.TextField(verbose_name="护理建议")


# 宠物护理日记模型
class pet_care_diary(models.Model):
    # 护理日记唯一标识
    diary_id = models.AutoField(primary_key=True)
    # 关联的宠物ID
    pet = models.ForeignKey(pet, on_delete=models.CASCADE, verbose_name="关联的宠物ID")
    # 日记内容
    content = models.TextField(verbose_name="日记内容")
    # 宠物体重
    weight = models.FloatField(verbose_name="宠物体重")


# 系统通知模型
class notification(models.Model):
    # 系统通知的唯一标识
    notification_id = models.AutoField(primary_key=True)
    # 接收用户
    user = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name="接收用户")
    # 消息内容
    message = models.TextField(verbose_name="消息内容")


# 论坛帖子模型
class post(models.Model):
    # 帖子的唯一标识
    post_id = models.AutoField(primary_key=True)
    # 发布帖子的用户
    user = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name="用户ID")
    # 帖子标题
    title = models.CharField(max_length=255, verbose_name="标题")
    # 帖子内容
    content = models.TextField(verbose_name="内容")
    # 帖子图片URL，存储为JSON格式
    picture_url = models.JSONField(verbose_name="图片URL", blank=True, null=True)
    # 帖子标签
    tags = models.CharField(max_length=50, verbose_name="标签", blank=True, null=True)
    # 点赞数
    likes_count = models.PositiveIntegerField(default=0, verbose_name="点赞数")
    # 评论数
    comments_count = models.PositiveIntegerField(default=0, verbose_name="评论数")


class comment(models.Model):
    # 评论的唯一标识
    comment_id = models.AutoField(primary_key=True)
    # 评论内容
    content = models.TextField(verbose_name="内容")
    # 评论所属的帖子
    post = models.ForeignKey(post, related_name='comments', on_delete=models.CASCADE, verbose_name="帖子ID")
    # 发表评论的用户
    user = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name="用户ID")
    # 评论创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 父评论，允许为空，用于实现评论回复
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE,
                               verbose_name="父评论ID")
    # 点赞数
    likes_count = models.PositiveIntegerField(default=0, verbose_name="点赞数")


# 互助模型
class Help(models.Model):
    # 互助帖子的唯一标识
    help_id = models.AutoField(primary_key=True)
    # 需要帮助的宠物ID
    pet = models.ForeignKey(pet, on_delete=models.CASCADE, verbose_name="需要帮助的宠物ID")
    # 发布互助的用户
    requester = models.ForeignKey(user, related_name='help_requests', on_delete=models.CASCADE,
                                  verbose_name="发布互助的用户")
    # 提供帮助的用户
    provider = models.ForeignKey(user, related_name='help_provided', on_delete=models.CASCADE,
                                 verbose_name="提供帮助的用户")
    # 互助状态（0-待接取 1-进行中 2-已完成）
    status = models.IntegerField(default=0, verbose_name="互助状态")
    # 互助详情
    detail = models.TextField(verbose_name="互助详情")
    # 佣金
    cost = models.CharField(max_length=255, verbose_name="佣金")
    # 互助标签
    tags = models.CharField(max_length=50, verbose_name="标签", blank=True, null=True)
