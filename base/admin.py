from django.contrib import admin

# Register your models here.


from .models import User, Parent, Hospital, Child, Vaccine, HospitalVaccine, Appointment, Admin, VaccineSupplier, HealthInfo

admin.site.register(User)
admin.site.register(Parent)
admin.site.register(Hospital)
admin.site.register(Child)
admin.site.register(Vaccine)
admin.site.register(HospitalVaccine)
admin.site.register(Appointment)
admin.site.register(Admin)
admin.site.register(VaccineSupplier)
admin.site.register(HealthInfo)