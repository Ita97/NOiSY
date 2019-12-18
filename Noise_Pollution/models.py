from django.db import models
# Create your models here.


class Stanza(models.Model):
    name = models.CharField(max_length=20)
    rep = models.CharField(max_length=50)
    mail = models.EmailField()

    def __str__(self):
        return self.name


class Sensore(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.BooleanField()  # 0 digitale, 1 analogico
    room = models.ForeignKey(Stanza, on_delete=models.CASCADE, default="")
    key = models.CharField(max_length=15, default='000000000000000')
    authenticated = models.BooleanField(default=0)
    time_collection = models.IntegerField(default=0)

    def is_analogic(self):
        return self.type


class Dati(models.Model):
    sensore = models.ForeignKey(Sensore, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    analogic_value = models.IntegerField(default=-1)
    digital_value = models.BooleanField(null=True)





