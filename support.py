import time
import random
import hmac
import hashlib
import base64
import json
from requests import Request, Session


class Support:
    def __init__(self):
        self.__appID = "FdmClient"
        self.__secretKey = "secretKey"
        self.__nonce = self.__getGUID()
        self.__timestamp = self.__getTimeStamp()

        print(self.__nonce, self.__timestamp)

    def __getMessage(self, body):
        encodedMessage = ''

        stringToHash = self.__appID + ":" + str(body) + ":" + self.__nonce + ":" + self.__timestamp

        if len(stringToHash) > 0:
            encodedMessage = hmac.new(key=self.__secretKey.encode('utf-8'),
                                      msg=stringToHash.encode("utf-8"),
                                      digestmod=hashlib.sha256).hexdigest()

        return str(encodedMessage)

    @staticmethod
    def __getGUID():
        u = ''

        for i in range(36):
            c = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'[i-1]
            r = random.randint(0, 17)
            v = r if c == 'x' else (r & 0x3 | 0x8)
            u += c if ((c == '-') | (c == '4')) else format(v, 'x')

        return u

    @staticmethod
    def __getTimeStamp():
        return str(round(time.time()))

    def getHeader(self, body):
        encodedMessage = self.__getMessage(body)

        temp = "".join([self.__appID, ":", encodedMessage, ":", self.__nonce, ":", self.__timestamp])
        b64msg = base64.b64encode(temp.encode('ascii'))

        return {'Authorization': 'Bearer ' + b64msg.decode('utf-8')}

    def post(self, bundle):
        headers = self.getHeader(json.dumps(bundle))
        headers['Accept'] = 'application/fhir+json'
        headers['api-version'] = '1.0.0'
        headers['Content-Type'] = 'application/json'

        req = Request('POST', 'https://130.145.132.91:9005/fhir/Bundle',
                      headers=headers, data=json.dumps(bundle))
        prepared = req.prepare()

        s = Session()
        resp = s.send(prepared, verify=False)

        return resp


if __name__ == "__main__":
    msg = '/api/embedded_dashboard?data=%7B%22dashboard%22%3A7863%2C%22embed%22%3A%22v2%22%2C%22filters' \
          '%22%3A%5B%7B%22name%22%3A%22Filter1%22%2C%22value%22%3A%22value1%22%7D%2C%7B%22name%22%3A%22' \
          'Filter2%22%2C%22value%22%3A%221234%22%7D%5D%7D'

    ch = Support()
    print('Example:', ch.getHeader(body=msg))

