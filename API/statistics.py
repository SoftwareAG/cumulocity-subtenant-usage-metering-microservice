import requests
import logging
import json
import API.authentication as auth
from datetime import datetime, date, time, timedelta
from API.inventory import check_external_ID


logger = logging.getLogger('Stats API')
logger.info('Logger for Statistics was initialised')
Auth = auth.Authentication()

def get_tenant_stats():
    try:
        url = f'{Auth.tenant}/tenant/statistics/allTenantsSummary'
        logger.debug('Requesting the following url: ' + str(url))
        response = requests.request("GET", url, headers=Auth.headers)
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
                json_data = json.loads(response.text)
                return json_data
        else:
                logger.warning('Response from request: ' + str(response.text))
                logger.warning('Got response with status_code: ' + str(response.status_code))
                return [{}]
    except Exception as e:
        logger.error('The following error occured in Stats: %s' % (str(e)))