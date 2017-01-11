from .models import Collection, Sample, Description, Publication, Taxon, Person, PersonsGroup, Organization
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Collection
		fields = ('id','number', 'dateRegistered_precision', 'content', 'stratigraphicUnit',
					'collectors_text', 'location', 'notes')


class SampleSerializer(serializers.ModelSerializer):
	#collection = serializers.ReadOnlyField(source='collection.number')

	class Meta:
		model = Sample
		fields = ('id','number', 'collection','publications', 'country', 'region',
					'regionSpec','geologicalContext','location','sistema','yarus','gorizont','dateCollected_precision','notes')

class DescriptionSerializer(serializers.ModelSerializer):
	sample = serializers.ReadOnlyField(source='sample.number')

	class Meta:
		model = Description
		fields = ('category', 'citation', 'group', 'genus', 'subgenus','species','speciesAuthor','speciesYear',
					'subspecies', 'subspeciesAuthor', 'subspeciesYear', 'notes')

class TaxonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Taxon
		fields = ('group', 'genus', 'subgenus','species','speciesAuthor','speciesYear',
					'subspecies', 'subspeciesAuthor', 'subspeciesYear')

class PublicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Publication
		fields = ('authors_text', 'year', 'title','periodical_text','pages','group',
					'notes', 'shelfCodeUp', 'shelfCodeDown')
