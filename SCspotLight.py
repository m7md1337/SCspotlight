import requests
import re
import json
import os.path
import time
from bs4 import BeautifulSoup
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto import Random
from base64 import *
import subprocess


class wrongoption(Exception):
    pass


class userwrong(Exception):
    pass


class passerror(Exception):
    pass


class badtoken(Exception):
    pass


class smscode(Exception):
    pass


class somthingelse(Exception):
    pass

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-select_streams",
                             "v", "-show_entries", "stream=width,height,duration", "-of",
                             "json", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    df = json.loads(result.stdout.decode())
    wi = df["streams"][0]["width"]
    hig = df["streams"][0]["height"]
    durat = df["streams"][0]["duration"]
    return wi, hig, durat

def encrypt(message, key_size=256):
    message = pad(message, AES.block_size)
    iv = Random.new().read(AES.block_size)
    key = os.urandom(32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # return data file with encrypted data.
    return {"enc": cipher.encrypt(message), "key": b64encode(key), "iv": b64encode(iv)}




def getCaptchToken():
    recaptcha_regex = re.compile(r'value="(.*?)">\n<script')

    header33 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Host": "www.google.com",
        "Pragma": "no-cache"}
    r = requests.get(
        'https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LezjdAZAAAAAD1FaW81QpkkplPNzCNnIOU5anHw&co=aHR0cHM6Ly9hY2NvdW50cy5zbmFwY2hhdC5jb206NDQz&hl=en&v=ecapuzyywmdXQ5gJHS3JQiXe&size=invisible&badge=inline&cb=dkb4t8ooxnw2',
        headers=header33)
    match = recaptcha_regex.search(r.text)
    recaptcha_token = match.group(1)
    dd = "".join(recaptcha_token)
    return dd


def GetReload():
    url = "https://www.google.com/recaptcha/api2/reload?k=6LezjdAZAAAAAD1FaW81QpkkplPNzCNnIOU5anHw"
    data = "c=" + getCaptchToken() + "&reason=q&k=6LezjdAZAAAAAD1FaW81QpkkplPNzCNnIOU5anHw&co=aHR0cHM6Ly9hY2NvdW50cy5zbmFwY2hhdC5jb206NDQz&hl=en&v=ecapuzyywmdXQ5gJHS3JQiXe&size=invisible&badge=inline&cb=dkb4t8ooxnw2"

    header33 = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1",
        "Host": "www.google.com",
        "Content-Type": "application/x-www-form-urlencoded", "origin": "https://www.google.com",
        "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin"}

    req = requests.post(url, data=data, headers=header33)
    ff = "".join(req.text)
    ffff = json.loads(ff.replace(")]}'", ''))
    return ffff[1]


