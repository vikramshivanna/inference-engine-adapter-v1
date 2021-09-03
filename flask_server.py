from proc_fhir_bundles import *
from support import Support

import os
from flask import Flask, request
from datetime import datetime
import json


app = Flask(__name__)


@app.route('/Bundle', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        app.logger.info("Received a GET")
        print('Received a GET.')
        return 'Received a GET'

    if request.method == 'POST':
        jo = json.loads(request.data.decode('utf-8'))

        app.logger.info("Received: {}".format(jo))

        if bundle_validator(jo):  # TODO: Drop this once the Outbound Filter is fixed.
            try:
                f_name = jo['resourceType'].lower()
                functions[f_name](jo)
            except KeyError:
                print("Unknown resourceType:", jo['resourceType'])

            app.logger.info("Modified Bundle: {}".format(jo))

            support = Support()
            resp = support.post(jo)

            app.logger.info(resp.status_code)
            app.logger.info(resp.json())

        return 'Received POST request.'


if __name__ == '__main__':
    import logging

    # Create a logs directory
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Every time a unique file name
    l_f_name = "logs_{}_{}".format(datetime.now().date(), datetime.now().time().strftime("%H_%M_%S"))

    logging.basicConfig(filename="logs/" + l_f_name, level=logging.INFO)

    app.run(debug=False, host='0.0.0.0', port=12345)
