from youtube_search import YoutubeSearch
from pytube import YouTube
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from threading import Thread
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# CREATING THE BASE WIDGET FOR ALL OPERATIONS TO BE PERFORMED
base = Tk()
base.title('Spotify Playlist Songs Downloader'); base.config(background = '#39473F')

# FUNCTION TO SELECT THE DOWNLOADED SPOTIFY ICON AND PROCEED FURTHER
def icon_selection():
    global base, temp_icon_path

    # try:
    #     # OPENS UP THE FILE_MANAGER AND ASKS FOR THE SELECTION OF DOWNLOADED SPOTIFY_ICON 
    #     temp_icon_path_var = filedialog.askopenfilename(initialdir = '\\', title = 'Select the downloaded Icon Image')
    #     temp_icon_path = ImageTk.PhotoImage(Image.open(temp_icon_path_var).resize((200, 200)))
    #     base.iconphoto(False, temp_icon_path)       

    # except:
    #     # DISPLAYS AN ERROR MESSAGE INCASE AN INVALID FILE IS CHOSEN
    #     messagebox.showerror('Invalid Icon !', 'Please select a valid spotify icon image !')
    #     icon_selection()

    #   AUTOMATICALLY PICKS UP THE LOGO TO RUN THE APPLICATION
    try:
        temp_icon_path = ImageTk.PhotoImage(Image.open('./spotify-logo.jpg').resize((200, 200)))
        base.iconphoto(False, temp_icon_path)
    except:
        temp_icon_path = None

icon_selection()

# DEFINING THE ESSENTIAL VARIABLES
client_id, client_secret, spotify_username, check_proceed_1, check_proceed_2 = '', '', '', 0, 0

