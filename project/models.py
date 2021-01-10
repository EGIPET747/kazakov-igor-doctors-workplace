from django.db import models


class Person(models.Model):
    fio = models.TextField(max_length=100)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    passport = models.TextField(max_length=11)
    oms = models.TextField(max_length=12)

    def __str__(self):
        return "пользователь: " + str(self.fio)


class Symptom(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return "симптом: " + str(self.name)


class Disease(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return "заболевание: " + str(self.name)


class Examination(models.Model):
    datetime = models.DateTimeField()
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    diseases = models.ManyToManyField(Disease)

    def __str__(self):
        return "обследование: " + str(self.datetime)
