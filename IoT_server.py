#!/usr/bin/env python3
# encoding: utf-8

import http.server
import socketserver
import time
import datetime
from datetime import date
import RPi.GPIO as GPIO



PORT = 80
pins = [12, 16, 20, 21] 

"Vamos usar o  CGIHTTPRequestHandler pois ele aceita" \
"POSTs também."
#Handler = http.server.SimpleHTTPRequestHandler

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(http.server.CGIHTTPRequestHandler):

  statusString = ""

  # POST
  def do_POST(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        self.buildStatusString()
        message = self.statusString
        print(message)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

  def do_GET(self):
      self.handle_request(self.path)
      "We don't want to do anything else that's special, so call superclass method here."
      # Send response status code
      self.send_response(200)
      newDate = datetime.datetime.now()

      # Send headers
      self.send_header('Content-type','text/html')
      self.end_headers()

      "Query pins and build a string describing them..."
      statusString = ''
      self.buildStatusString()
      # Send message back to client
      message = "<head>\
<meta http-equiv=\"refresh\" content=\"30\">\
<meta charset=\"utf-8\" /><meta id=\"meta\" name=\"viewport\" content=\"width=device-width; initial-scale=1.2\" /><meta http-equiv=\"cache-control\" content=\"no-cache\" />\
<meta HTTP-EQUIV=\"EXPIRES\" CONTENT=\"0\">\
<title>Internet das Coisas!</title>\
</head>\
<body>Status: "+self.statusString+"<br>\
<div style=\"text-align: center\"><form  method=\"get\" name=\"relay\" value=\"1-on\">\
<table>\
  <th colspan=\"2\" align=\"center\">Controle do Relê #1</th>\
  <tr><td>Ligar 1: </td><td><button type=\"submit\" name=\"relay\" value=\"1-on\"><img src=\"http://192.168.25.5/fig/yellow48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
  <tr><td>Desligar 1: </td><td><button type=\"submit\" name=\"relay\" value=\"1-off\"><img src=\"http://192.168.25.5/fig/black48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
</table></form>\
</div>\
<br>\
<div style=\"text-align: center\"><form  method=\"get\" name=\"relay\" value=\"2-on\">\
<table>\
  <th colspan=\"2\" align=\"center\">Controle do Relê #2</th>\
  <tr><td>Ligar 2: </td><td><button type=\"submit\" name=\"relay\" value=\"2-on\"><img src=\"http://192.168.25.5/fig/yellow48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
  <tr><td>Desligar 2: </td><td><button type=\"submit\" name=\"relay\" value=\"2-off\"><img src=\"http://192.168.25.5/fig/black48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
</table></form>\
</div>\
<br>\
<div style=\"text-align: center\"><form  method=\"get\" name=\"relay\" value=\"3-on\">\
<table>\
  <th colspan=\"2\" align=\"center\">Controle do Rele #3</th>\
  <tr><td>Ligar 3: </td><td><button type=\"submit\" name=\"relay\" value=\"3-on\"><img src=\"http://192.168.25.5/fig/yellow48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
  <tr><td>Desligar 3: </td><td><button type=\"submit\" name=\"relay\" value=\"3-off\"><img src=\"http://192.168.25.5/fig/black48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
</table></form>\
</div>\
<br>\
<div style=\"text-align: center\"><form  method=\"get\" name=\"relay\" value=\"3-on\">\
<table>\
  <th colspan=\"2\" align=\"center\">Controle do Rele #4</th>\
  <tr><td>Ligar 4: </td><td><button type=\"submit\" name=\"relay\" value=\"4-on\"><img src=\"http://192.168.25.5/fig/yellow48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
  <tr><td>Desligar 4: </td><td><button type=\"submit\" name=\"relay\" value=\"4-off\"><img src=\"http://192.168.25.5/fig/black48.png\" style=\"border: 0px solid ;\" /></button></td></tr>\
</table></form>\
</div>\
<br>\
<footer><span style=\"font-size: smaller;\">Computação na Escola "+ str(newDate.time()) + "</span></footer>\
</body>\
</html>"
      # Write content as utf-8 data
      self.wfile.write(bytes(message, "utf8"))
      return

  def handle_request(self, requestData):
      requestValue = requestData.split("=")
      if (len(requestValue)> 1):
          print("Found a command!")
          requestValue=requestValue[1]
          print(requestValue)
          if (requestValue == "1-on"):
              self.turnOn(1)
          elif (requestValue == "1-off"):
              self.turnOff(1)
          elif (requestValue == "2-on"):
              self.turnOn(2)
          elif (requestValue == "2-off"):
              self.turnOff(2)
          elif (requestValue == "3-on"):
              self.turnOn(3)
          elif (requestValue == "3-off"):
              self.turnOff(3)
          elif (requestValue == "4-on"):
              self.turnOn(4)
          elif (requestValue == "4-off"):
              self.turnOff(4)
      return

  def turnOn(self, relay):
      "Put RPi code to turn relay ON here!"
      GPIO.output(pins[relay - 1], 0)
      return

  def turnOff(self, relay):
      "Put RPi code to turn relay OFF here!"
      GPIO.output(pins[relay - 1], 1)
      return

  def buildStatusString(self):
      for pin in pins:
      	if (GPIO.input(pin)):
          self.statusString = self.statusString + "DES "
      	else:
          self.statusString = self.statusString + "LIG "
      print(self.statusString)
      return


Handler = testHTTPServer_RequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Initializing Relays")
for pin in pins:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)


print("serving at port", PORT)
httpd.serve_forever()

