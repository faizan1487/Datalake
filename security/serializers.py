from rest_framework import serializers
from .models import Scan, Comment

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.scan_type = validated_data.get('scan_type', instance.scan_type)
        instance.scan_date = validated_data.get('scan_date', instance.scan_date)
        instance.severity = validated_data.get('severity', instance.severity)
        instance.remediation = validated_data.get('remediation', instance.remediation)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.scan_progress = validated_data.get('scan_progress', instance.scan_progress)
        instance.testing_method = validated_data.get('testing_method', instance.testing_method)
        instance.target = validated_data.get('target', instance.target)
        instance.target_value = validated_data.get('target_value', instance.target_value)
        instance.application_type = validated_data.get('application_type', instance.application_type)
        instance.file_upload = validated_data.get('file_upload', instance.file_upload)
        instance.poc = validated_data.get('poc', instance.poc)

        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
