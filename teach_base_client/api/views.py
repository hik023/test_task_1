from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from client.models import Course
from .serializers import CourseListSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseListSerializer(queryset, many=True)
        authentication_classes = [SessionAuthentication]
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, third_party_id=pk)
        serializer = CourseDetailSerializer(course)
       
        return Response(serializer.data)