from .models import Collection, Sample, Description, Publication, Taxon, Person, PersonsGroup, Organization
from rest_framework import viewsets
from .serializers import CollectionSerializer, SampleSerializer, DescriptionSerializer, PublicationSerializer, TaxonSerializer

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain

class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = Collection.objects.all()
	serializer_class = CollectionSerializer

	def get_queryset(self):
		search_query = self.request.GET.get('q', '')
		QQ = Q(dateRegistered_precision__icontains=search_query) | Q(content__icontains=search_query) | Q(collectors_text__icontains=search_query) | Q(location__icontains=search_query) | Q(stratigraphicUnit__icontains=search_query)
		try:
			x = int(search_query) + 1
		except (UnicodeEncodeError,ValueError):
			return Collection.objects.filter(QQ).order_by('-id')
		else:
			queryset = Collection.objects.filter(number=int(search_query))
			return list(chain(queryset, Collection.objects.filter(QQ).order_by('-id')))



class SampleViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Sample.objects.all()
	serializer_class = SampleSerializer

	def get_queryset(self):
		search_query = self.request.GET.get('q', '')
		if search_query == '':
			QQ = Q()
		else:
			QQ = Q(notes__icontains=search_query)
		collection = self.request.GET.get('col', '')
		try:
			x = int(search_query) + 1
		except (UnicodeEncodeError,ValueError):
			return Sample.objects.filter(QQ, collection_id=collection).order_by('-id')
		else:
			queryset = Sample.objects.filter(number=int(search_query), collection_id=collection)
			return list(chain(queryset, Sample.objects.filter(QQ, collection_id=collection).order_by('-id')))

class IndexView(generic.base.TemplateView):
	template_name = 'db/index.html'
