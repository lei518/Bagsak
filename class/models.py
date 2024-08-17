from django.db import models
from accounts.models import *
from django.contrib.auth.models import AbstractUser, Group, Permission
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='assignments/')
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')

    def __str__(self):
        return f"{self.student} submitted {self.assignment}"

class User(AbstractUser):

    is_professor = models.BooleanField('is prof', default=False)
    is_student = models.BooleanField('is stud', default=False)

    # def has_perms(self, perm_list):
    #     return True




# Create your models here.
