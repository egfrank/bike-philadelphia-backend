from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import DefaultSnapshotSerializer, DetailSnapshotSerializer
from .models import Snapshot
from django.db.models.functions import ExtractHour,ExtractDay, RowNumber
from django.db.models import F, Window

from datetime import datetime, timedelta

class SnapshotList(APIView):

    def get(self, request, format=None):
        stations = Snapshot.objects.all().order_by('-timestamp')

        at_ = request.query_params.get('at', None)
        to_ = request.query_params.get('to', None)
        from_ = request.query_params.get('from', None)
        frequency = request.query_params.get('frequency', None)

        if at_:
            station = stations.filter(timestamp__gte=datetime.strptime(at_,'%Y-%m-%dT%X')).last()
            serializer = DefaultSnapshotSerializer(station, many=False)

        elif to_ and from_:
            stations = stations.filter(
                timestamp__gte=datetime.strptime(from_, '%Y-%m-%dT%X'),
                timestamp__lte=datetime.strptime(to_, '%Y-%m-%dT%X'))

            if frequency and frequency == 'daily':
                stations = stations.annotate(
                        freq=Window(
                            expression=RowNumber(),
                            partition_by=ExtractDay('timestamp'),
                            order_by=F('timestamp').asc()
                        ))

            elif (frequency and frequency == 'hourly') or not frequency:
                stations = stations.annotate(
                        freq=Window(
                            expression=RowNumber(),
                            partition_by=[ExtractHour(F('timestamp')), ExtractDay(F('timestamp'))],
                            order_by=F('timestamp').asc()
                        ))
            stations = [s for s in stations if s.freq == 1]
            serializer = DefaultSnapshotSerializer(stations, many=True)

        else:
            serializer = DefaultSnapshotSerializer(stations[0], many=False)
        return Response(serializer.data)

class SnapshotDetail(APIView):

    def get(self, request, kioskID, format=None):
        stations = Snapshot.objects.all().order_by('-timestamp')


        at_ = request.query_params.get('at', None)
        to_ = request.query_params.get('to', None)
        from_ = request.query_params.get('from', None)


        frequency = request.query_params.get('frequency', None)


        if at_:
            stations = stations.filter(timestamp__gte=datetime.strptime(at_,'%Y-%m-%dT%X')).last()
            
            try:
                stations.stations = stations.stations[str(kioskID)]
            except (KeyError, AttributeError):
                raise Http404() 

            serializer = DefaultSnapshotSerializer(stations, many=False)

        elif to_ and from_:
            stations = stations.filter(
                timestamp__gte=datetime.strptime(from_, '%Y-%m-%dT%X'),
                timestamp__lte=datetime.strptime(to_, '%Y-%m-%dT%X'))

            if frequency and frequency == 'daily':
                stations = stations.annotate(
                        freq=Window(
                            expression=RowNumber(),
                            partition_by=ExtractDay('timestamp'),
                            order_by=F('timestamp').asc()
                        ))
                

            elif (frequency and frequency == 'hourly') or not frequency:
                stations = stations.annotate()
                stations = stations.annotate(
                        freq=Window(
                            expression=RowNumber(),
                            partition_by=[ExtractHour(F('timestamp')), ExtractDay(F('timestamp'))],
                            order_by=F('timestamp').asc()
                        ))
            
            stations_list = []

            try:
                for station in stations:
                    station.stations = station.stations[str(kioskID)]
                    if station.freq == 1:
                        stations_list.append(station)

            except (KeyError, AttributeError):
                raise Http404() 


            serializer = DefaultSnapshotSerializer(stations_list, many=True)





        
        return Response(serializer.data)



def index(request):
    try:
        snapshot = Snapshot.objects.latest('timestamp') 

    except Snapshot.DoesNotExist:
        raise Http404("No Snapshots in DB")


    context = {
        'snapshot': snapshot
    }
    return render(request, 'api/index.html', context)




