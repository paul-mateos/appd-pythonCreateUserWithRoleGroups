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
            r = requests.post(url = createUserURI, data =json.dumps(data), headers = header) 

            response = r.text
            print("Response is: %s"%response) 
            
            # parse response to valid if application is creates successfully, validate applicationId
            responseJson = json.loads(response)
            if('id' not in responseJson):
                print("Error in creating users: %s" %users)

            else:
               print ("Successfully created users: %s" %users)
               for group in user["groups"]:
                    # get group id by name
                    getGroupUserURI = protocol + "://" + baseurl + updateGroupUserURL + "name/" + group.replace(" ", "%20")
                    r = requests.get(url = getGroupUserURI, headers = header) 
                    responseGroupJson = json.loads(r.text)

                    # add user to group
                    updateGroupUserURI = protocol + "://" + baseurl + updateGroupUserURL + str(responseGroupJson["id"]) + "/users/" + str(responseJson["id"])
                    r = requests.put(url = updateGroupUserURI, headers = header) 
               for role in user["accountRoles"]:
                    # get role id by name
                    getRoleUserURI = protocol + "://" + baseurl + updateRoleUserURL + "name/" + role.replace(" ", "%20")
                    
                    r = requests.get(url = getRoleUserURI, headers = header) 
                    responseRoleJson = json.loads(r.text)

                    # add role to user
                    updateRoleUserURI = protocol + "://" + baseurl + updateRoleUserURL + str(responseRoleJson["id"]) + "/users/" + str(responseJson["id"])
                    r = requests.put(url = updateRoleUserURI.replace(" ", "%20"), headers = header) 


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
    baseurl="platform-apacjantrainbp2arp-xwrpidox.srv.ravcloud.com:8090"
    protocol="http"
    accountName = "customer1"
    userName = "appd"
    password = "appd"
    apiClient = "Test"
    apiSecret = "c3ab681f-9403-47a2-b41c-eca935092393"

    # create user
    users = readJson(jsonfile)
    createUsers(baseurl, protocol, accountName, userName, password, apiClient, apiSecret)

