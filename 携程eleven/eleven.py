import json
import time

import execjs
import requests


def get_callback_param():
    f = open("./callback.js")
    context = execjs.compile(f.read())
    return context.call("getCallback")


def get_time():
    return str(time.time()).replace(".", "")[0:13]


def get_eleven():
    callback = get_callback_param()
    headers = {

    }
    data = json.dumps(
        {"callback": callback, "a": 0, "b": "", "c": "", "d": "zh-cn", "e": 2,
         "webpSupport": True, "platform": "online", "pageID": "102002"})

    url = 'https://m.ctrip.com/restapi/soa2/16709/json/getHotelScript'
    response = requests.post(url, headers=headers, data=data)
    code = (
            """
            var testab = function () {
            ((window = self = global).Window = () => 'native code', this);
            window.Image = class {
            }
            process = {
                mainModule: {
                    constructor: {
                        _load: ""
                    }
                }
            }
            window["%s"] = function (e) {
                window.ab = e();
            };

            %s

            return window.ab
            }
            testab()
            """
            % (callback, response.json()['Response'])
    )
    return code


print(get_eleven())
