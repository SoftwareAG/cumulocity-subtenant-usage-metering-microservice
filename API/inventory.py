import requests
import logging
import json
from datetime import datetime, date, time, timedelta
from base64 import b64encode
import API.authentication as auth


logger = logging.getLogger('Inventory API')
logger.info('Logger for Inventory was initialised')
Auth = auth.Authentication()


def create_device(externalID, domain):
    try:
        logger.debug('Checking for managed object in c8y with external ID %s' + externalID)
        url = '%s/inventory/managedObjects'%(Auth.tenant)
        payload = json.loads('{"com_cumulocity_model_Agent": {},"c8y_IsDevice": {}, "c8y_metering": {}}')
        payload['name'] = f'{domain} - ({externalID})'
        response = requests.request("POST", url, headers=Auth.headers, data = json.dumps(payload))
        logger.debug('Requesting the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or 201:
            logger.info(f'Created a device for the following tenant: {externalID}')
            internal_id = json.loads(response.text)['id']
            if create_external_ID(externalID,internal_id,'c8y_Serial'):
                logger.debug('Returning the internal ID')
                return internal_id
            else:
                logger.error('Raising Exception, external ID was not registered properly')
                raise Exception
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            logger.warning('Device was not created properly')
            raise Exception
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))


def check_external_ID(external_id, domain):
    logger.debug('Checking if external ID exists')
    try:
        url = f'{Auth.tenant}/identity/externalIds/c8y_Serial/{external_id}'
        response = requests.request("GET", url, headers=Auth.headers)
        logger.debug('Sending data to the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.debug('Inventory exists')
            logger.debug(json.loads(response.text))
            internal_id = json.loads(response.text)['managedObject']['id']
            return internal_id
        elif response.status_code == 404:
            logger.info('Device does not exist, creating it')
            return create_device(external_id, domain)
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            raise Exception
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))


def create_external_ID(deviceID,internalID,type):
    logger.debug('Create an external id for an existing managed object')
    try:
        url = "%s/identity/globalIds/%s/externalIds"%(Auth.tenant, internalID)
        payload = {}
        payload['externalId'] = deviceID
        payload['type'] = type
        response = requests.request("POST", url, headers=Auth.headers, data = json.dumps(payload))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.debug('Receiving the following response %s'%(str(response.text)))
            return True
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

if __name__ == '__main__':
    pass

