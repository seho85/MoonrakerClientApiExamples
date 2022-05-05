Moonraker Client API Access Examples
====================================
This example show how to use the [Moonraker Client API](https://moonraker.readthedocs.io/en/latest/web_api/) per Python.

A complete description of the [Moonraker Client API](https://moonraker.readthedocs.io/en/latest/web_api/) can be found [here](https://moonraker.readthedocs.io/en/latest/web_api/)

The ClientAPI can be used in two different ways:

* per HTTP Requests
* per Websocket
  * Websocket uses JSON RPC

The posted examples using the [websocket-client](https://websocket-client.readthedocs.io/en/latest/installation.html) python library. This library has to be installed to use this examples.

read_http.py
------------
This example shows how to use the MoonrakerAPI per HTTP requests

read_websocket_simple.py
------------------------
This example show how to use the websocket in a simple way.

1) Connect to Websocket 
2) Request Data
3) Disconnect from Websocket

read_websocket_app.py
---------------------
This example uses the more complex _websocketapp_ from the websocket-client library.

1) Connect to Websocket
2) Request Data
3) Stay connected
4) Status Updates published from Moonraker are also shown in this example