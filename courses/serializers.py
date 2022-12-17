from rest_framework.serializers import ModelSerializer, Serializer

from .models import Course
from users.serializers import UserSerializer


class CourseDisplaySerializer(ModelSerializer):
    student_no = Serializer.IntegerField(source='get_enrolled_student')
    author = UserSerializer()

    class Meta:
        model=Course
        fields = [
            'course_uuid',
            'title',
            'student_no',
            'author',
            'price',
            'image_url',
        ]