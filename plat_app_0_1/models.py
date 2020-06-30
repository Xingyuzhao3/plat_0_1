from django.db import models

# Create your models here.
class Ch_rete_dtl(models.Model):
    pday = models.IntegerField()   #参加人数
    ch_id = models.IntegerField()
    rete_d1 = models.FloatField()
    rete_d2 = models.FloatField()
    rete_d3 = models.FloatField()
    rete_d4 = models.FloatField()
    rete_d5 = models.FloatField()
    rete_d6 = models.FloatField()
    rete_d7 = models.FloatField()
    rete_d8 = models.FloatField()
    rete_d9 = models.FloatField()
    rete_d10 = models.FloatField()
    rete_d11 = models.FloatField()
    rete_d12 = models.FloatField()
    rete_d13 = models.FloatField()
    rete_d14 = models.FloatField()
    rete_d15 = models.FloatField()
    rete_d16 = models.FloatField()
    rete_d17 = models.FloatField()
    rete_d18 = models.FloatField()
    rete_d19 = models.FloatField()
    rete_d20 = models.FloatField()
    rete_d21 = models.FloatField()
    rete_d22 = models.FloatField()
    rete_d23 = models.FloatField()
    rete_d24 = models.FloatField()
    rete_d25 = models.FloatField()
    rete_d26 = models.FloatField()
    rete_d27 = models.FloatField()
    rete_d28 = models.FloatField()
    rete_d29 = models.FloatField()
    dnu = models.IntegerField()


class Dim_ch(models.Model):
    ch = models.IntegerField() #发布会标题
    ch_type = models.CharField(max_length=200)
    ch_name = models.CharField(max_length=200)