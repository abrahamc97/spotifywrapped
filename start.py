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
    topFiveGenre, genreDict = wrapper.getTopFiveGenres(artistStr)
    print("top five genres...")
    print(topFiveGenre)

    totalMintues = wrapper.getTotalMinutesAdded(tracks)
    print("%d total minutes of music added." % totalMintues)

    uniqueArtists = wrapper.getUniqueArtistsCount(artistsCount)
    print("Number of artists added:", uniqueArtists)

    topContributors = wrapper.getTopContributors(tracks)
    print("Top Contributors:")
    print(topContributors)

    uniqueGenres = wrapper.getUniqueGenresCount(genreDict)
    print("Number of unique genres:", uniqueGenres)

    explicit_users = wrapper.getExplicitContributors(tracks)
    print("Most explicit songs added:")
    print(explicit_users)

    winter_song_features, winter_songs,spring_song_features, spring_songs, summer_song_features, summer_songs, fall_song_features, fall_songs = wrapper.getSeasonFeatures(ids)
    print("Winter Songs", winter_songs)
    print("Winter song features:")
    print(winter_song_features)
    print("Spring Songs", spring_songs)
    print("Spring song features:")
    print(spring_song_features)
    print("Summer Songs", summer_songs)
    print("Summer song features:")
    print(summer_song_features)
    print("Fall Songs", fall_songs)
    print("Fall song features:")
    print(fall_song_features)

    #christin_playlists, jasmine_playlists = wrapper.getCreatorReigns(tracks)
    # print("Christin's playlist features:")
    # print(christin_playlists)
    # print("Jasmine's playlist features:")
    # print(jasmine_playlists)
