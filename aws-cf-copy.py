import json
import os
import argparse

def confirm(id):
    print("")
    for i, origin in enumerate( outOrigins ):
        print( str(i)+" - "+origin )
    mappedId = int(input("What origin you want to use for "+id+"?"))
    originsMap[id] = outOrigins[mappedId]
    return

parser = argparse.ArgumentParser(description='Copy CloudFront behaviors between distributions')
parser.add_argument('src', metavar='src', type=str,
                    help='source CF distribution')
parser.add_argument('target', metavar='target', type=str,
                    help='target CF distribution')                    
'''
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
'''

args = parser.parse_args()

srcDistribution = args.src
cfSrcFileName = "cf_src.json"
targetDistribution = args.target

# load the src distribution config from AWS
#os.system("aws cloudfront get-distribution-config --id "+srcDistribution+" > "+cfSrcFileName)
cfSrcStr = os.popen("aws cloudfront get-distribution-config --id "+srcDistribution).read()
cfSrc = json.loads(cfSrcStr)['DistributionConfig'].copy()


# load targer distribution configuration
cfOutStr = os.popen("aws cloudfront get-distribution-config --id "+targetDistribution).read()
cfOutOrig = json.loads(cfOutStr)
cfOut = cfOutOrig['DistributionConfig'].copy()

# copy behaviors
cfOut['CacheBehaviors'] = cfSrc['CacheBehaviors'].copy()

# get available distribution ids
outOrigins = []
for bh in cfOutOrig['DistributionConfig']['Origins']['Items']:
    outOrigins.append(bh['Id'])
originsMap = {}

# confirm distribution ids
for i, bh in enumerate(cfOut['CacheBehaviors']['Items']):
    id = bh['TargetOriginId']
    if not originsMap.get( id ):
        confirm( id )
    cfOut['CacheBehaviors']['Items'][i]['TargetOriginId'] = originsMap[id]


# export modified config
cfOutFileName = 'cf_out.json'
cfOutFileH = open(cfOutFileName, 'w')
json.dump(cfOut,cfOutFileH)
cfOutFileH.close()

# apply changes to AWS CF
cmd = "aws cloudfront update-distribution --id "+targetDistribution
cmd += " --distribution-config file://"+cfOutFileName
cmd += " --if-match "+cfOutOrig['ETag']
os.system( cmd )