# FUNCTION TO DOWNLOAD THE CHOSEN PLAYLIST AND FURTHER PROCEEDINGS
def playlist_download(index):
    global playlist_download_cancel_button, playlist_download_update_str, playlists_download_window, track, check_proceed_2

    # WITHDRAWS THE PLAYLISTS_DISPLAY WIDGET AND MAKES ROOM TO POP UP THE PLAYLISTS_DOWNLOAD WINDOW
    playlists_window.withdraw()
    playlist_download_update_str, track = '\n', 0

    # FUNCTION FOR CANCELLATION OF DOWNLOAD
    def end_download():
        global check_proceed_2

        # POPS UP A DIALOG BOX TO CONFIRM THE CANCELLATION OF DOWNLOAD
        playlist_download_cancel_button.config(state = DISABLED)
        check_cancellation = messagebox.askyesno('Spotify Playlist download cancellation !', 'Do you want to quit the download process ?')

        if check_cancellation == 1:
            # CANCELS THE DOWNLOAD PROCESS AND QUITS THE PROGRAM
            check_proceed_2 = 1; quit()

        else:
            # CONTINUES THE DOWNLOAD IF USER DECLINES THE CANCELLATION
            playlists_download_window.deiconify()
            playlists_download_cancel_button = Button(playlists_download_cancel_frame, text = 'CANCEL', bg = '#4B574E', fg = 'white', width = 11, font = ('Calibri', '10', 'bold'), command = end_download); playlists_download_cancel_button.grid(row = 0, column = 1)
    
    # FUNCTION FOR POST DOWNLOAD PROCESSES
    def playlist_post_download():
        # WITHDRAWS THE DOWNLOAD_PROGRESS WINDOW TO MAKE ROOM TO POP UP THE POST_DOWNLOAD_PROCESSING WIDHGET
        playlists_download_window.withdraw()

        # FUNCTION TO CONTINUE DOWNLOADING OTHER PLAYLISTS
        def continue_download():
            playlists_post_download_continue_yes.config(state = DISABLED)
            playlists_post_download_continue_no.config(state = DISABLED)

            playlists_post_download_window.withdraw()

            spotify_playlists(1)

        # CREATING THE WIDGET TO ASK USER TO CONTINUE DOWNLOADING OTHER PLAYLISTS OR END THE PROGRAM
        playlists_post_download_window = Toplevel()
        playlists_post_download_window.title('Spotify Playlist Songs Downloader'); playlists_post_download_window.config(background = '#39473F'); playlists_post_download_window.iconphoto(False, temp_icon_path)

        playlists_post_download_frame = Frame(playlists_post_download_window, borderwidth = 7, bg = '#BFBFBF'); playlists_post_download_frame.grid(row = 0, column = 0, rowspan = 4, columnspan = 3, padx = 10, pady = 10)

        playlist_post_download_str = playlist_download_update_str
        instructions_text_3 = '''\n7. import the downloaded songs to your mobile phone from the pc,
       after all the songs have been downloaded
    8. go to spotify on your mobile phone and enable the show local files feature
    9. you'll see the downloaded songs in the local files
    10. now they are available offline, either listen to them from the local files, 
        or create a new playlist and add the required songs to that playlist manually, 
        you'll be able to listen to them even without internet alongside the features of spotify 
        (shuffle, loop, queue, etc.) !\n'''
        
        playlist_post_download_label = Label(playlists_post_download_frame, highlightbackground = '#39473F', highlightthickness = 2, text = 'Your playlist has been downloaded !', bg = 'white', fg = 'black', width = 78, font = ('Bahnschrift', '12', ('bold', 'italic')), anchor = CENTER, relief = RAISED).grid(row = 0, column = 0, columnspan = 3)
        instructions_label_3 = Label(playlists_post_download_frame, highlightbackground = '#39473F', highlightthickness = 2, text = instructions_text_3, bg = 'white', fg = 'black', width = 100, font = ('Bahnschrift', '10', 'bold'), anchor = W, justify = 'left', relief = RAISED).grid(row = 1, column = 0, columnspan = 3)
        playlist_post_download_str_label = Label(playlists_post_download_frame, highlightbackground = '#39473F', highlightthickness = 2, text = playlist_post_download_str, bg = 'white', fg = 'black', width = 100, font = ('Bahnschrift', '10'), anchor = W, justify = 'left').grid(row = 2, column = 0, columnspan = 3)
        playlists_post_download_continue = Label(playlists_post_download_frame, highlightbackground = '#39473F', highlightthickness = 2, text = 'Do you want to download another spotify playlist ? ', bg = 'white', fg = 'black', width = 76, font = ('Bahnschrift', '10', 'bold'), anchor = E, relief = RAISED).grid(row = 3, column = 0)
        playlists_post_download_continue_yes = Button(playlists_post_download_frame, text = 'YES', bg = '#4B574E', fg = 'white', width = 10, font = ('Calibri', '10', 'bold'), command = continue_download); playlists_post_download_continue_yes.grid(row = 3, column = 1, padx = 1, pady = 1)
        playlists_post_download_continue_no = Button(playlists_post_download_frame, text = 'NO', bg = '#4B574E', fg = 'white', width = 10, font = ('Calibri', '10', 'bold'), command = quit); playlists_post_download_continue_no.grid(row = 3, column = 2, padx = 1, pady = 1)

    # FUNCTION TO DOWNLOAD THE SELECTED PLAYLIST
    def temp_playlist_download(track):
        global playlist_download_update_str

        quit() if check_proceed_2 == 1 else None

        # DOWNLOAD PROCESSING
        if track < len(track_names_artists):

            # SEARCHES THE SONG FROM THE SPOTIFY PLAYLIST AND SEARCHES IT ON YOUTUBE
            yt_search = YoutubeSearch(track_names_artists[track], max_results = 1).to_dict()
            yt_video = YouTube(f"https://www.youtube.com/{yt_search[0]['url_suffix']}").streams.filter(only_audio = True).first()

            try: 
                # DOWLOADS THE SEACHED SONG AUDIO FROM YOUTUBE IN .mp4 FORMAT AND THEN CHANGES IT TO .mp3 FORMAT
                main_file = yt_video.download(output_path = download_path)
                
                base_file, extension = os.path.splitext(main_file)
                temp_file = base_file + '.mp3'
                os.rename(main_file, temp_file)

                # INDICATION THAT THE SONG HAS BEEN SUCCESFULLY DOWNLOADED
                playlist_download_update_str += f'{yt_video.title} has been successfully downloaded\n'

            except:
                # INDICATION THAT THE SONG COULDN'T BE DOWNLOADED
                playlist_download_update_str += f'{yt_video.title} could not be downloaded, Please check if the file already exists\n'

            track += 1; temp_playlist_download(track)

        # POST DOWNLOAD PROCESSING
        else:
            playlist_download_cancel_button.config(state = DISABLED)
            playlist_post_download()

    playlist_selected = search_results['items'][index]['external_urls']['spotify']
    playlist_tracks = token.playlist_tracks(playlist_selected)['items']

    track_names = tuple(track['track']['name'] for track in playlist_tracks)
    track_artists = tuple(track['track']['artists'][0]['name'] for track in playlist_tracks)

    # TUPLE CONTAINING TRACKS + ARTISTS NAME FROM THE SELECTED PLAYLIST
    track_names_artists=tuple(f'{track_names[track]} by {track_artists[track]} full song' for track in range(len(track_names)))

    # ASKS FOR THE LOCATION TO DOWNLOAD THE TRACKS FROM THE PLAYLIST
    download_path = filedialog.askdirectory(initialdir = '//', title = 'Select the location for the songs to be downloaded')

    # CREATES THE WIDGET TO DISPLAY THE DOWNLOAD OPERATION
    playlists_download_window = Toplevel()
    playlists_download_window.title('Spotify Playlist Songs Downloader'); playlists_download_window.config(background = '#39473F'); playlists_download_window.iconphoto(False, temp_icon_path)

    playlists_download_cancel_frame = Frame(playlists_download_window, borderwidth = 7, bg = '#BFBFBF'); playlists_download_cancel_frame.grid(row = 0, column = 0, columnspan = 3, rowspan = 2, padx = 10, pady = 10)

    playlist_download_progress_label = Label(playlists_download_cancel_frame, text = "Your download is in progress...", width = 50, height = 2, font = ('Calibri', '12', 'bold'), highlightbackground = 'white', highlightthickness = 2, anchor = CENTER, relief = RAISED); playlist_download_progress_label.grid(row = 0, column = 0, columnspan = 2)
    playlist_download_cancel_label = Label(playlists_download_cancel_frame, text = "Press 'Cancel' to quit the process ->", width = 40, font = ('Calibri', '10', 'bold'), highlightbackground = 'white', highlightthickness = 2, anchor = E); playlist_download_cancel_label.grid(row = 1, column = 0, padx = 1, pady = 2)
    playlist_download_cancel_button = Button(playlists_download_cancel_frame, text = 'CANCEL', bg = '#4B574E', fg = 'white', width = 15, font = ('Calibri', '10', 'bold'), command = end_download); playlist_download_cancel_button.grid(row = 1, column = 1, padx = 1, pady = 1)

    download_func = Thread(target = lambda: temp_playlist_download(track)); download_func.start()

