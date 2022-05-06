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

from urllib import response
import websocket
import json


printer_ip = "10.0.1.69"
api_port = 7125

ws_url = "ws://%s:%s/websocket?token=" % ( printer_ip, str(api_port))

def on_close(ws, close_status, close_msg):
  pass

def on_error(ws, error):
  print("Websocket error: %s" % error)

def on_message(ws, msg):
  response = json.loads(msg)
  
  # Subscribed printer objects are send with method: "notifiy_status_update"
  # The subscribed objects are only published when the value has changed.
  # e.g. bed_temperature target set to 50°, extruder temperature has changed, bed_temperature has changed, a.s.o.
  if response['method'] == "notify_status_update":
    print(json.dumps(response, indent=2))

  #else:
  # print(json.dumps(response, indent=3))

def on_open(ws):

  print("on_open()...")

  #Unsubscribe from any printer objects
  data = {
    "jsonrpc": "2.0",
    "method": "printer.objects.subscribe",
    "params": {
        "objects": {
        
        }
    },
    "id": 4654
  }

  ws.send(json.dumps(data))

  # Subscribe to 'extruder' and 'heater_bed' printer object
  data = {
    "jsonrpc": "2.0",
    "method": "printer.objects.subscribe",
    "params": {
        "objects": {
            "extruder": [ "temperature", "target"],
            "heater_bed": ["temperature", "target"]
        }
    },
    "id": 5434
  }

  ws.send(json.dumps(data))


ws = websocket.WebSocketApp(url=ws_url, on_close=on_close, on_error=on_error, on_message=on_message, on_open=on_open)
ws.run_forever()

