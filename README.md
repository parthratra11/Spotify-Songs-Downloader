Spotify Playlist Songs Downloader
This program allows users to download songs from a Spotify playlist by searching for them on YouTube and then downloading them. It involves using the Spotify and YouTube APIs and a tkinter GUI for the interface.

Refer to the .txt file for the instructions on how to use the application.

Requirements
Make sure you have the following packages installed:

youtube_search
pytube
tkinter
PIL
spotipy
You can install the required packages using pip:

pip install youtube-search-python
pip install pytube
pip install pillow
pip install spotipy

Usage
Run the script.
You will be prompted to enter your Spotify client_id and client_secret.
Then you will need to enter your Spotify username.
The script will display your playlists. Enter the index number of the playlist you want to download.
Select the location where you want to save the downloaded songs.
The program will search for the songs on YouTube, download them, and convert them to mp3 format.
Once the download is complete, it will prompt you to continue downloading other playlists or exit the program.

Note: Make sure you have an active internet connection throughout the process.

Acknowledgements
This code uses the following libraries:

youtube-search-python
pytube
Pillow
spotipy

Important Notes:
The script requires valid Spotify developer credentials to run. Follow the instructions within the script to obtain these credentials.
Ensure you have a working understanding of the Spotify and YouTube APIs before running this code.
Be cautious of rate limits and API quotas when using the Spotify and YouTube APIs.
Make sure to comply with the terms of service of both Spotify and YouTube when using their APIs.
Please refer to the Python documentation for more information on the Python programming language.
