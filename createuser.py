# AppDynamics Legal Disclosure
#
# THE SCRIPT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SCRIPT OR THE USE OR
# OTHER DEALINGS IN THE SCRIPT.
#
#
# Author:  Arpita.Agarwal@appdynamics.com
# 

import sys
import requests
import json
import readcsv
import gettoken




# get users from csv
def getUserNames(fileName, colList):
    # read csv file
    users = readcsv.readCSV(fileName, colList)
    return users

# create users in controller
def createUsers(baseurl, protocol, accountName, userName, password, apiClient, apiSecret):
    # get authentication token
    auth_token=gettoken.getToken(accountName, protocol, baseurl,  userName, password, apiClient, apiSecret)

    # get create application url
    createUserURI = protocol + "://" + baseurl + createUserurl
    header = {'Content-Type': 'application/vnd.appd.cntrl+json;v=1', "Authorization": "Bearer %s" %auth_token}
    for user in users:
        print ("Creating user: %s" %user)
        
        try:
            r = requests.post(url = createUserURI, data =json.dumps(user), headers = header) 

            response = r.text
            print("Response is: %s"%response) 
            
            # parse response to valid if application is creates successfully, validate applicationId
            responseJson = json.loads(response)
            if('id' not in responseJson):
                print("Error in creating users: %s" %users)
            else:
               print ("Successfully created users: %s" %users)

        except Exception as e:
            print(str(e))
            raise Exception("Exception in creating users:")
            exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        fileName = sys.argv[0]
        print ("FileName = %s" % (fileName))
    else:
        print ("Usage: python creatuser.py <fileName>")
        exit(0)
   

    csvfile = "Users-NFT.csv"
    colName = ["name","security_provider_type","displayName","password"]
    createUserurl="/controller/api/rbac/v1/users"
    baseurl="platform-apacjantrainbp2arp-xwrpidox.srv.ravcloud.com:8090"
    protocol="http"
    accountName = "customer1"
    userName = "appd"
    password = "appd"
    apiClient = "Test"
    apiSecret = "c3ab681f-9403-47a2-b41c-eca935092393"

    #create users from CSV
    users = getUserNames(csvfile, colName)
    createUsers(baseurl, protocol, accountName, userName, password, apiClient, apiSecret)

