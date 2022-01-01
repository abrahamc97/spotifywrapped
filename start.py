from wrapped import SpotifyHelper

if(__name__ == "__main__"):

    wrapper = SpotifyHelper()
    print("trying to setup spotify api...")
    #sp = createSpotifyEnv(client_id, client_secret)
    print("initialized spotify api")
    ids = wrapper.getPlaylistIds("21")        
    topMonth = wrapper.getMonthWithMostSongs(ids)
    print("top month is " + topMonth)
    
    print("getting all tracks...")
    tracks = wrapper.getAllTracks(ids)
    artistsCount, artistsId = wrapper.getArtists(tracks)
    topFiveArtists = wrapper.getTopFiveArtists(artistsCount, artistsId)
    print("top five artists")
    print(topFiveArtists)
      
    artistStr = []
    for key in artistsId:
        artistStr.append(artistsId[key])

    #print("len of artist list is " + str(len(artistsCount)))

    #print(artistStr)
    topFiveGenre = wrapper.getTopFiveGenres(artistStr)
    print("top five genres...")
    print(topFiveGenre) 

