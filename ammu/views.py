from oauth2_provider.contrib.rest_framework import OAuth2Authentication      
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .exceptions import *
from rest_framework import serializers

class CreatePostRequest:
    def __init__(self, user_id, content=''):
        self.user_id = user_id
        self.content = content

class CreatePostRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    content = serializers.CharField()

    def create(self, validated_data):
        return CreatePostRequest(**validated_data)
        


class CreatePostResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    
@api_view(["POST"])
def create_new_post(request):
    serializer = CreatePostRequestSerializer(data = request.data)
    is_serializer_valid = serializer.is_valid()
    if is_serializer_valid:
        request_obj = serializer.save()
        from .utils import create_post
        try:
            new_post_obj = create_post(request_obj.user_id, request_obj.content)
            
        except InvalidUserException:
            return Response(status=404)
        except InvalidPostContent:
            return Response(status=404)
        response_serializer = CreatePostResponseSerializer(new_post_obj)
        return Response(response_serializer.data, status=201)
    else:
        Response(serializer.errors)

