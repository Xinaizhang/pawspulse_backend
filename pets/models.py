from django.db import models
from app.models import User


# 宠物模型
class Pet(models.Model):
    # 宠物唯一标识
    pet_id = models.AutoField(primary_key=True)
    # 关联的用户ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联的用户ID")
    # 宠物名字
    pet_name = models.CharField(max_length=50, verbose_name="宠物名字")
    # 类别（0-猫 1-狗 2-其他）
    pet_type = models.IntegerField(verbose_name="类别")
    # 品种，设置为外键
    species = models.ForeignKey('Pet_encyclopedia', on_delete=models.CASCADE, verbose_name="品种")
    # 性别（0-母 1-公 2-其他）
    sex = models.IntegerField(verbose_name="性别")
    # 出生日期
    birth_date = models.DateField(verbose_name="出生日期")
    # 体重
    weight = models.FloatField(verbose_name="体重")
    # 宠物身份证二维码
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="宠物身份证二维码")
    # 宠物头像
    avatar = models.ImageField(upload_to='pet_avatars/', blank=True, null=True, verbose_name="宠物头像")
    # 绝育情况
    sterilization = models.CharField(max_length=50,
                                     choices=[('未绝育', '未绝育'), ('已绝育', '已绝育'), ('未知', '未知')],
                                     default='未知', verbose_name="绝育情况")


# 宠物百科模型
class Pet_encyclopedia(models.Model):
    # 品种唯一标识
    species_id = models.AutoField(primary_key=True)
    # 类别（0-猫 1-狗 2-其他）
    pet_type = models.IntegerField(verbose_name="类别")
    # 品种名
    species_name = models.CharField(max_length=255, verbose_name="品种名")
    # 品种中文名
    species_name_cn = models.CharField(max_length=255, verbose_name="品种中文名", blank=True, null=True)
    # 特征
    characteristic = models.TextField(verbose_name="特征", blank=True, null=True)
    # 护理建议
    care_instruction = models.TextField(verbose_name="护理建议", blank=True, null=True)


# 宠物护理日记模型
class Pet_care_diary(models.Model):
    # 护理日记唯一标识
    diary_id = models.AutoField(primary_key=True)
    # 关联的宠物ID
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="关联的宠物ID")
    # 日记内容
    content = models.TextField(verbose_name="日记内容")
    # 宠物体重
    weight = models.FloatField(verbose_name="宠物体重")
