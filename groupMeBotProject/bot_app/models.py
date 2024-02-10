from django.db import models
from rest_framework import serializers


class GroupLinkTb(models.Model):
    year            =   models.IntegerField(null = False)
    class_section   =   models.CharField(max_length=50)
    grp_link        =   models.CharField(max_length=200)

    created_at      =   models.DateTimeField(auto_now_add=True)
    updated_at      =   models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('year', 'class_section')
    def __str__(self) -> str:
        return f"{self.grp_link}"

class StudentTb(models.Model):
    uid             =   models.CharField(max_length=50,unique=True)
    name            =   models.CharField(max_length=50)
    class_section   =   models.CharField(max_length=50)
    year            =   models.IntegerField()
    grp_link        =   models.ForeignKey(GroupLinkTb,max_length=200,default = None, on_delete=models.RESTRICT)


    created_at      =   models.DateTimeField(auto_now_add=True)
    updated_at      =   models.DateTimeField(auto_now=True)

    # def __str__(self) -> str:
    #     return f"QuoteItem:{self.pk} quote_pk:{self.quote.pk} {self.comment}"





class ViewGroupLinkTb(serializers.ModelSerializer):
    class Meta:
        model = GroupLinkTb
        fields = '__all__'


class StudentTbSerializer(serializers.ModelSerializer):
    grp_link = ViewGroupLinkTb(read_only = True )

    class Meta:
        model = StudentTb
        fields = '__all__'

