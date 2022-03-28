from cgitb import reset
import json
from msilib.schema import AppId
from traceback import print_tb
import requests
import argparse


def fetchPolicyDetails(policyFilePath):
    # Opening JSON file
    f = open(policyFilePath)
    # returns JSON object as
    data = json.load(f)
    # closing JSON file
    f.close()
    return data

def fetchToken(username,password):
    global token
    tokenUrl = "https://anypoint.mulesoft.com/accounts/login"
    headers = {"Content-Type": "application/json","Accept":"application/json"}
    payload = {
        "username": username,
        "password": password
    }   
    try:
        response = requests.post(tokenUrl, headers=headers, json=payload)
        tokenResponse = json.loads(response.content) 
        token = tokenResponse['access_token']
        print("---------------token generated successfully---------------")
        return 1
    except Exception as e:
        print("token generation failed! please check your credentials")
        return 0

def validatePolicy(organizationId,environmentId,apiId):
    policyUrl = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + \
                organizationId + "/environments/"+ environmentId + "/apis/" + apiId + "/policies"
    authorization = "Bearer " + token
    headers = {"Content-Type": "application/json","Authorization":authorization}
    print("validating the policies for appId: ",apiId)
    response = requests.get(policyUrl, headers=headers)
    policyResponse = json.loads(response.content)
    policies = policyResponse['policies']
    if(len(policies)>0):
        print("policies are already applied ! hence skipping this stage")
        return "success4"
    else:
        return 0

def fetchApiId(organizationId,environmentId,assetId):
    global apiId
    status = False
    assetUrl = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + \
                organizationId + "/environments/"+ environmentId + "/apis"
    authorization = "Bearer " + token
    headers = {"Content-Type": "application/json","Authorization":authorization}
    print("fetching apiId for assetId: ",assetId)
    response = requests.get(assetUrl, headers=headers)
    assetsResponse = json.loads(response.content)
    assets = assetsResponse['assets']
    for asset in assets:
        apiDetails = asset['apis']
        apiDetails = apiDetails[0]
        assetName = apiDetails['assetId']
        if(assetName == assetId):
            apiId = apiDetails['id']
            apiId = str(apiId)
            status = True
    if(status):
        print("apiId fetched successfully:- ",apiId)
        return 1
    else:
        print("fetch apiId failed! please check your assetId")
        return 0

def applyPolicy(organizationId,environmentId,apiId,policyDetails):
    policyUrl = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + \
                organizationId + "/environments/"+ environmentId + "/apis/" + apiId + "/policies"
    authorization = "Bearer " + token
    headers = {"Content-Type": "application/json","Authorization":authorization}
    status = False
    for policy in policyDetails[0]:
        policy = json.dumps(policy)
        policy_v = json.loads(policy)
        for payload in policyDetails[1]:
            payload = json.dumps(payload)
            payload_v = json.loads(payload)
            if policy_v['assetId'] == payload_v['assetId'] and policy_v['apply'] == True:
                status =True
                print("applying the policy: ",policy_v['assetId'])
                response = requests.post(policyUrl, headers=headers, json=payload_v)
                        
    if(status):
        print("---------------policies applied successfully---------------") 
        return 1       
    else:
        print("no policy matched!. please check the policy configuration")
        return 0

def main(username,password,policyFilePath,organizationId,environmentId,assetId):
    print("222")
    policyDetails = fetchPolicyDetails(policyFilePath)
    if(fetchToken(username,password)):
        if(fetchApiId(organizationId,environmentId,assetId)):
            if(validatePolicy(organizationId,environmentId,apiId)):
                return "Success"    
            else:
                if(applyPolicy(organizationId,environmentId,apiId,policyDetails)):
                    return "success1"
                else:
                    return "fail1"
        else:
            return "fail2"
    else:
        return "fail3"
    

if __name__ == '__main__':
    print("123")
    parser = argparse.ArgumentParser(description='Apply the policy')
    parser.add_argument('--u', metavar='username', required=True,
                        help='anypoint portal username')
    parser.add_argument('--p', metavar='password', required=True,
                        help='anypoint portal password')
    parser.add_argument('--o', metavar='organizationId', required=True,
                        help='anypoint portal organizations id')
    parser.add_argument('--e', metavar='environmentId', required=True,
                        help='anypoint portal environments id')
    parser.add_argument('--at', metavar='assetId', required=True,
                        help='mule asset id')                                                                                 
    parser.add_argument('--pp', metavar='policyFilePath', required=True,
                        help='policy file location')
    args = parser.parse_args()
    main(username=args.u,password=args.p,organizationId=args.o,environmentId=args.e,assetId=args.at,policyFilePath=args.pp)
    print("1234")
    return("SUCC")
    
