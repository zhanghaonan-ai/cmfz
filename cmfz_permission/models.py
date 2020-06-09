from django.db import models


# Create your models here.

class Permission(models.Model):
    """verbose_name:字段详细名称
       db_column: 在数据库中的字段名称
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    is_menu = models.BooleanField(verbose_name="是否是菜单", default=False)

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=20)
    roles = models.ManyToManyField(verbose_name = '拥有的所有角色', to = 'cmfz_permission.Role', blank = True)
    class Meta:
        db_table = 'admin'

    def __str__(self):
        return self.name