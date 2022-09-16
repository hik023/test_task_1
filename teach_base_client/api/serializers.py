from rest_framework import  serializers

from client.models import Course, CourseSection, CourseSectionMaterial


class CourseListSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedRelatedField(
        view_name='courses-detail', read_only=True, lookup_field='third_party_id')
    class Meta:
        model = Course
        fields = ['name', 'description', 'third_party_id', 'link', 'img_url']


class CourseSectionMaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseSectionMaterial
        fields = ['name', 'description', 'third_party_id']


class CourseSectionSerializer(serializers.HyperlinkedModelSerializer):
    materials = CourseSectionMaterialSerializer(read_only=True, many=True)
    class Meta:
        model = CourseSection
        fields = ['name', 'third_party_id', 'materials']


class CourseDetailSerializer(serializers.HyperlinkedModelSerializer):
    sections = CourseSectionSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ['name', 'description', 'third_party_id', 'img_url', 'sections']
