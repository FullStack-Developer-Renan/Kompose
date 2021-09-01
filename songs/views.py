from rest_framework.views import APIView
from .models import Song, Artist
from .serializers import SongSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class SongView(APIView):
    def get(self, request, song_id=None):
        if song_id:
            song = get_object_or_404(Song, pk=song_id)
            serializer = SongSerializer(song)
            return Response(serializer.data, status=status.HTTP_200_OK)

        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SongSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        artist = Artist.objects.get_or_create(**serializer.data["artist"])[0]
        song = Song.objects.get_or_create(title=serializer.data["title"], artist=artist)[0]

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, song_id):
        serializer = SongSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        song = get_object_or_404(Song, pk=song_id)
        song.title = serializer.data["title"]

        artist = Artist.objects.get_or_create(**serializer.data["artist"])[0]
        song.artist = artist

        song.save()

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        song.votes += 1
        song.save()

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        song.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)