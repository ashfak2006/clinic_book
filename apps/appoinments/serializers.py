from rest_framework import serializers
from .models import TimeSlot, Appointment


class TimeSloteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ["start_time","end_time","doctor_clinic","doctor",
                  "day_of_week","is_active","max_tokens"]
    def validate(self,data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        day_of_week = data.get('day_of_week')
        if day_of_week > 6 or day_of_week < 0:
            raise serializers.ValidationError({
                 "detail":"select a valid weekday"
            })
        if end_time <= start_time:
            raise serializers.ValidationError({
                "detail":"time is note valid "
            })
        return data
    def create(self, validated_data):
        time_slote = TimeSlot.objects.create(**validated_data)
        return time_slote

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['session', 'reason_for_visit']
