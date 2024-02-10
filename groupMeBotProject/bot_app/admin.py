from django.contrib import admin
from .models import GroupLinkTb,StudentTb

# Register your models here.
@admin.register(GroupLinkTb)
class GroupLinkTbModel(admin.ModelAdmin):
    search_fields = ['year', 'class_section', 'grp_link']
    list_display = ['id', 'year', 'class_section', 'grp_link',"created_at",'updated_at',]


@admin.register(StudentTb)
class PStudentTbModel(admin.ModelAdmin):
    search_fields = ['name','year', 'class_section', 'grp_link']
    list_display = ['id', 'name', 'grp_link', 'year',"year"]