# PLAYLISTS_DISPLAY AND SPOTIFY_PLAYLIST_INDEX ENTRY
def spotify_playlists(entry):
    global playlist_entry, spotify_playlists_tuple, search_results, token, playlists_window

    # WITHDRAWING THE USERNAME_ENTRY WINDOW TO MAKE ROOM FOR THE PLAYLISTS_DISPLAY WINDOW
    user_entry_window.withdraw() if entry == 0 else None

    # USER_SPOTIFY_CREDENTIALS
    spotify_credentials={'client_id': client_id,
                         'client_secret': client_secret,
                         'redirect_uri': 'http://www.google.com/',
                         'scope': ('playlist-modify-private', 'playlist-read-private')}

    # CREATING THE LINK BETWEEN THE PYTHON CODE AND SPOTIFY
    try:
        spotify_auth = SpotifyOAuth(client_id = spotify_credentials['client_id'], client_secret = spotify_credentials['client_secret'], redirect_uri = spotify_credentials['redirect_uri'], scope = spotify_credentials['scope'])
        refresh_token = spotify_auth.get_cached_token()

        token = Spotify(auth_manager = spotify_auth)
        search_results = token.user_playlists(spotify_username)

        # TUPLE CONTAINING SPOTIFY_PLAYLISTS NAMES
        spotify_playlists_tuple = tuple(search_results['items'][playlist]['name'] for playlist in range(len(search_results['items'])))

    except:
        # ERROR POPUP INCASE THE CREDENTIALS ENTERED ARE INCORRECT
        check_proceed3 = messagebox.askokcancel('Spotify Playlist Downloader', 'The credentials entered do not correspond to a Spotify account\n\nPlease enter the credentials again !')
        initial_entry() if check_proceed3 == True or check_proceed3 == False else None

    # FUNCTION TO PERFORM THE BACKSPACE OPERATION FOR SPOTIFY_PLAYLISTS_INDEX ENTRY
    def entry_backspace():
        global playlist_entry

        temp_entry_val = str(playlist_entry.get())
        playlist_entry.delete(0, END); playlist_entry.insert(0, temp_entry_val[-2::-1][::-1])

    # FUNTION TO CONFIRM SPOTIFY_PLAYLISTS_INDEX ENTRY
    def entry_confirmed():

        # DISPLAY AN ERROR WARNING INCASE THE ENTERED INDEX ISN'T VALID
        if (playlist_entry.get()).isalpha() or int(playlist_entry.get()) > len(spotify_playlists_tuple) or int(playlist_entry.get()) < 1:
            messagebox.showerror('Error Warning !', 'Enter a valid Index No. !')

        else:
            playlist_label.config(fg = 'grey', relief = SUNKEN)
            Label(temp_playlist_frame_2, text = playlist_entry.get(), bg = 'white', fg = 'grey', width = 10, font = ('Bahnschrift', '10'), borderwidth = 4, anchor = W, justify = LEFT, relief = SUNKEN).grid(row = len(spotify_playlists_tuple) + 1, column = 1)
            playlist_backspace.config(state = DISABLED)
            playlist_confirm.config(state = DISABLED)

            playlist_download(int(playlist_entry.get()) - 1)

    # CREATING THE WIDGET TO DISPLAY THE PLAYLISTS NAME AND TAKING THE PLAYLIST TO BE DOWNLOADED AS INPUT
    playlists_window = Toplevel()
    playlists_window.title('Spotify Playlist Songs Downloader'); playlists_window.config(background = '#39473F'); playlists_window.iconphoto(False, temp_icon_path)

    playlists_frame = Frame(playlists_window, borderwidth = 7, bg = '#BFBFBF'); playlists_frame.grid(row = 0, column = 0, columnspan = 2, rowspan = len(spotify_playlists_tuple) + 3, padx = 10, pady = 5)
    
    temp_playlist_frame_1 = Frame(playlists_frame); temp_playlist_frame_1.grid(row = 0, column = 0, rowspan = len(spotify_playlists_tuple) + 1, columnspan = 2, pady = 5)
    temp_playlist_frame_2 = Frame(playlists_frame, bg = '#39473F'); temp_playlist_frame_2.grid(row = len(spotify_playlists_tuple) + 2, column = 0, rowspan = 2, columnspan = 4, pady = 5)

    playlist_index = Label(temp_playlist_frame_1, text = 'Index No.', highlightbackground = '#39473F', highlightthickness = 2, bg = 'white', fg = 'black', width = 10, height = 2, font = ('Bahnschrift', '10', 'bold'), relief = RAISED).grid(row = 0, column = 0)
    playlist_name = Label(temp_playlist_frame_1, text = 'Playlist Name', highlightbackground = '#39473F', highlightthickness = 2, bg = 'white', fg = 'black', width = 30, height = 2, font = ('Bahnschrift', '10', 'bold'), relief = RAISED).grid(row = 0, column = 1, columnspan = 2)

    for playlist in range(len(spotify_playlists_tuple)):
        Label(temp_playlist_frame_1, text = f'{playlist + 1}', highlightbackground = '#39473F', highlightthickness = 2, bg = 'white', fg = 'black', width = 10, font = ('Calibri', '10', 'bold'), anchor = W).grid(row = playlist + 1, column = 0)
        Label(temp_playlist_frame_1, text = f'{spotify_playlists_tuple[playlist]}', highlightbackground = '#39473F', highlightthickness = 2, bg = 'white', fg = 'black', width = 30, font = ('Calibri', '10', 'bold'), anchor = W).grid(row = playlist + 1, column = 1)

    playlist_label = Label(temp_playlist_frame_2, highlightbackground = '#39473F', highlightthickness = 2, height = 3, text = 'Enter the Index No. of the\nPlaylist to be downloaded :', bg = 'white', fg = 'black', width = 22, font = ('Bahnschrift', '10'), anchor = E, justify = RIGHT); playlist_label.grid(row = len(spotify_playlists_tuple) + 1, column = 0, rowspan = 2)
    playlist_entry = Entry(temp_playlist_frame_2, bg = 'white', fg = 'black', width = 10, font = ('Bahnschrift', '10'), borderwidth = 4, justify = LEFT); playlist_entry.grid(row = len(spotify_playlists_tuple) + 1, column = 1)
    playlist_backspace = Button(temp_playlist_frame_2, bg = '#4B574E', fg = 'white', height = 3, text = '<<', width = 6, font = ('Candara', '10', 'bold'), borderwidth = 2, command = entry_backspace); playlist_backspace.grid(row = len(spotify_playlists_tuple) + 1, column = 2, rowspan = 2, padx = 2, pady = 2)
    playlist_confirm = Button(temp_playlist_frame_2, bg = '#4B574E', fg = 'white', text = 'Confirm', width = 10, font = ('Candara', '10', 'bold'), borderwidth = 2, command = entry_confirmed); playlist_confirm.grid(row = len(spotify_playlists_tuple) + 2, column = 1)

