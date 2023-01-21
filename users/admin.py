from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class User_detailsAdmin(admin.ModelAdmin):
    list_display = [ 'id','email','password','first_name','last_name','mobile_number','is_superuser','is_staff','role',
                     'is_active','last_login','is_deleted','created_date','modified_date']
# admin.register(User)
