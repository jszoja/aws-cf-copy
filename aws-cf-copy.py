import json, sys, os, argparse

# FUNCTIONS
def confirm(id):
    print("")
    for i, origin in enumerate( outOrigins ):
        print( str(i)+" - "+origin )
    mappedId = int(input("What origin you want to use for "+id+"?"))
    originsMap[id] = outOrigins[mappedId]
    return

# COMMAND LINE OPTIONS
parser = argparse.ArgumentParser(description='Copy CloudFront behaviors between distributions')
parser.add_argument('src', metavar='src', type=str,
                    help='source CF distribution')
parser.add_argument('target', metavar='target', type=str,
                    help='target CF distribution')                    
parser.add_argument('--with-error-pages', action="store_true", dest="withErrorPages",
                    help='copy error pages setup')
parser.add_argument( '-o', dest="output", default=False, help="output the configuration to a file" )
parser.add_argument( '--deploy', action='store_true', dest="deploy", default=False, help="Deploy the changes to the target CloudFront distribution? It requires output file to be defined in -o option." )
args = parser.parse_args()

if args.deploy and not args.output:
    print("You must specify the output file(-o option) to deploy the new distribution configuration.")
    sys.exit(1)

srcDistribution = args.src
targetDistribution = args.target

# load the src distribution config from AWS
cfSrcStr = os.popen("aws cloudfront get-distribution-config --id "+srcDistribution).read()
cfSrc = json.loads(cfSrcStr)['DistributionConfig'].copy()

# load targer distribution configuration
cfOutStr = os.popen("aws cloudfront get-distribution-config --id "+targetDistribution).read()
cfOutOrig = json.loads(cfOutStr)
cfOut = cfOutOrig['DistributionConfig'].copy()


# copy error pages setup
if args.withErrorPages:
    cfOut['CustomErrorResponses'] = cfSrc['CustomErrorResponses']

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

# if no output file defined then print the final configuration to stdout
if args.output == False:
    print(json.dumps(cfOut, indent=2, sort_keys=True))
    sys.exit(0)

# export modified config
cfOutFileName = args.output
cfOutFileH = open(cfOutFileName, 'w')
json.dump(cfOut,cfOutFileH)
cfOutFileH.close()

# CLI command for applying the changes
cmd = "aws cloudfront update-distribution --id "+targetDistribution
cmd += " --distribution-config file://"+cfOutFileName
cmd += " --if-match "+cfOutOrig['ETag']

if args.deploy == False:
    print("Updated configuration has been saved to "+cfOutFileName)
    print("Run the following command to deploy it:")
    print("  "+cmd)
    sys.exit(0)

# apply changes to AWS CF
os.system( cmd )


