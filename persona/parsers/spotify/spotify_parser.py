from persona.models import ArtistObject


def parse_artists(artists):
        artist_list = artists['items']
        external_urls = item.get("external_urls", None)
        artist_object = ArtistObject()

        artist_object.id = item['id']
        # Join Genres into comma seperated string
        genres = ','.join(item["genres"])
        artist_object.genres = genres
        artist_object.href = item['href']


