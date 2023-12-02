from rest_framework import serializers
from .models import UploadedFile
from django.core.exceptions import ValidationError

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file',)

    def validate_file(self, value):
        allowed_extensions = ['pptx', 'docx', 'xlsx']
        file_extension = value.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise serializers.ValidationError("Invalid file type. Allowed types are pptx, docx, and xlsx.")

        return value