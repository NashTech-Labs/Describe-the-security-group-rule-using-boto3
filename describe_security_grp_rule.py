# import logging for get the logs in  execution
import logging
# import the boto3 which will use to interact  with the aws
import boto3
from botocore.exceptions import ClientError
import json

AWS_REGION = input("Please enter the AWS_REGION")

# this is the configration for the logger

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

vpc_client = boto3.client("ec2", region_name=AWS_REGION)


def describe_rules(security_group_ids, max_items):
    try:
        
        paginator = vpc_client.get_paginator('describe_security_group_rules')

        response_iterator = paginator.paginate(
            Filters=[{
                'Name': 'group-id',
                'Values': security_group_ids
            }],
            PaginationConfig={'MaxItems': max_items})

        full_result = response_iterator.build_full_result()

        security_groups_rules = []

        for page in full_result['SecurityGroupRules']:
            security_groups_rules.append(page)

    except ClientError:
        logger.exception('This Security Groups Rules can not be described.')
        raise
    else:
        return security_groups_rules


if __name__ == '__main__':
    # SECURITY_GROUP_IDS = ['sg-022ed25b68ad24c18']
    SECURITY_GROUP_IDS = input("Please enter the Security Groups ID")

    MAX_ITEMS = 10
    rules = describe_rules(SECURITY_GROUP_IDS, MAX_ITEMS)
    logger.info('Security groups rules: ')
    for rule in rules:
        logger.info(json.dumps(rule, indent=4) + '\n')