def Loginweb(Username, Password):
    get_cokeis = requests.get("https://accounts.snapchat.com/accounts/login?client_id=story-studio-lite--prod")
    token = get_cokeis.cookies['xsrf_token']
    webclientid = get_cokeis.cookies['web_client_id']
    Header_login = {"Host": "accounts.snapchat.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
                    "Content-Type": "application/x-www-form-urlencoded", "Connection": "close",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "origin": "https://accounts.snapchat.com",
                    "referer": "https://accounts.snapchat.com/",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "sec-gpc": "1",
                    "upgrade-insecure-requests": "1"}
    cookies_login = {'xsrf_token': token, "sc-cookies-accepted": "true", "Preferences": "true",
                     "Performance": "true", "Marketing": "true", "sc-a-csrf": "true", "web_client_id": webclientid}
    capctha = GetReload()
    data_post = "username={}&password={}&xsrf_token={}&continue=%2Faccounts%2Fwelcome&g-recaptcha-response={}&g-recaptcha-response={}".format(
        Username, Password, token, capctha, capctha)
    # print(data_post) # for debug just
    reqlogin = requests.post("https://accounts.snapchat.com/accounts/login", data=data_post, headers=Header_login,
                             cookies=cookies_login, allow_redirects=False)
    if "That&#39;s not the right password." in reqlogin.text:
        raise passerror()

    elif "Cannot find the user" in reqlogin.text:
        raise userwrong()

    elif "__Host-sc-a-session" in reqlogin.cookies:

        tokenauth = GetToken(reqlogin.cookies["__Host-sc-a-session"], reqlogin.cookies["sc-a-nonce"])

        env = {"__Host-sc-a-session": reqlogin.cookies["__Host-sc-a-session"],
               " sc-a-nonce": reqlogin.cookies["sc-a-nonce"], "token": tokenauth[1]}
        config = open(".envspot", "w")
        js = json.dumps(env)
        config.write(js)
        config.close()
        return tokenauth[1]

    elif "/accounts/login/tfa" in reqlogin.headers["Location"]:
        url = reqlogin.headers["Location"]
        smsreu = requests.get(url)
        ntoken = smsreu.cookies["xsrf_token"]
        soup2 = BeautifulSoup(smsreu.text, 'html.parser')
        authsmscode = input("enterthe code: ")
        cookies_sms = {'xsrf_token': ntoken, "sc-cookies-accepted": "true", "Preferences": "true",
                       "Performance": "true", "Marketing": "true", "sc-a-csrf": "true", "web_client_id": webclientid}
        urlsms = "https://accounts.snapchat.com/accounts/login/tfa?tfa_requirements=" + soup2.find_all('div')[1][
            "data-tfa-requirements"] + "&continue=https%3A%2F%2Faccounts.snapchat.com%2Faccounts%2Fwelcome"
        datasms = "tfa_code=" + authsmscode + "&action=verify&tfa_mechanism=sms&tfa_requirements=" + \
                  soup2.find_all('div')[1]["data-tfa-requirements"] + "&xsrf_token=" + ntoken + "&pre_auth_token=" + \
                  soup2.find_all('div')[1][
                      "data-pre-auth-token"] + "&continue=https%3A%2F%2Faccounts.snapchat.com%2Faccounts%2Fwelcome&sms_enabled=true"
        print(urlsms, datasms)
        resms = requests.post(urlsms, data=datasms, headers=Header_login, cookies=cookies_sms, allow_redirects=False)
        print(resms.text, resms.headers, resms.cookies, resms.status_code)
        if "__Host-sc-a-session" in resms.cookies:

            tokenauth = GetToken(resms.cookies["__Host-sc-a-session"], resms.cookies["sc-a-nonce"])
            env = {"__Host-sc-a-session": resms.cookies["__Host-sc-a-session"],
                   " sc-a-nonce": resms.cookies["sc-a-nonce"], "token": tokenauth[1]}
            config = open(".envspot", "w")
            js = json.dumps(env)
            config.write(js)
            config.close()
            return tokenauth[1]
        else:
            raise smscode()

    else:
        raise somthingelse()
        # print(reqlogin.text,reqlogin.headers,reqlogin.status_code)
        # print(reqlogin.text,reqlogin.headers,reqlogin.cookies,reqlogin.status_code)
    # print({reqlogin.cookies["__Host-sc-a-session"], reqlogin.cookies["sc-a-nonce"]})


def GetToken(H_session, H_nonce):
    # GET TOKEN AFTER LOGIN BY TWO HEADERS
    url = "https://accounts.snapchat.com/accounts/sso?client_id=story-studio-lite--prod"
    header = {'Connection': 'close',
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}

    cookie = {'__Host-sc-a-session': H_session, "sc-a-nonce": H_nonce}
    re = requests.get(url=url, headers=header, cookies=cookie, allow_redirects=False)
    token = "".join(str(re.headers['Location']))
    return token.split("https://my.snapchat.com/?ticket=")  # RETURN THE DATA RESPONSE THAT CONTAINT TOKEN


def GetcheckToken(token):
    re1Url = "https://us-east1-aws.api.snapchat.com/gravy-gateway/graphql"
    data = {"operationName": "GetUploadUrl", "variables": {},
            "query": "query GetUploadUrl {\n  uploadUrl {\n    uploadUrl\n    contentObjectBase64\n    __typename\n  }\n}\n"}
    header = {'Connection': 'close',
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
              "content-type": "application/json",
              "authorization": "Bearer " + token + ""}  # token we get it from GetToken after successful login

    re1 = requests.post(url=re1Url, json=data,
                        headers=header)  # req1 that's gave us the UploadUrl and contentObjectBase64
    if "unauthorized" not in re1.text:
        return "good"
    else:
        return "bad"


