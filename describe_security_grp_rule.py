# import logging for get the logs in  execution
import logging
# import the boto3 which will use to interact  with the aws
import boto3
from botocore.exceptions import ClientError
import json

REGION = input("Please enter the REGION: ")

# this is the configration for the logger_for

logger_for = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

client = boto3.client("ec2", region_name=REGION)


def describe_rules(grp_ids, maximum_items):
    try: 
        paginate = client.get_paginator('describe_security_group_rules')

        response_iterator = paginate.paginate(
            Filters=[{
                'Name': 'group-id',
                'Values': grp_ids
            }],
            PaginationConfig={'MaxItems': maximum_items})

        result = response_iterator.build_full_result()

        grps_rules = []

        for x in result['SecurityGroupRules']:
            grps_rules.append(x)

    except ClientError:
        logger_for.exception('This Security Groups Rules can not be described.')
        raise
    else:
        return grps_rules


if __name__ == '__main__':
    # GRP_IDS = input("Please enter the Security Groups ID: ")
    MAXIMUM_ITEMS = int(input("Enter the Value for MAX ITEMS: "))
    GRP_IDS = ['<enter security grp id>']
    grp_rules = describe_rules(GRP_IDS, MAXIMUM_ITEMS)
    
    logger_for.info('Your Security groups rules: ')
    for x in grp_rules:
        logger_for.info(json.dumps(x, indent=4) + '\n')