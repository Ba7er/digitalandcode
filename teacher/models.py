import re
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.urls import reverse


from subject.models import Subject
# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    room_number = models.PositiveIntegerField(blank=False)
    phone_number = models.CharField(max_length=17, blank=True)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.first_name

    def clean(self):

        if re.match(r'^\+?1?\d{9,15}$', self.phone_number) is None:
            raise ValidationError(
                "Phone number must be entered in the format: '+999999999'. Up to 15 digits alloweddd.")

        m2m_changed.connect(subjects_changed, sender=Teacher.subjects.through)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.full_clean()  # @TODO: Check if we need to call this here
        super(Teacher, self).save(*args, **kwargs)


def subjects_changed(sender, **kwargs):
    if kwargs['instance'].subjects.count() > 5:
        raise ValidationError("Teacher cannot teach more than 5 subjects")
