from .models import Image, Link
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('picture',)


class ImageExpiredLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('picture', 'expiring_time')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        
        data['user'] = user
        return data


class LinkSerializer(serializers.ModelSerializer):
    link_gen = serializers.SerializerMethodField('link_gen1')
    
    class Meta:
        model = Link
        fields = ('link_gen',)

    def link_gen1(self, obj):
        return self.context['request'].build_absolute_uri(obj['link_gen']).replace('list/', '')