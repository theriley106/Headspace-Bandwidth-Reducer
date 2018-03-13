import requests

def generateURL(number):
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://my.headspace.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,es-US;q=0.8,es;q=0.6,ru-BY;q=0.4,ru;q=0.2,en;q=0.2',
        'authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU3OTRiZmMzLWY1ZTktNDVhNC04Y2E1LWViNWRkYzkwNDIxZiIsInVzZXJJZCI6IkhTVVNFUl9NQ0dRWUlHNFQ5OEdGQU1XIiwicGxhdGZvcm0iOiJERVNLVE9QIiwic2NvcGUiOlsiVVNFUjpIU1VTRVJfTUNHUVlJRzRUOThHRkFNVyJdLCJwcml2aWxlZ2VzIjpbIlNUQU5EQVJEX0NPTlRFTlQiLCJTVUJTQ1JJQkVSIl0sImlhdCI6MTUyMDkxNTk5ODQ2OCwidjJBcGlLZXkiOiJqK2ZzMS9FTWpJWXlyWGlPYUJaU0JweklDSlFxTDM3SmVDaTR5UG93d3dZPSJ9.FzRMq3xHF306qnhSWZM2OISdOMROi83YvSg9Zn2Pc1Y',
        'Accept': 'application/vnd.api+json',
        'Cache-Control': 'no-cache',
        'X-HS-No-Cache': 'true',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
        'Connection': 'keep-alive',
    }

    params = (
        ('mp3', 'true'),
    )

    response = requests.get('https://api.prod.headspace.com/content/media-items/{}/make-signed-url'.format(number), headers=headers, params=params)
    return response.json()["url"]

def getAllNums():
    listOfIDs = []
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://my.headspace.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,es-US;q=0.8,es;q=0.6,ru-BY;q=0.4,ru;q=0.2,en;q=0.2',
        'authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU3OTRiZmMzLWY1ZTktNDVhNC04Y2E1LWViNWRkYzkwNDIxZiIsInVzZXJJZCI6IkhTVVNFUl9NQ0dRWUlHNFQ5OEdGQU1XIiwicGxhdGZvcm0iOiJERVNLVE9QIiwic2NvcGUiOlsiVVNFUjpIU1VTRVJfTUNHUVlJRzRUOThHRkFNVyJdLCJwcml2aWxlZ2VzIjpbIlNUQU5EQVJEX0NPTlRFTlQiLCJTVUJTQ1JJQkVSIl0sImlhdCI6MTUyMDkxNTk5ODQ2OCwidjJBcGlLZXkiOiJqK2ZzMS9FTWpJWXlyWGlPYUJaU0JweklDSlFxTDM3SmVDaTR5UG93d3dZPSJ9.FzRMq3xHF306qnhSWZM2OISdOMROi83YvSg9Zn2Pc1Y',
        'Accept': 'application/vnd.api+json',
        'Cache-Control': 'no-cache',
        'X-HS-No-Cache': 'true',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'https://my.headspace.com/',
    }

    params = (
        ('activityGroupIds', '0'),
        # Activity group id 0 returns a TON
        ('limit', '1000'),
        # Will return 1000 meditation sessions
        ('page', '0'),
        # Setting this to page 0 by default
    )

    response = requests.get('https://api.prod.headspace.com/content/activities', headers=headers, params=params)
    for i, val in enumerate(response.json()["included"]):
        if val["type"] == "mediaItems":
            if ".mp3" in str(val["attributes"]["filename"]):
                listOfIDs.append(val["id"])
                print("{} / {}".format(i, str(response.json()["included"]).count(".mp3")))
                downloadMP3(generateURL(val["id"]), val["attributes"]["filename"])
                #print("{} - {}".format(val["id"], val["attributes"]["filename"]))
    return listOfIDs

def downloadMP3(mp3URL, mp3File):
    try:
        #return MP3 file name
        #calls it a random file name to later delete
        with open(mp3File, 'wb') as f:
            #this saves the response locally as an actual mp3 file
            f.write(requests.get(mp3URL,timeout=20).content)
        return mp3File
    except:
        pass

if __name__ == '__main__':
    print getAllNums()
    #print generateURL(3659)
