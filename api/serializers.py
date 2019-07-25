from rest_framework import serializers

from .models import Snapshot

class DefaultSnapshotSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Snapshot
        fields = ('timestamp', 'stations', 'weather')


class DetailSnapshotSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Snapshot
        fields = ('timestamp', 'stations', 'weather')
