from django.contrib import admin
from django.db import models

# Register your models here.
from .models import Teacher


admin.site.register(Teacher)
