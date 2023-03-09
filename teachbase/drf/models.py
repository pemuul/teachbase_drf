from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=255)
    test2 = models.ForeignKey('Test2', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title


class Test2(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title