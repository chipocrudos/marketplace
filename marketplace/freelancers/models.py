from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date


class Job(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=80)
    description = models.TextField()
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired = models.DateField()
    concluded = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ['created', '-concluded', 'expired']

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def available(self):
        return not self.accept_set.filter(
            reject=False
        ) and self.expired > date.today()


class Accept(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reject = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Accept"
        verbose_name_plural = "Accepted"

    def __str__(self):
        pass
