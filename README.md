# Spotify Playlist Songs Downloader

This application allows you to download songs from your Spotify playlists for offline use by sourcing them from YouTube and converting them to MP3 format. Follow the steps below to set up and use the tool.

## Prerequisites

- **Spotify Account**: Make sure you have an active Spotify account.
- **Spotify Developer Account**: You will need to create an app on Spotify Developer Portal to use this tool.
- **Python**: Ensure you have Python installed (preferably version 3.6+).
- **Required Libraries**: Install the necessary Python libraries by running:
  ```bash
  pip install spotipy pytube youtube-search pillow


## Instructions

1. Go to the [Spotify Developer Portal](https://developer.spotify.com/).
2. Log in with your Spotify account.
3. Create an app:
   - Use `https://www.self-spotify.com/` as the website.
   - Use `http://www.google.com/` as the redirect URI.
4. Ensure you are connected to the internet before proceeding.

## Running the Program

1. **Start the Application**:
   Run the program using Python:
   ```bash
   python spotify_song_download_gui.py
   ```
   
2. **Input Spotify Credentials**:
   - Enter the `Client ID` and `Client Secret` from your Spotify app (created in step 3) when prompted.
   - Enter your **Spotify Username**:
     - Click on your Spotify profile picture on the Spotify desktop app.
     - Select the **Account** option to be redirected to the Spotify website.
     - Choose **Edit Profile** and find your actual Spotify username to enter in the input.

3. **Select Playlist and Download**:
   - Choose the playlist you want to download by entering the index number displayed on the screen.
   - Provide the download location by selecting a folder on your computer to save the songs.
   
4. **Post-Download Instructions**:
   After all the songs have been downloaded:
   - Transfer the downloaded songs from your computer to your mobile phone.
   - On the Spotify mobile app:
     1. Go to **Settings** > **Show Local Files** and enable this feature.
     2. The downloaded songs will appear in the **Local Files** section.
     3. You can either play them directly from **Local Files** or create a new playlist and add the downloaded songs.

5. **Offline Availability**:
   Once the songs are available in your Spotify app, you can listen to them offline with all Spotify features such as shuffle, loop, and queue.

## Features

- Downloads songs from a Spotify playlist by searching them on YouTube.
- Converts downloaded songs into MP3 format.
- Offers seamless integration with the Spotify app for offline listening.
