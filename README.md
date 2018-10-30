# aws-cf-copy
It is simple tool, which automates the process of copying setup between two CloudFront distributions

## Requirements
You need to install awscli and configure it, eg:
```bash
pip install awscli --upgrade --user
```
More details: [read more...](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)

## Usage
```bash
usage: aws-cf-copy.py [-h] [-o OUTPUT] [--deploy] src target

Copy CloudFront behaviors between distributions

positional arguments:
  src         source CF distribution
  target      target CF distribution

optional arguments:
  -h, --help  show this help message and exit
  -o OUTPUT   output the configuration to a file
  --deploy    Deploy the changes to the target CloudFront distribution? It
              requires output file to be defined in -o option.
```
It will ask you to choose the corresponding origins for the target distribution. 
