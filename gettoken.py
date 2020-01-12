#!/usr/bin/python
import urllib.request, urllib.parse
import json, re, sys, base64

def getToken(acc,prot,url,usr,pswd, client, secret):
	# Get url, username and password
	account = acc
	protocol = prot
	baseurl = url
	username = usr
	passwd = pswd
	client_id=client+"@"+account
	client_secret=secret

	# Call oauth Url to get token
	values = {'grant_type': 'client_credentials', 'client_id': client_id,
			  'client_secret':client_secret}
	postdata = urllib.parse.urlencode(values)
	postdata = postdata.encode('ascii')  # data should be bytes
	urlstr = protocol + "://" + baseurl + "/controller/api/oauth/access_token"
	print(urlstr)
	authstr = username + "@" + account + ":" + passwd
	enc_authstr=base64.b64encode(authstr.encode("utf-8")).decode("ascii")
	req = urllib.request.Request(urlstr, postdata, {"Authorization": "Basic %s" % enc_authstr})
	req.add_header('Content-Type', 'application/vnd.appd.cntrl+protobuf;v=1')
	print(req.header_items())
	print(req.data)
	token_data={}
	try:
	 response = urllib.request.urlopen(req)
	 #print(response.read())
	 token_data= json.loads(response.read())
	 print(token_data)
	except Exception as e:
	 print(str(e))
	 
	return(str(token_data['access_token']))
	
if __name__ == "__main__":
    print(getToken("customer1", "http", "platform-apacjantrainbp2arp-xwrpidox.srv.ravcloud.com:8090",  "appd", "appd", "Test",'c3ab681f-9403-47a2-b41c-eca935092393'))