# SPOTIFY USERNAME CODE ENTRY
def username_entry():
    global user_entry, user_entry_window

    # WITHDRAWING THE CLIENT_ID AND CLIENT_SECRET INPUT WIDGET TO MAKE ROOM FOR THE USERNAME_ENTRY WIDGET TO POP UP
    id_entry.withdraw()

    # CREATING THE WIDGET TO INPUT THE SPOTIFY_USERNAME_CODE
    user_entry_window = Toplevel()
    user_entry_window.title('Spotify Playlist Songs Downloader'); user_entry_window.config(background = '#39473F'); user_entry_window.iconphoto(False, temp_icon_path)

    # FUNCTION TO PERFORM THE BACKSPACE OPERATION FOR SPOTIFY_USERNAME_CODE
    def entry_backspace():
        global user_entry

        temp_entry_val = str(user_entry.get())
        user_entry.delete(0, END); user_entry.insert(0, temp_entry_val[-2::-1][::-1])

    # FUNTION TO CONFIRM SPOTIFY_USERNAME_CODE ENTRY
    def entry_confirmed():
        global spotify_username, user_entry

        if str(user_entry.get()) == '':
            messagebox.showerror('Error Warning !', f'Username cannot be empty !')

        else:
            spotify_username = str(user_entry.get())
            
            user_label.config(fg = 'grey', relief = SUNKEN)
            Label(user_entry_frame, text = str(user_entry.get()), bg = 'white', fg = 'grey', width = 26, font = ('Bahnschrift', '10'), borderwidth = 4,anchor = W, justify = LEFT, relief = SUNKEN).grid(row = 2, column = 1)
            user_backspace.config(state = DISABLED)
            user_confirm.config(state = DISABLED)

            spotify_playlists(0)

    # CREATION OF FRAME, INSRUCTIONS_TEXT, LABELS AND BUTTONS FOR THE SPOTIFY_USERNAME_CODE INPUT WIDGET
    user_entry_frame = Frame(user_entry_window, borderwidth = 7, bg = '#BFBFBF'); user_entry_frame.grid(row = 0, column = 0, columnspan = 4, padx = 10, pady = 10)

    instructions_text_2 = '''\n6. For spotify username input, 
    click on your spotify pfp from your pc and go to accounts opt,
    it will redirect you to a site,
    from there choose the opt to edit profile,
    there you will see your actual spotify username,
    give that as the spotify username input\n'''
    instructions_label_2 = Label(user_entry_frame, highlightbackground = '#39473F', highlightthickness = 2, text = instructions_text_2, bg = 'white', fg = 'black', width = 72, font = ('Bahnschrift', '10'), anchor = W, justify = 'left').grid(row = 0, column = 0, columnspan = 4)

    user_label = Label(user_entry_frame, highlightbackground = '#39473F', highlightthickness = 2, text = 'Enter your Username here :', bg = 'white', fg = 'black', width = 26, font = ('Bahnschrift', '10'), anchor = E); user_label.grid(row = 2, column = 0)
    user_entry = Entry(user_entry_frame, bg = 'white', fg = 'black', width = 26, font = ('Bahnschrift', '10'), borderwidth = 4, justify = LEFT); user_entry.grid(row = 2, column = 1)
    user_backspace = Button(user_entry_frame, bg = '#4B574E', fg = 'white', text = '<<', width = 5, font = ('Candara', '10', 'bold'), borderwidth = 2, command = entry_backspace); user_backspace.grid(row = 2, column = 2)
    user_confirm = Button(user_entry_frame, bg = '#4B574E', fg = 'white', text = 'Confirm', width = 10, font = ('Candara', '10', 'bold'), borderwidth = 2, command = entry_confirmed); user_confirm.grid(row = 2, column = 3)

