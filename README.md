# Amazon Route53 Dynamic DNS Tool
A simple dynamic DNS service for Route53.

## Retrieving your external IP
This service performs a DNS query to retrieve your IP address from an OpenDNS resolver. This method arguably faster and more reliable than using an http(s) service.

Similar functionality could be done via the shell using dig: `dig +short myip.opendns.com @resolver1.opendns.com;`


## Usage
```bash
docker run -d \
    --name route53 \
    -e AWS_ACCESS_KEY_ID= \
    -e AWS_SECRET_ACCESS_KEY= \
    -e AWS_CONNECTION_REGION=us-east-1 \
    -e ROUTE53_DOMAIN_A_RECORD= \
    -e ROUTE53_UPDATE_FREQUENCY=10800 \
    bshaw/route53-dyndns
```

## Required Environment Variables
* `AWS_ACCESS_KEY_ID` - An AWS Access Key
* `AWS_SECRET_ACCESS_KEY` - An AWS Secret Key
* `AWS_CONNECTION_REGION` - The AWS region for connections
* `ROUTE53_DOMAIN_A_RECORD` - The A record to update, such as myhouse.domain.com
* `ROUTE53_UPDATE_FREQUENCY` - The frequency (in seconds) to check for updates. Unless you have very specific needs, consider using a very large value here.

## Credit
Heavily influenced by:
* [JacobSanford/docker-route53-dyndns](https://github.com/JacobSanford/docker-route53-dyndns)
* [JacobSanford/route-53-dyndns](https://github.com/JacobSanford/route-53-dyndns)
