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

# read json file
def readJson(jsonfile):
    with open(jsonfile) as json_file:
        users = json.load(json_file)
    return users
def getUserByName(name, header):
    # get user id by name
    getUserURI = protocol + "://" + baseurl + createUserurl + "/name/" + name
    r = requests.get(url = getUserURI, headers = header) 
    responseRoleJson = json.loads(r.text)
    return responseRoleJson
    
def updateRole(user, header, userID):
    for role in user["accountRoles"]:
        # get role id by name
        getRoleUserURI = protocol + "://" + baseurl + updateRoleUserURL + "name/" + role.replace(" ", "%20")
        
        r = requests.get(url = getRoleUserURI, headers = header) 
        responseRoleJson = json.loads(r.text)

        # add role to user
        updateRoleUserURI = protocol + "://" + baseurl + updateRoleUserURL + str(responseRoleJson["id"]) + "/users/" + str(userID)
        r = requests.put(url = updateRoleUserURI.replace(" ", "%20"), headers = header) 

# create users in controller
def createUsers(baseurl, protocol, accountName, userName, password, apiClient, apiSecret):
    # get authentication token
    auth_token=gettoken.getToken(accountName, protocol, baseurl,  userName, password, apiClient, apiSecret)

    # get create application url
    createUserURI = protocol + "://" + baseurl + createUserurl
    header = {'Content-Type': 'application/vnd.appd.cntrl+json;v=1', "Authorization": "Bearer %s" %auth_token}
    for user in users["users"]:
        print (user)
        data = {}
        data['name'] = user["name"] 
        data['security_provider_type'] = user["security_provider_type"]
        data['displayName'] = user["displayName"]
        data['password'] = user["password"]
        
        try:
            # create user
            r = requests.post(url = createUserURI, data =json.dumps(data), headers = header) 

            response = r.text
            print("Response is: %s"%response) 
            
            if('id' not in response):
                print("Error in creating users: %s" %users)
            elif('User already present' in response):
                print("User already present. Attempting to update Roles")
                # parse response to valid if application is creates successfully, validate applicationId
                userJson = getUserByName(data['name'], header)
                userID = userJson["id"]
                updateRole(user, header, userID)
            else:
                print ("Successfully created users: %s" %users)
                responseJson = json.loads(response)
                updateRole(user, header, responseJson["id"])

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
   

    jsonfile = "UsersGroupRolesPosts-NFT.json"
    colName = ["name","security_provider_type","displayName","password"]
    createUserurl="/controller/api/rbac/v1/users"
    updateGroupUserURL="/controller/api/rbac/v1/groups/"
    updateRoleUserURL="/controller/api/rbac/v1/roles/"
    baseurl="enterpriseconsolep-vhpaulmateos-hmpczlps.srv.ravcloud.com:8090"
    protocol="http"
    accountName = "customer1"
    userName = "admin"
    password = "appd"
    apiClient = "apiclient"
    apiSecret = "f19aab36-1a9c-483e-9749-a0cc255a0f55"

    # create user
    users = readJson(jsonfile)
    createUsers(baseurl, protocol, accountName, userName, password, apiClient, apiSecret)

