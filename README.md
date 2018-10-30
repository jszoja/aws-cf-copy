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
aws-cf-copy <source CF distribution id> <target CF distribution id>
```
It will ask you to choose the corresponding origins for the target distribution. 
 
 

