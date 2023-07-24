from youtube_search import YoutubeSearch
from pytube import YouTube
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

client_id: str=input('\nEnter your client id:')
client_secret: str=input('\nEnter your client secret:')

spotify_credentials={'client_id':client_id,
                     'client_secret':client_secret,
                     'redirect_uri':'http://www.google.com/',
                     'scope':('playlist-modify-private', 'playlist-read-private')}

spotify_auth=SpotifyOAuth(client_id=spotify_credentials['client_id'], client_secret=spotify_credentials['client_secret'], redirect_uri=spotify_credentials['redirect_uri'], scope=spotify_credentials['scope'])
refresh_token=spotify_auth.get_cached_token()

token=Spotify(auth_manager=spotify_auth)

spotify_username: str=input('\nEnter your spotify username:'); print('')

search_results=token.user_playlists(spotify_username)

spotify_playlists=[search_results['items'][playlist]['name'] for playlist in range(len(search_results['items']))]; print('')

for playlist in range(len(spotify_playlists)):
    print(f'{playlist+1}.', spotify_playlists[playlist])

temp_playlist=int(input('\nEnter the playlist to be downloaded:')); print('')

playlist=search_results['items'][temp_playlist-1]['external_urls']['spotify']

playlist_tracks=token.playlist_tracks(playlist)['items']

track_names=tuple(track['track']['name'] for track in playlist_tracks)
track_artists=tuple(track['track']['artists'][0]['name'] for track in playlist_tracks)

track_names_artists=tuple(f'{track_names[track]} by {track_artists[track]} full song' for track in range(len(track_names)))

download_path: str=input('Enter the download path:'); print('')

for track in range(len(track_names_artists)):
    yt_search=YoutubeSearch(track_names_artists[track], max_results=1).to_dict()
    yt_video=YouTube(f"https://www.youtube.com/{yt_search[0]['url_suffix']}").streams.filter(only_audio=True).first()

    try:        
        main_file=yt_video.download(output_path=download_path)
        
        base_file, extension=os.path.splitext(main_file)
        temp_file=base_file+'.mp3'
        os.rename(main_file, temp_file)

        print(f'{yt_video.title} has been successfully downloaded')

    except:
        print(f'An error has occured, {yt_video.title} could not be downloaded, Please check if the file already exists')

print('')
