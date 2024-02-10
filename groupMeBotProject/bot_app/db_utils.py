from .models import StudentTb
from rest_framework import serializers
from datetime import datetime

import csv



class StudentTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTb
        fields = '__all__'



def import_books(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        books_data = []
        for row in reader:
            # Convert published_date string to datetime object
            row['published_date'] = datetime.strptime(row['published_date'], '%Y-%m-%d').date()
            # Serialize the data
            serializer = StudentTbSerializer(data=row)
            if serializer.is_valid():
                books_data.append(serializer.validated_data)
            else:
                print(serializer.errors)
        # Save data in bulk and update existing records
        StudentTb.objects.bulk_update_or_create(
            books_data,
            ['title'],  # Fields to check for existing records
            update_fields=['author', 'published_date', 'price']  # Fields to update if the record exists
        )