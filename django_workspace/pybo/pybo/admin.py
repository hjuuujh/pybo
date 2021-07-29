from django.contrib import admin

# Register your models here.
from pybo.models import Question, Answer

admin.site.register(Question)
admin.site.register(Answer)