import spotipy
from secret import client_id, client_secret, displayNames
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import typing
import operator

class SpotifyHelper():
    def __init__(self):
        self.sp = self.createSpotifyEnv(client_id, client_secret)

    #Authorization and Client Credentials
    def createSpotifyEnv(self, spotify_user_id, spotify_token) -> spotipy.Spotify:
        '''
        @name: createSpotifyEnv
        @param: spotify_user_id - client id
        @param: spotify_token - client secret
        @description: creates the spotify wrapper object and returns it to the program
        '''
        scopes= "user-read-private user-read-email playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-modify user-follow-modify ugc-image-upload"
        sp= spotipy.Spotify(auth_manager=SpotifyOAuth(spotify_user_id, spotify_token,'http://127.0.0.1:5000/spotify/callback', scope=scopes))
        return sp

    def getPlaylistIds(self, query) -> typing.Dict:
        '''
        @name: getPlaylistIds
        @param: sp - the spotify wrapper object to access the api
        @description: query the api for playlists that contain a certain substring
                      and return a list of the playlist ids
        '''
        print("querying for user playlists with string " + query + "...")
        playlistIdList = {}
        playlists = self.sp.current_user_playlists()

        for i in range(0, len(playlists['items'])):
            userInfo = playlists['items'][i]['owner']
            username = userInfo['id']
            # if(query in playlists['items'][i]['name']):
            #     playlistId = playlists['items'][i]['id']
            #     total = playlists['items'][i]['tracks']['total']
            #     miniDict = {}
            #     miniDict['id'] = playlistId
            #     miniDict['num_songs'] = total
            #     playlistIdList[playlists['items'][i]['name']] = miniDict
            #     print("total is " + str(playlists['items'][i]['tracks']['total']))
            displayName = displayNames.get(username)
            if(displayName == 'Christin'):
                playlistId = playlists['items'][i]['id']
                total = playlists['items'][i]['tracks']['total']
                miniDict = {}
                miniDict['id'] = playlistId
                miniDict['num_songs'] = total
                playlistIdList[playlists['items'][i]['name']] = miniDict
                print("total is " + str(playlists['items'][i]['tracks']['total']))
        return playlistIdList


    def getAllTracks(self, playlistIds) -> typing.Dict:
        '''
        @name: getAllTracks
        @param: sp - the spotify wrapper object to access the api
        @param: playlistIds - a list of playlist ids
        @description: returns a dictionary with the key being the name of the playlist and the value being a list of all the items in that playlist
        '''
        tracks = {}
        for key, value in playlistIds.items():
            #print("value is " + str(value['id']))
            tmp = self.sp.playlist_tracks(value['id'], offset=0, market='US', limit=50)
            songs = tmp['items']
            tracks[key] = songs
        return tracks

    def getMonthWithMostSongs(self,playlistIds) -> str:
        '''
        '''
        topMonthName = ""
        topMonthVal = 0
        for key in playlistIds:
            if(playlistIds[key]['num_songs'] > topMonthVal):
                topMonthName = key
                topMonthVal = playlistIds[key]['num_songs']

        return topMonthName

    def getArtists(self, tracks) -> typing.List:
        '''
        '''
        artistCountDict = {}
        artistIdDict = {}
        for key, trackList in tracks.items():
            for i in range(0, len(trackList)):
                curTrack = trackList[i]
                #print(curTrack)
                artistList = curTrack['track']['artists']
                for j in range(0, len(artistList)):
                    #print("----------------")
                    #print(artistList[j])
                    curArtist = artistList[j]
                    if(curArtist['name'] in artistCountDict):
                        artistCountDict[curArtist['name']] += 1
                    else:
                        artistCountDict[curArtist['name']] = 1
                        artistIdDict[curArtist['name']] = curArtist['id']

        return artistCountDict, artistIdDict

    def getTopFiveArtists(self,artistsCount, artistsId) -> typing.Dict:
        '''

        '''
        topFiveArtists = {}
        topArtists = sorted(artistsCount, key=artistsCount.get, reverse=True)[:5]
        for i in range(0, len(topArtists)):
            topFiveArtists[topArtists[i]] = artistsCount[topArtists[i]]

        return topFiveArtists


    def getTopFiveGenres(self, artistStr) -> typing.List[str]:
        '''
        @name: getTopFiveGenres
        @param: sp - the spotify wrapper object to access the api
        @param: artistStr - a list of all the artists (not a string)
        @description: returns a dictionary with the key being the name of the genre and the value being the count of how often those genres appeared in the set of playlists
        '''

        '''
        '''
        artistUriStr = []
        genreDict = {}
        topFiveGenre = {}

        # divide up uri into 50 artist chunk uri's
        for i in range(0, len(artistStr)):
            if(len(artistUriStr) >= 50):
                genreList = self.sp.artists(artistUriStr)
                artistUriStr = []
                artists = genreList['artists']
                for j in range(0, len(artists)):
                    genres = artists[j]['genres']
                    for z in range(0, len(genres)):
                        if(genres[z] in genreDict):
                            genreDict[genres[z]] += 1
                        else:
                            genreDict[genres[z]] = 1
            else:
                artistUriStr.append(artistStr[i])

        topGenres = sorted(genreDict, key=genreDict.get, reverse=True)[:5]
        for i in range(0, len(topGenres)):
            #print(topGenres[i] + " count " + str(genreDict[topGenres[i]]))
            topFiveGenre[topGenres[i]] = genreDict[topGenres[i]]

        return topFiveGenre, genreDict

    def getTotalMinutesAdded(self, tracks) -> int:
        '''
        @name: getTotalMinutesAdded
        @param: sp - the spotify wrapper object to access the api
        @param: ids - a list of all the playlists
        @description: Return the total number of mintues added
        '''
        totalTime = 0
        for key, trackList in tracks.items():
            for i in range(0, len(trackList)):
                curTrack = trackList[i]
                totalTime += curTrack['track']['duration_ms']
        minutes = totalTime/60000
        return minutes


    def getUniqueArtistsCount(self, artistsCount):
        '''
        @name: getUniqueArtistsCount
        @param: sp - the spotify wrapper object to access the api
        @param: artistsCount - dictionary of all the artists added to monthly playlists
        @description: gets the total count of all the unique artists.
        '''
        return len(artistsCount)

    def getTopContributors(self, tracks):
        '''
        @name: getTopContributors
        @param: sp - the spotify wrapper object to access the api
        @param: ids - a list of all the playlists
        @description: returns a dictionary of all the top contributors
        '''
        frequent_users = {}
        for key, trackList in tracks.items():
            for i in range(0, len(trackList)):
                curTrack = trackList[i]
                userId = curTrack['added_by']['id']
                displayName = displayNames.get(userId)
                if displayName in frequent_users:
                    temp = {displayName: frequent_users.get(displayName)+1}
                    frequent_users.update(temp)
                else:
                    frequent_users[displayName] = 1
        sorted_d = dict( sorted(frequent_users.items(), key=operator.itemgetter(1),reverse=True))
        return sorted_d

    def getPlaylistsByCreatedBy(self):
        '''
        @name: getPlaylistsByCreatedBy
        @description: returns a list of all the playlist ids based on the user that had created them. This function should be able to search for playlists created by multiple users.
        '''
        return

    def getUniqueGenresCount(self, genreDict):
        '''
        @name: getUniqueGenresCount
        @param: sp - the spotify wrapper object to access the api
        @param: genreDict - dictionary of all the genres added to monthly playlists
        @description: gets the total count of all the unique genres.
        '''
        return len(genreDict)

    def getSeasonFeatures(self, ids):
        '''
        @name: getSeasonFeatures
        @param: sp - the spotify wrapper object to access the api
        @param: ids - a list of all the playlists
        @description: returns a dictionary of songs features for each season
            (currently limited to liveness, danceability and valence)
        '''
        fall_songs = 0
        fall_song_features = {}
        summer_songs = 0
        summer_song_features = {}
        spring_songs = 0
        spring_song_features = {}
        winter_songs = 0
        winter_song_features = {}
        for i in ids:
            playlistId = ids[i]['id']
            playlistInfo = self.sp.playlist_items(playlistId, fields=None, limit=100, offset=0, market='US', additional_types=('track',))
            track_id = []
            added_at = playlistInfo['items'][0]['added_at']
            playlistMonth = int(added_at[5:7])
            for idx, tracks in enumerate(playlistInfo['items']):
                #track_id[idx] = playlistInfo['items'][idx]['track']['id']
                track_id.append(playlistInfo['items'][idx]['track']['id'])
            if (playlistMonth == 12 or playlistMonth == 1 or playlistMonth == 2):
                winter_song_features, winter_songs = self.getSpecificFeatures(track_id, winter_song_features, winter_songs)
            elif (playlistMonth == 3 or playlistMonth == 4 or playlistMonth == 5):
                spring_song_features, spring_songs = self.getSpecificFeatures(track_id, spring_song_features, spring_songs)
            elif (playlistMonth == 6 or playlistMonth == 7 or playlistMonth == 8):
                summer_song_features, summer_songs = self.getSpecificFeatures(track_id, summer_song_features, summer_songs)
            elif (playlistMonth == 9 or playlistMonth == 10 or playlistMonth == 11):
                fall_song_features, fall_songs = self.getSpecificFeatures(track_id, fall_song_features, fall_songs)

        average_danceability = round(winter_song_features.get('danceability')/winter_songs,4)
        winter_song_features.update({'danceability': average_danceability})
        average_energy = round(winter_song_features.get('energy')/winter_songs,4)
        winter_song_features.update({'energy': average_energy})
        average_liveness = round(winter_song_features.get('liveness')/winter_songs,4)
        winter_song_features.update({'liveness': average_liveness})
        average_valence = round(winter_song_features.get('valence')/winter_songs,4)
        winter_song_features.update({'valence': average_valence})

        average_danceability = round(spring_song_features.get('danceability')/spring_songs,4)
        spring_song_features.update({'danceability': average_danceability})
        average_energy = round(spring_song_features.get('energy')/spring_songs,4)
        spring_song_features.update({'energy': average_energy})
        average_liveness = round(spring_song_features.get('liveness')/spring_songs,4)
        spring_song_features.update({'liveness': average_liveness})
        average_valence = round(spring_song_features.get('valence')/spring_songs,4)
        spring_song_features.update({'valence': average_valence})

        average_danceability = round(summer_song_features.get('danceability')/summer_songs,4)
        summer_song_features.update({'danceability': average_danceability})
        average_energy = round(summer_song_features.get('energy')/summer_songs,4)
        summer_song_features.update({'energy': average_energy})
        average_liveness = round(summer_song_features.get('liveness')/summer_songs,4)
        summer_song_features.update({'liveness': average_liveness})
        average_valence = round(summer_song_features.get('valence')/summer_songs,4)
        summer_song_features.update({'valence': average_valence})

        average_danceability = round(fall_song_features.get('danceability')/fall_songs,4)
        fall_song_features.update({'danceability': average_danceability})
        average_energy = round(fall_song_features.get('energy')/fall_songs,4)
        fall_song_features.update({'energy': average_energy})
        average_liveness = round(fall_song_features.get('liveness')/fall_songs,4)
        fall_song_features.update({'liveness': average_liveness})
        average_valence = round(fall_song_features.get('valence')/fall_songs,4)
        fall_song_features.update({'valence': average_valence})

        return winter_song_features, winter_songs, spring_song_features, spring_songs, summer_song_features, summer_songs, fall_song_features, fall_songs

    def getSpecificFeatures(self,track_id, song_features, songs):
        '''
        @name: getSpecificFeatures
        @param: sp - the spotify wrapper object to access the api
        @param: track_id - track ids for a specific playlist
        @param: song_features - a dictionary that holds the average features for a specific season
        @param: songs - number of songs for that specific season
        @description: Track ids from each playlist are passed in the audio features are added to
            dictionaries
        '''
        songs += len(track_id)
        #print(songs)
        track_features = self.sp.audio_features(tracks=track_id)
        for i in track_features:
            if 'danceability' in song_features:
                sum = song_features.get('danceability')+i['danceability']
                song_features.update({'danceability': sum})
            else:
                song_features['danceability'] = i['danceability']
            if 'energy' in song_features:
                sum = song_features.get('energy')+i['energy']
                song_features.update({'energy': sum})
            else:
                song_features['energy'] = i['energy']
            if 'liveness' in song_features:
                sum = song_features.get('liveness')+i['liveness']
                song_features.update({'liveness': sum})
            else:
                song_features['liveness'] = i['liveness']
            if 'valence' in song_features:
                sum = song_features.get('valence')+i['valence']
                song_features.update({'valence': sum})
            else:
                song_features['valence'] = i['valence']
        return song_features, songs

    def getExplicitContributors(self, tracks):
        '''
        @name: getExplicitContributors
        @param: sp - the spotify wrapper object to access the api
        @param: track_id -
        @description: Return a dictionary about the top contributors who added explicit songs
        '''
        explicit_users = {}
        for key, trackList in tracks.items():
            for i in range(0, len(trackList)):
                curTrack = trackList[i]
                explicit = curTrack['track']['explicit']
                #print(artistList)
                if explicit == True:
                    userId = curTrack['added_by']['id']
                    displayName = displayNames.get(userId)
                    if displayName in explicit_users:
                        temp = {displayName: explicit_users.get(displayName)+1}
                        explicit_users.update(temp)
                    else:
                        explicit_users[displayName] = 1
        sorted_d = dict( sorted(explicit_users.items(), key=operator.itemgetter(1),reverse=True))
        return sorted_d

    def getCreatorReigns(self, ids):
        '''
        @name: get getCreatorReign
        @param: sp - the spotify wrapper object to access the api
        @param: tracks - all the track items of the playlists
        @description: Return a dictionary of average audio features for both playlist creators
        '''
        christin_songs = 0
        christin_playlists = {}
        jasmine_songs = 0
        jasmine_playlists = {}
        for i in ids:
            track_id = []
            playlistId = ids[i]['id']
            playlistInfo = self.sp.playlist(playlistId, fields=None, market='US', additional_types=('track', ))
            track_id = []
            userId = playlistInfo['owner']['id']
            displayName = displayNames.get(userId)
            tracks = playlistInfo['tracks']['items']
            for i in range(0, len(tracks)):
                curTrackId = tracks[i]['track']['id']
                track_id.append(curTrackId)
            if displayName == 'Christin':
                christin_playlists, christin_songs = self.getSpecificFeatures(track_id, christin_playlists, christin_songs)
            elif displayName == 'Jasmine':
                jasmine_playlists, jasmine_songs = self.getSpecificFeatures(track_id, jasmine_playlists, jasmine_songs)
        average_danceability = round(christin_playlists.get('danceability')/christin_songs,4)
        christin_playlists.update({'danceability': average_danceability})
        average_energy = round(christin_playlists.get('energy')/christin_songs,4)
        christin_playlists.update({'energy': average_energy})
        average_liveness = round(christin_playlists.get('liveness')/christin_songs,4)
        christin_playlists.update({'liveness': average_liveness})
        average_valence = round(christin_playlists.get('valence')/christin_songs,4)
        christin_playlists.update({'valence': average_valence})

        average_danceability = round(jasmine_playlists.get('danceability')/jasmine_songs,4)
        jasmine_playlists.update({'danceability': average_danceability})
        average_energy = round(jasmine_playlists.get('energy')/jasmine_songs,4)
        jasmine_playlists.update({'energy': average_energy})
        average_liveness = round(jasmine_playlists.get('liveness')/jasmine_songs,4)
        jasmine_playlists.update({'liveness': average_liveness})
        average_valence = round(jasmine_playlists.get('valence')/jasmine_songs,4)
        jasmine_playlists.update({'valence': average_valence})

        return christin_playlists, jasmine_playlists