def main():
    if os.path.exists(".envspot"):
        fg = open(".envspot", "r")
        env = json.load(fg)
        token = env["token"]
        if GetcheckToken(token) == "good":
            print("[++]ur session still work ")
        else:

            check = input("[++]for login enter 1 if u have token enter 2 :")
            if check == "1":
                user = input("[+]enter the username: ")
                passU = input("[+]enter the password: ")
                Loginweb(user, passU)
            elif check == "2":
                tokeninput = input("[+]enter token :")
                h = GetcheckToken(tokeninput)
                if h == "good":
                    env = {"token": tokeninput}
                    a_file = open(".envspot", "w")
                    js = json.dumps(env)
                    a_file.write(js)
                    a_file.close()

                elif h == "bad":

                    raise badtoken()
            else:
                raise wrongoption()

    else:
        check = input("[++]for login enter 1 if u have token enter 2 :")
        if check == "1":
            user = input("[+]enter the username: ")
            passU = input("[+]enter the password: ")
            Loginweb(user, passU)
        elif check == "2":
            tokeninput = input("[+]enter token :")
            h = GetcheckToken(tokeninput)
            if h == "good":
                env = {"token": tokeninput}
                a_file = open(".envspot", "w")
                js = json.dumps(env)
                a_file.write(js)
                a_file.close()

            elif h == "bad":

                raise badtoken()
        else:
            raise wrongoption()


def uploadVideo(token, file):
    # this function must be in sequence
    # get data auth for upload video on the server by graphql
    re1Url = "https://us-east1-aws.api.snapchat.com/gravy-gateway/graphql"
    data = {"operationName": "GetUploadUrl", "variables": {},
            "query": "query GetUploadUrl {\n  uploadUrl {\n    uploadUrl\n    contentObjectBase64\n    __typename\n  }\n}\n"}
    header = {'Connection': 'close',
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
              "content-type": "application/json",
              "authorization": "Bearer " + token + ""}  # token we get it from GetToken after successful login

    re1 = requests.post(url=re1Url, json=data,
                        headers=header)  # req1 that's gave us the UploadUrl and contentObjectBase64
    lj = json.loads(re1.content)  # load json from response data to get value of keys
    UploadUrl = lj["data"]['uploadUrl']['uploadUrl']
    contentObjectBase64 = lj["data"]['uploadUrl']['contentObjectBase64']
    width, highe, timems = get_length(file)
    fileread = open(file, "rb")  # actually isn't a file its a video
    enc = encrypt(fileread.read())
    iv = enc["iv"].decode("utf8")
    key = enc["key"].decode("utf8")
    hh  = {'Connection': 'keep-alive',
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1",
                    "Content-Type": "application/octet-stream"}
    re2 = requests.put(url=UploadUrl, headers=hh, data=enc["enc"])
    if re2.status_code == 200:  # to submit the video and make sure the video uploaded successfully
        url3 = "https://us-east1-aws.api.snapchat.com/gravy-gateway/graphql"  # now we will send request to confirm and  share the video
        data3 = {"operationName": "PostSpotlightSnap", "variables": {
            "media": {"height": highe, "width": width, "durationMs": round(float(timems) * 1000),
                      "contentObjectBase64": contentObjectBase64 , "ivBase64": iv,
                      "keyBase64": key, "hasSound": True,
                      "mediaCaptureTimestampMs": 0, "topics": []}, "createHighlight": False, "locale": "en-US"},
                 "query": "mutation PostSpotlightSnap($media: Media!, $createHighlight: Boolean!, $locale: String!) {\n  postSpotlightSnap(\n    media: $media\n    createHighlight: $createHighlight\n    locale: $locale\n  ) {\n    id\n    __typename\n  }\n}\n"}
        header3 = {'Connection': 'close',
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
                   "content-type": "application/json",
                   "authorization": "Bearer " + token + ""}  # token we get it from GetToken after successful login
        re3 = requests.post(url=url3, json=data3, headers=header3)
        if "__typename" in re3.text:
            print("upload success")
        elif "TooManyRequestsError:" in re3.text :
            print("TooManyRequestsError wait 20 seconds ")
            time.sleep(20)
        else:
            print("error when submit the upload ")
    else:
        print("error before upload")


if __name__ == '__main__':
    try:
        main()
        print("[++]good we will continue")
        files = input("[++]but the full pathe of videos (if videos in dir vids enter vids : ")
        token = json.load(open(".envspot"))
        lengg = os.listdir(files)
        times = input("[++]how many times upload the video: ")
        for dx in lengg * int(times):
            uploadVideo(token["token"], files + "/" + dx)
            time.sleep(61)
        print("[**]  finshed ")




    except badtoken:
        print("[--]u enter bad token try another way")

    except smscode:
        print("[--]u enter wrong sms code")

    except passerror:
        print("[--]u enter  wrong  password")

    except somthingelse:
        print("[---]somthing wrong try again")
    except userwrong:
        print("[oops]we cannot find username")
    except wrongoption:
        print("[oops]enter wrong option")
