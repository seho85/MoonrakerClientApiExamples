"""
License:
    GPLv3

    Copyright (c) 2022 Sebastian Holzgreve

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import json
from websocket import create_connection

printer_ip = "10.0.1.69"
api_port = 7125
ws_url = "ws://%s:%s/websocket?token=" % ( printer_ip, str(api_port))

ws = create_connection(ws_url)

# Byte setting "extruder" : None we signalize we want to read everything in extrduder
# See https://moonraker.readthedocs.io/en/latest/printer_objects/ for a listing of all 
# availabe "objects" that can be queried.
# or use get available printer status request (https://moonraker.readthedocs.io/en/latest/web_api/#printer-status)

data = {
    "jsonrpc": "2.0",
    "method": "printer.objects.query",
    "params": {
        "objects": {
            "extruder" : None
        }
    },
    "id": 4654
  }

ws.send(json.dumps(data))

response = json.loads(ws.recv())

# Moonraker sends cyclic status information over the websocket, we need to make sure that
# the response data for our request was received.
# Cyclic status data doesn't contain an 'id' field.

while not 'id' in response:
    response = json.loads(ws.recv())

print(json.dumps(response, indent=2))

ws.close()
