from cgitb import reset
import json
from msilib.schema import AppId
from traceback import print_tb

import argparse

def fetchPolicyDetails(policyFilePath):
    # Opening JSON file
    f = open(policyFilePath)
    # returns JSON object as
    data = json.load(f)
    # closing JSON file
    f.close()
    return data

def main(username,password,policyFilePath,organizationId,environmentId,assetId):
    print(username)
    return 0

if __name__ == '__main__':
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

    

