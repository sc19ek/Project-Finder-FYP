from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmployeeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    grade = models.CharField(max_length=100)
    los = models.CharField(max_length=100)
    skills = models.CharField(max_length=300)
    languages = models.CharField(max_length=300, default='English')
    def __str__(self) -> str:
        return self.user.username


class ProjectRole(models.Model):
    requester = models.ForeignKey(EmployeeUser, on_delete=models.CASCADE)
    projectTitle = models.CharField(max_length=100)
    roleTitle = models.CharField(max_length=100)
    los = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.CharField(max_length=300)
    skills = models.CharField(max_length=300)
    baseOffice = models.CharField(max_length=200)
    creationDate = models.DateField()
    def __str__(self) -> str:
        return self.projectTitle


class Applications(models.Model):
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    applicant = models.ForeignKey(EmployeeUser, on_delete=models.CASCADE)
    applicationDate = models.DateField()
    def __str__(self) -> str:
        return self.id