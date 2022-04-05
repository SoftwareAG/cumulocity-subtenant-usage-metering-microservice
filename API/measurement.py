import requests
import logging
import json
import API.authentication as auth
import datetime


logger = logging.getLogger('Measurement API')
logger.info('Logger for Measurements was initialised')
Auth = auth.Authentication()

def send_measurement(payload):
    logger.info('Creating measurements in c8y')
    try:
        url = "%s/measurement/measurements"%(Auth.tenant)
        Auth.headers['Accept'] = 'application/vnd.com.nsn.cumulocity.measurementCollection+json'
        response = requests.request("POST", url, headers=Auth.headers, data = payload)
        logger.debug('Sending data to the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or 201:
            logger.info('Measurment send')
            return True
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                           str(response.status_code))
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))


def create_c8y_payload(message, internalID):
        payload = {}
        payload['source'] = {"id": str(internalID)}
        payload['type'] = "statistics"
        payload['time'] = datetime.datetime.strptime(str(datetime.datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f').isoformat() + "Z"

        payload['StorageSize'] = {}
        payload['StorageSize']['Current'] = {'value': message['storageSize']}
        payload['StorageSize']['Peak'] = {'value': message['peakStorageSize']}

        payload['DevicesWithChildren'] = {}
        payload['DevicesWithChildren']['Current'] = {'value': message['deviceWithChildrenCount']}
        payload['DevicesWithChildren']['Peak'] = {'value': message['peakDeviceWithChildrenCount']}

        payload['Devices'] = {}
        payload['Devices']['Current'] = {'value': message['deviceCount']}
        payload['Devices']['Peak'] = {'value': message['peakDeviceCount']}

        payload['Inventories'] = {}
        payload['Inventories']['Updated'] = {'value': message['inventoriesUpdatedCount']}
        payload['Inventories']['Created'] = {'value': message['inventoriesCreatedCount']}

        payload['Events'] = {}
        payload['Events']['Updated'] = {'value': message['eventsUpdatedCount']}
        payload['Events']['Created'] = {'value': message['eventsCreatedCount']}

        payload['Alarms'] = {}
        payload['Alarms']['Updated'] = {'value': message['alarmsUpdatedCount']}
        payload['Alarms']['Created'] = {'value': message['alarmsCreatedCount']}

        payload['Measurements'] = {}
        payload['Measurements']['Created'] = {'value': message['measurementsCreatedCount']}

        payload['ResourceCreateAndUpdate'] = {}
        payload['ResourceCreateAndUpdate']['Total'] = {'value': message['totalResourceCreateAndUpdateCount']}

        payload['Requests'] = {}
        payload['Requests']['Total'] = {'value': message['requestCount']}
        payload['Requests']['Devices'] = {'value': message['deviceRequestCount']}

        logger.debug(f'Created the following payload: {json.dumps(payload)}')
        return payload


if __name__ == '__main__':
    pass