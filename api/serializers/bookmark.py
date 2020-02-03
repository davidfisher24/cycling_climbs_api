# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Bookmark, Climb

class ClimbSerializer(serializers.ModelSerializer):
	class Meta:
		model = Climb
		fields = ('id', 'name', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center')

class BookmarkSerializer(serializers.ModelSerializer):
	
	def __init__(self, *args, **kwargs):
		super(BookmarkSerializer, self).__init__(*args, **kwargs)
		action = self.context['view'].action
		if action != 'create' and action != 'update':
			self.fields.update({"climb": ClimbSerializer()})
	

	class Meta:
		model = Bookmark
		fields = ('id', 'climb', 'user', 'created_at')


