from django.db import models


class Provincials(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code + " - " + self.name


class Districts(models.Model):
    name = models.CharField(max_length=100)
    provincial = models.ForeignKey(Provincials, related_name="districts", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Wards(models.Model):
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=20)
    district = models.ForeignKey(Districts, related_name="wards", on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.prefix, self.name)