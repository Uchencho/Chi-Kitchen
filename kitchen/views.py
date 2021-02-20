from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import renderers

import os


class HealthCheck(APIView):

    permission_classes          = []
    renderer_classes            = [renderers.JSONRenderer]

    def get(self, request):
        env = os.getenv("ENV")
        cloud_key = os.getenv("CLOUD_KEY")
        data = {
            "env" : env,
            "cloud_key" : cloud_key,
            "message" : "Hello serverless from Django"
        }

        return Response(data)
