import spotipy
from secret import client_id, client_secret
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import typing

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
            if(query in playlists['items'][i]['name']):
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
            tmp = self.sp.playlist_tracks(value['id'], offset=0, limit=50)
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

        return topFiveGenre

    def getTotalMinutesAdded(tracks) -> int:
        '''
        '''
        return

    def getUniqueArtistsCount(self):
        '''
        @name: getUniqueArtistsCount
        @description: gets the total count of all the unique artists. Probably an easy way to get is to take the return of getArtists as an input and just return the length of the list
        '''
        return
    
    def getTopContributors(self):
        '''
        @name: getTopContributors
        @description: returns a list of all the top contributors 
        '''
        return

    def getPlaylistsByCreatedBy(self):
        '''
        @name: getPlaylistsByCreatedBy
        @description: returns a list of all the playlist ids based on the user that had created them. This function should be able to search for playlists created by multiple users.
        '''
        return

    def getUniqueGenresCount(self):
        '''
        @name: getUniqueGenresCount
        @description: gets the total count of all the unique genres.
        '''
        return

