from django.contrib import admin
from .models import PatientProfile, Observation, User

admin.site.register(PatientProfile)
admin.site.register(Observation)
admin.site.register(User)
