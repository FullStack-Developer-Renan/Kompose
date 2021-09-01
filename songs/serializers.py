from rest_framework import serializers


class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    
class SongSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    artist = ArtistSerializer()
    votes = serializers.IntegerField(read_only=True)
