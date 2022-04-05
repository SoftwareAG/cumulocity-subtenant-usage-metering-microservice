import sys
import logging
from API.statistics import get_tenant_stats
from API.measurement import create_c8y_payload
from API.measurement import send_measurement
from API.inventory import check_external_ID
from flask import Flask, jsonify, request
import threading
import time
import json

logger = logging.getLogger('metering')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for metering was initialised')

app = Flask(__name__)

@app.route('/health')
def health():
    return '{"status":"UP"}'


if __name__== "__main__":
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)).start()
        while True:
            try:
                logger.info("Sending Stats")
                stats = get_tenant_stats()
                messages = []
                payload = {}
                for i in stats:
                    logger.debug(f'Iterating over all stats elements, picking: {i}')
                    logger.debug("Handing over to create_c8y_payload")
                    messages.append(create_c8y_payload(i,check_external_ID(i['tenantId'],i['tenantDomain'])))
                payload['measurements'] = messages
                logger.debug(f'Received the following payload for the whole measurement: {json.dumps(payload)}')
                send_measurement(json.dumps(payload))
                logger.info("Sleeping")
                time.sleep(900)
            except Exception as e:
                logger.error('The following error occured: %s' % (str(e)))