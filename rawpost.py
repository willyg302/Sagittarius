import webbrowser, httplib, urllib, urllib2, json

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

app = raw_input('App ID: ')
password = raw_input('Password: ')

while True:
    page = raw_input('Target page: ')
    if page == 'exit':
        break
    data = {}
    while True:
        key = raw_input('Key: ')
        if key == '':
            break
        val = raw_input('Value: ')
        data[key] = val

    req = urllib2.Request("http://" + app + ".appspot.com/" + page, urllib.urlencode(data))
    rsp = urllib2.urlopen(req)
    content = rsp.read()
    print content