from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, pagination
from rest_framework.reverse import reverse

from nodeshot.core.base.fields import PointField
from nodeshot.core.layers.models import Layer

from .models import *

PARTICIPATION_INSTALLED = 'nodeshot.community.participation' in settings.NODESHOT['API']['APPS_ENABLED']
HSTORE_ENABLED = settings.NODESHOT['SETTINGS'].get('HSTORE', True)

if HSTORE_ENABLED:
    from nodeshot.core.base.fields import HStoreDictionaryField


__all__ = [
    'NodeListSerializer',
    'NodeCreatorSerializer',
    'NodeDetailSerializer',
    'PaginatedNodeListSerializer',
    'ImageListSerializer',
    'ImageAddSerializer',
    'ImageEditSerializer',
    'StatusListSerializer'
]

  
class NodeDetailSerializer(serializers.ModelSerializer):
    """ node detail """
    user = serializers.Field(source='user.username')
    status = serializers.Field(source='status.slug')
    geometry = PointField(label=_('coordinates'))
    layer_name = serializers.Field(source='layer.name')
    layer_details = serializers.HyperlinkedRelatedField(view_name='api_layer_detail', source='layer', read_only=True)
    images = serializers.HyperlinkedIdentityField(view_name='api_node_images', slug_field='slug')
    access_level = serializers.Field(source='get_access_level_display')
    
    if HSTORE_ENABLED:
        data = HStoreDictionaryField(required=False, label=_('extra data'), help_text=_('stoca!'))
    
    if PARTICIPATION_INSTALLED:
        comments = serializers.HyperlinkedIdentityField(view_name='api_node_comments', slug_field='slug')
    
    class Meta:
        model = Node
        primary_fields = [
            'name', 'slug', 'status', 'user',
            'geometry', 'elev', 'address', 'description',
        ]
        
        if HSTORE_ENABLED:
            primary_fields += ['data']
            
        secondary_fields = [
            'access_level', 'layer', 'layer_name', 'added', 'updated',
            'layer_details', 'images'
        ]
        
        if PARTICIPATION_INSTALLED:
            secondary_fields += ['comments']
        
        fields = primary_fields + secondary_fields
        
        read_only_fields = ('added', 'updated')


class NodeListSerializer(NodeDetailSerializer):
    """ node list """
    
    details = serializers.HyperlinkedIdentityField(view_name='api_node_details', slug_field='slug')
    
    class Meta:
        model = Node
        fields = [
            'name', 'slug', 'layer', 'layer_name', 'user', 'status',
            'geometry', 'elev', 'address', 'description', 'data',
            'updated', 'added', 'details'
        ]
        
        read_only_fields = ['added', 'updated']


class PaginatedNodeListSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = NodeListSerializer


class NodeCreatorSerializer(NodeDetailSerializer):
    layer = serializers.WritableField(source='layer')


class ImageListSerializer(serializers.ModelSerializer):
    """ Serializer used to show list """
    
    file_url = serializers.SerializerMethodField('get_image_file')
    uri = serializers.SerializerMethodField('get_uri')
    
    def get_image_file(self, obj):
        """ returns url to image file or empty string otherwise """
        url = ''
        
        if obj.file != '':
            url = '%s%s' % (settings.MEDIA_URL, obj.file)
        
        return url
    
    def get_uri(self, obj):
        """ returns uri of API image resource """
        args = {
            'slug': obj.node.slug,
            'pk': obj.pk
        }
        
        return reverse('api_node_image_detail', kwargs=args, request=self.context.get('request', None))
    
    class Meta:
        model = Image
        fields = (
            'id', 'file', 'file_url', 'description', 'order',
            'access_level', 'added', 'updated', 'uri'
        )
        read_only_fields = ('added', 'updated')


class ImageAddSerializer(ImageListSerializer):
    """ Serializer for image creation """
    
    class Meta:
        model = Image
        fields = (
            'node', 'id', 'file', 'file_url', 'description', 'order',
            'access_level', 'added', 'updated', 'uri'
        )


class ImageEditSerializer(ImageListSerializer):
    """ Serializer for image edit """
    
    class Meta:
        model = Image
        fields = ('id', 'file_url', 'description', 'order', 'access_level', 'added', 'updated', 'uri')
        read_only_fields = ('file', 'added', 'updated')


# --------- Status --------- #


class StatusIconSerializer(serializers.ModelSerializer):
    """ status icons """
    
    class Meta:
        model = StatusIcon


class StatusListSerializer(serializers.ModelSerializer):
    """ status list """
    
    icons = StatusIconSerializer(source='statusicon_set', many=True, read_only=True)
    
    class Meta:
        model = Status
        fields = ['id', 'name', 'slug', 'description', 'icons']