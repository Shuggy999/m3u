from flask import Flask, redirect, request, Response
import requests
import base64
import json
import requests

app = Flask(__name__)

@app.route('/itvx')
def itvredirect():

    channel = request.args.get('channel', 'ITV')  # Default to 'ITV' if no channel is provided

    # ITV

    proxies = {
        'http': 'http://localhost:8080',
        'https': 'http://localhost:8080',
    }

    cookies = {
        'SyrenisCookieFormConsent_Itv.Session': '{"tokens":{"content":{"entitlement":{"purchased":[],"source":"","failed_availability_checks":[]},"email_verified":true,"token_type":"bearer","missingUserData":["NoPlanSelected"]}}',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'application/vnd.itv.online.playlist.sim.v3+json',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://www.itv.com/',
        'Origin': 'https://www.itv.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = '{"user":{"itvUserId":"{4f129513-1f5b-4dc9-8a2a-b6434e93c938}","entitlements":[],"profile_id":"{4f129513-1f5b-4dc9-8a2a-b6434e93c938}_0"},"device":{"manufacturer":"Firefox","model":"126.0","os":{"name":"Mac OS","version":"10.15","type":"desktop"}},"client":{"version":"4.1","id":"browser","supportsAdPods":true,"service":"itv.x","appversion":"2.228.2"},"variantAvailability":{"player":"dash","featureset":{"min":["mpeg-dash","widevine"],"max":["mpeg-dash","widevine"]},"platformTag":"dotcom"}}'

    response = requests.post(
        f'https://simulcast.itv.com/playlist/itvonline/{channel}',
        cookies=cookies,
        headers=headers,
        data=data,
        proxies=proxies,
    ).json()

    url = response['Playlist']['Video']['VideoLocations'][0]['Url']
    return redirect(url)

@app.route('/livingabroadtv')
def livingabroadtvplaylist():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://livingabroad.tv/',
        'Content-Type': 'application/json',
        'Origin': 'https://livingabroad.tv',
    }

    json_data = {
        'data': None,
    }

    response = requests.post(
        'https://us-central1-speedy-district-332216.cloudfunctions.net/getChannels',
        headers=headers,
        json=json_data,
    ).json()

    m3uplaylist = '#EXTM3U\n\n'

    for channel in response['result']['channels']:
        m3uplaylist += f'#EXTINF:-1 tvg-id="{channel["epg_tag"]}" tvg-logo="{channel["imageUrl"]}",{channel["title"]}\n{channel["url"]}\n\n'

    return Response(m3uplaylist, mimetype='audio/x-mpegurl')

@app.route('/skyit')
def skyitredirect():

    channel = request.args.get('channel', 1)


    params = {
        'id': f'{channel}',
        'isMobile': 'false',
    }

    response = requests.get(f'https://apid.sky.it/vdp/v1/getLivestream', params=params).json()

    url = response["streaming_url"]
    return redirect(url)


@app.route('/allsport')
def allsportplaylist():
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Authorization': 'Bearer terimkc-bsdk-mhdtvworld-69gay420bsdk69gay420bsdk69copycat420bsdk69gay69terimkc',
    }

    response = requests.get(
        'https://allsport.games/api/hi-chutiye-mhdtvworld-gay-teri-mkc-ab-to-copy-mat-kar-bsdk-chutiye',
        headers=headers,
    ).json()

    channels = base64.b64decode(response["data"]).decode("utf8")

    channelsarr = json.loads(channels)

    m3uplaylist = '#EXTM3U\n\n'

    for channel in channelsarr:
        if channel['license_key'] == '':
            m3uplaylist += f'#EXTINF:-1,{channel["name"]}\n{channel["url"]}\n\n'
        else:
            m3uplaylist += f'#EXTINF:-1,{channel["name"]}\n#KODIPROP:inputstream.adaptive.license_type=clearkey\n#KODIPROP:inputstream.adaptive.license_key={channel['license_key']}:{channel['license_key2']}\n{channel["url"]}\n\n'

    return Response(m3uplaylist, mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(debug=True, port=1984)