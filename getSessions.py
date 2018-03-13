import requests
def getAllURLs():
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
        ('activityGroupIds', '124'),
        ('limit', '100'),
        ('page', '0'),
    )

    response = requests.get('https://api.prod.headspace.com/content/activities', headers=headers, params=params)
    for val in response.json()["included"]:
        if val["type"] == "mediaItems":
            if ".mp3" in str(val["attributes"]["filename"]):
                print("{} - {}".format(val["id"], val["attributes"]["filename"]))


getAllURLs()
