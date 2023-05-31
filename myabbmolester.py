import requests
from typing import Dict, List, Optional


class MyAbbMolester():
    def __init__(self, user_id: str) -> None:
        self.__session_id = None
        self.__user_id = user_id
        self.__did_ping_cup007 = False

    @property
    def session_id(self) -> str:
        if not self.__session_id:
            # acquire a session id
            # A session id is required to validate requests
            # Some requests are checked in a weird fashion
            # but generally, JSESSIONID is a requirement
            # It can be obtained by sending any request to myabb.in/*
            response = requests.get('https://myabb.in')
            if not (j_session_id := response.cookies.get('JSESSIONID')):
                raise Exception("Unable to obtain a cookie")
            self.__session_id = j_session_id
        return self.__session_id

    def __mix_headers(self, headers: Optional[Dict]) -> Dict:
        out_headers = headers or {}
        out_headers['Cookie'] = f"JSESSIONID={self.session_id}"
        return out_headers

    def forgotPassword(self) -> Optional[Dict]:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://myabb.in/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        headers = self.__mix_headers(headers)
        payload = {'Duser': self.__user_id, 'Pwd': ''}
        response = requests.post(
            f'https://myabb.in/ForgotPwrd?userId={self.__user_id}',
            data=payload, 
            headers=headers
        )
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                pass
        return None
            
    def login(self, password: str) -> Optional[Dict]:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://myabb.in/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        headers = self.__mix_headers(headers)
        payload = {'Duser': self.__user_id, 'Pwd': password}
        response = requests.post(
            f'https://myabb.in/loginVal?userId={self.__user_id}', 
            data=payload, 
            headers=headers
        )
        if response.status_code == 200:
            try:
                if (data := response.json):
                    return isinstance(data, List)
            except Exception:
                pass
        return None

    def userInfo(self) -> Optional[Dict]:
        # This is one of those weird reqests I found. The user has to go to 
        # the markup url to receive a redirect with a JWT query param
        # The JWT itself is not required as far as I know, but it
        # has to be generated. Once it's generated, the JSESSSIONID is 
        # allowed to fetch user info
        if not self.__did_ping_cup007:
            self.pingUserInfoForm()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
        headers = self.__mix_headers(headers)
        response = requests.post(
            'https://myabb.in/getsubscriberDetails', 
            headers=headers
        )
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                pass
        return None

    def pingUserInfoForm(self) -> str:
        url = 'https://myabb.in/goToForm?formId=CUP007'
        headers = self.__mix_headers({})
        response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code != 302:  
            raise Exception("Unable to get redirect url")
        redirect_url = response.headers.get('Location')
        self.__did_ping_cup007 = True
        return redirect_url