# CLIENT_ID AND CLIENT_SECRET ENTRY
def initial_entry():
    global id_entry, client_id, client_secret, check_proceed_1, client_id_entry, client_secret_entry

    # WITHDRAWING THE BASE WIDGET AND MAKING ROOM FOR THE INPUT WIDGET TO POP UP
    base_entry_button.config(state = DISABLED)
    base.withdraw()

    # CREATING THE SECOND WIDGET FOR INPUT OF CLIENT_ID AND CLIENT_SECRET
    id_entry = Toplevel()
    id_entry.title('Spotify Playlist Songs Downloader'); id_entry.config(background = '#39473F'); 
    
    if temp_icon_path:
        id_entry.iconphoto(False, temp_icon_path)
        
    # FUNCTION TO PERFORM THE BACKSPACE OPERATION FOR CLIENT_ID AND CLIENT_SECRET
    def entry_backspace(var):
        global client_id_entry, client_secret_entry

        temp_entry_val = str(eval(f'{var}_entry').get())
        
        if var == 'client_id':
            client_id_entry.delete(0, END); client_id_entry.insert(0, temp_entry_val[-2::-1][::-1])

        elif var == 'client_secret':
            client_secret_entry.delete(0, END); client_secret_entry.insert(0, temp_entry_val[-2::-1][::-1])        

    # FUNTION TO CONFIRM BOTH CLIENT_ID AND CLIENT_SECRET ENTRIES
    def entry_confirmed(var):
        global client_id, client_secret, check_proceed_1

        # ERROR MEESSAGE POPS UP INCASE USER CONFIRMS AN EMPTY INPUT FOR CLIENT_ID AND CLIENT_SECRET
        if str(eval(f'{var}_entry').get()) == '':
            messagebox.showerror('Error Warning !', f'Client {var[7::]} cannot be empty !')

        else:

            if var == 'client_id':
                client_id = str(eval(f'{var}_entry').get()); check_proceed_1 += 1

                client_id_label.config(fg = 'grey', relief = SUNKEN)
                Label(initial_entries, highlightbackground = '#39473F', highlightthickness = 2, text = str(eval(f'{var}_entry').get()), bg = 'white', fg = 'grey', width = 26, font = ('Bahnschrift', '10'), anchor = W, relief = SUNKEN).grid(row = 1, column = 1)
                client_id_backspace.config(state = DISABLED)
                client_id_confirm.config(state = DISABLED)

            elif var == 'client_secret':
                client_secret = str(eval(f'{var}_entry').get()); check_proceed_1 += 1

                client_secret_label.config(fg = 'grey', relief = SUNKEN)                
                Label(initial_entries, highlightbackground = '#39473F', highlightthickness = 2, text = str(eval(f'{var}_entry').get()), bg = 'white', fg = 'grey', width = 26, font = ('Bahnschrift', '10'), anchor = W, relief = SUNKEN).grid(row = 2, column = 1)
                client_secret_backspace.config(state = DISABLED)                
                client_secret_confirm.config(state = DISABLED)                

            # IF BOTH CLIENT_ID AND CLIENT_SECRET ARE CONFIRMED, IT PROCEEDS FURTHER
            username_entry() if check_proceed_1 == 2 else None

    # CREATION OF FRAME, INSRUCTIONS_TEXT, LABELS AND BUTTONS FOR THE CLIENT_ID AND CLIENT_SECRET INPUT WIDGET
    initial_entries = Frame(id_entry, borderwidth = 7, bg = '#BFBFBF'); initial_entries.pack(anchor = CENTER, padx = 10, pady = 10)

    instructions_text_1 = '''\nFollow the following instructions to proceed further:
    (Make sure you are connected to the internet throughout the process)\n
    1. Go to developer.spotify.com
    2. Login with your spotify account
    3. Create an app, then:
        a. Use https://www.self-spotify.com/ as website
        b. Use http://www.google.com/ as redirect uri
    4. Enter the required details\n'''
    instructions_label_1 = Label(initial_entries, highlightbackground = '#39473F', highlightthickness = 2, text = instructions_text_1, bg = 'white', fg = 'black', width = 72, font = ('Bahnschrift', '10'), anchor = W, justify = 'left'); instructions_label_1.grid(row = 0, column = 0, columnspan = 4)

    client_id_label = Label(initial_entries, highlightbackground = '#39473F', highlightthickness = 2, text = 'Enter your Client ID here :', bg = 'white', fg = 'black', width = 26, font = ('Bahnschrift', '10'), anchor = E); client_id_label.grid(row = 1, column = 0)
    client_id_entry = Entry(initial_entries, bg = 'white', fg = 'black', width = 26, font = ('Bahnschrift', '10'), borderwidth = 4, justify = LEFT); client_id_entry.grid(row = 1, column = 1)
    client_id_backspace = Button(initial_entries, bg = '#4B574E', fg = 'white', text = '<<', width = 5, font = ('Candara', '10', 'bold'), borderwidth = 2, command = lambda: entry_backspace('client_id')); client_id_backspace.grid(row = 1, column = 2)
    client_id_confirm = Button(initial_entries, bg = '#4B574E', fg = 'white', text = 'Confirm', width = 10, font = ('Candara', '10', 'bold'), borderwidth = 2, command = lambda: entry_confirmed('client_id')); client_id_confirm.grid(row = 1, column = 3)

    client_secret_label = Label(initial_entries, highlightbackground = '#39473F', highlightthickness = 2, text = 'Enter your Client Secret here :', bg = 'white', fg = 'black', width = 26, font = ('Bahnschrift', '10'), anchor = E); client_secret_label.grid(row = 2, column = 0)
    client_secret_entry = Entry(initial_entries, bg = 'white', fg = 'black', width = 26, font = ('Bahnschrift', '10'), borderwidth = 4, justify = LEFT); client_secret_entry.grid(row = 2, column = 1)
    client_secret_backspace = Button(initial_entries, bg = '#4B574E', fg = 'white', text = '<<', width = 5, font = ('Candara', '10', 'bold'), borderwidth = 2, command = lambda: entry_backspace('client_secret')); client_secret_backspace.grid(row = 2, column = 2)
    client_secret_confirm = Button(initial_entries, bg = '#4B574E', fg = 'white', text = 'Confirm', width = 10, font = ('Candara', '10', 'bold'), borderwidth = 2, command = lambda: entry_confirmed('client_secret')); client_secret_confirm.grid(row = 2, column = 3)

# CREATING THE FRAME, LABELS AND BUTTONS FOR THE BASE WIDGET
base_frame = Frame(base).grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

if temp_icon_path:
    base_image_label = Label(base_frame, image = temp_icon_path, highlightbackground = 'white', highlightthickness = 2, relief = RAISED).grid(row = 0, column = 0, rowspan = 2, padx = 2, pady = 5) if temp_icon_path else None

base_info_label = Label(base_frame, text = 'Spotify Playlist Songs Downloader', width = 30, font = ('Candara', '20', 'bold'), highlightbackground = 'white', highlightthickness = 2, height = 5, relief = RAISED).grid(row = 0, column = 1, padx = 5, pady = 5, columnspan = 2)
base_entry_label = Label(base_frame, text = "Press 'Enter' to proceed further ->", width = 51, font = ('Calibri', '10', 'bold'), highlightbackground = 'white', highlightthickness = 1, height = 1, anchor = E).grid(row = 1, column = 1, padx = 5)
base_entry_button = Button(base_frame, text = 'ENTER', width = 11, font = ('Calibri', '10', 'bold'), bg = '#4B574E', fg = 'white', command = initial_entry); base_entry_button.grid(row = 1, column = 2, padx = 5)

mainloop()
