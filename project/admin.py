from django.contrib import admin
from project.models import Person, Symptom, Disease, Examination

admin.site.register(Person)
admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(Examination)