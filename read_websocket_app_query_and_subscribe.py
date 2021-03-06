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

import websocket
import json


printer_ip = "10.0.1.69"
api_port = 7125

ws_url = "ws://%s:%s/websocket?token=" % ( printer_ip, str(api_port) )

extruder_temperature = 0
extruder_target_temperature = 0
bed_temperature = 0
bed_target_temperature = 0

def on_close(ws, close_status, close_msg):
  pass

def on_error(ws, error):
  print("Websocket error")
  print(error)

def query_data(ws):
  query_req = {
    "jsonrpc": "2.0",
    "method": "printer.objects.query",
    "params": {
        "objects": {
            "extruder": [ "temperature", "target"],
            "heater_bed": ["temperature", "target"]
        }
    },
    "id": 1234
  }
  ws.send(json.dumps(query_req))

def unsubscribe_all(ws):
  data = {
    "jsonrpc": "2.0",
    "method": "printer.objects.subscribe",
    "params": {
        "objects": { },
    },
    "id": 4654
  }

  ws.send(json.dumps(data))


def add_subscription(ws):
  data = {
    "jsonrpc": "2.0",
    "method": "printer.objects.subscribe",
    "params": {
        "objects": {
            "heater_bed": None,
            "extruder": None
        }
    },
    "id": 5434
  }
  ws.send(json.dumps(data))

def print_data():
  print("Extruder Temperature:        %s ??C" % ( str(extruder_temperature)) )
  print("Extruder Target Temperature: %s ??C" % ( str(extruder_target_temperature)) )
  print("Bed Temperature:             %s ??C" % ( str(bed_temperature)) )
  print("Bed Target Temperature:      %s ??C" % ( str(bed_target_temperature)) )


def on_message(ws, msg):
  response = json.loads(msg)

  if 'id' in response:
    # Response to our query data request 
    if response["id"] == 1234:
      print("Data Query Data:")

      global extruder_temperature
      global extruder_target_temperature
      global bed_temperature
      global bed_target_temperature

      extruder_temperature = response["result"]["status"]["extruder"]["temperature"]
      extruder_target_temperature = response["result"]["status"]["extruder"]["target"]

      bed_temperature = response["result"]["status"]["heater_bed"]["temperature"]
      bed_target_temperature = response["result"]["status"]["heater_bed"]["target"]
     
      print_data()

      
      add_subscription(ws)
       
  
  # Subscribed printer objects are send with method: "notifiy_status_update"
  # The subscribed objects are only published when the value has changed.
  # e.g. bed_temperature target set to 50??, extruder temperature has changed, bed_temperature has changed, a.s.o.
  if response['method'] == "notify_status_update":

    if "heater_bed" in response['params'][0]:
      if 'temperature' in response["params"][0]["heater_bed"]:
              bed_temperature = response["params"][0]["heater_bed"]["temperature"]
      if 'target' in response["params"][0]["heater_bed"]:
              bed_target_temperature = response["params"][0]["heater_bed"]["target"]
    
    if "extruder" in response['params'][0]:
      if 'temperature' in response["params"][0]["extruder"]:
              extruder_temperature = response["params"][0]["extruder"]["temperature"]
      if 'target' in response["params"][0]["extruder"]:
              extruder_target_temperature = response["params"][0]["extruder"]["target"]

print_data()


def on_open(ws):

  print("on_open()...")
 
  query_data(ws)

global ws
#websocket.enableTrace(True)
ws = websocket.WebSocketApp(url=ws_url, on_close=on_close, on_error=on_error, on_message=on_message, on_open=on_open)
ws.run_forever()


