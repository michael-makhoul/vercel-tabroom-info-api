#os, requests
import os
import requests

payload = {
    'username': os.environ.get('USERNAME'),
    'password': os.environ.get('PASSWORD')

}
login_session = requests.Session()
login_session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0'
 })
# must prevent redirects in order to extract cookie
login_response = login_session.post('https://www.tabroom.com/user/login/login_save.mhtml', data=payload, allow_redirects=False)
cookie = login_response.headers.get('set-cookie')
    
os.environ['TABROOM_COOKIE'] = cookie

print("Cookie:", cookie)
