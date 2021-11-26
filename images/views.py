from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import ImageSerializer, ImageExpiredLinkSerializer, TokenSerializer, LoginSerializers, LinkSerializer
from rest_framework.response import Response
from .models import UserPlan, Image, Link
from easy_thumbnails.files import get_thumbnailer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http.response import FileResponse
from django.http import HttpResponseForbidden
import pytz
from datetime import datetime


class AddImageView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if UserPlan.objects.get(user=self.request.user).account_tier.choose_exp_time:
            return ImageExpiredLinkSerializer
        return ImageSerializer
    
    def perform_create(self, serializer):
        user = self.request.user.pk
        return serializer.save(user=UserPlan.objects.get(user=user))
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        user = self.request.user.pk
        account_plan = UserPlan.objects.get(user=user).account_tier
        links_dict = {}
        for height in account_plan.allowed_sizes:
            size = (height, int(height) * int(instance.width) / int(instance.height))
            thumb_url = get_thumbnailer(instance.picture).get_thumbnail({'size': size, 'crop': False})
            
            link = Link.objects.create(link_to_image=thumb_url.url, user=UserPlan.objects.get(user=user),
                                       expiring_time=instance.expiring_time)
            
            links_dict[height] = request.build_absolute_uri(link.link_gen)
        
        if account_plan.get_link_to_org:
            link_obj = Link.objects.create(link_to_image=instance.picture.url, user=UserPlan.objects.get(user=user),
                                           expiring_time=instance.expiring_time)
            links_dict['org'] = request.build_absolute_uri(link_obj.link_gen)
        
        return Response({
            'status': 200,
            'links': links_dict
        })

from django.db.models.functions import Concat
from django.db.models import F, Value, CharField
# this endpoint provides list of all original images uploaded by user
# it may be extended to provide links for thumbnails also - if client specifies
class ImagesListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer
    
    def get_queryset(self):
        return Link.objects.filter(user=UserPlan.objects.get(user=self.request.user.pk)).values('link_gen' )


def image_access(request, path):
    print(path)
    link_obj = Link.objects.get(link_gen=('image/') + path)
    utc = pytz.UTC
    if link_obj.expired_date is None or link_obj.expired_date.replace(tzinfo=utc) > datetime.now().replace(tzinfo=utc):
        path = link_obj.link_to_image.strip('/')
        response = FileResponse(open(path, 'rb+'))
        return response
    else:
        return HttpResponseForbidden('Access to this link has expired.')


class LoginView(APIView):
    serializer_class = LoginSerializers
    
    def post(self, request, format=None):
        serializer = LoginSerializers(data=request.data,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token = TokenSerializer(Token.objects.get(user=user))
        
        return Response({
            'status': 200,
            'Authorization': 'Token ' + str(token.data)
        })


from django import http
import sys
from django.template import loader, Context


def this_server_error(request, template_name='images/nondefault500.html'):
    """
    500 error handler.
    Templates: `500.html`
    Context: sys.exc_info() results
     """
    t = loader.get_template(template_name)  # You need to create a 500.html template.
    ltype, lvalue, ltraceback = sys.exc_info()
    context = {'type': ltype, 'value': lvalue, 'traceback': ltraceback}
    return http.HttpResponseServerError(t.render(context))
