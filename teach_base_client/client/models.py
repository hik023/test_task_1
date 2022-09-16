from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    img_url = models.URLField()
    third_party_id = models.IntegerField()


class CourseSection(models.Model):
    name = models.CharField(max_length=64)
    third_party_id = models.IntegerField()
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)


class CourseSectionMaterial(models.Model):
    name = models.CharField(max_length=64)
    third_party_id = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    course_section = models.ForeignKey(CourseSection, related_name='materials', on_delete=models.CASCADE)
