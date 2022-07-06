from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import time
import types
import os
import RPi.GPIO as GPIO
import subprocess
import shlex
import os
from subprocess import Popen, PIPE
import math
#import VolumeScript.py
#import KillServerScript.py
#import StartServerScript.py
#import CombineSinks.py

server = OSCServer( ("192.168.1.253", 8000) )#This has to be the IP of the RaspberryPi on the network
client = OSCClient()

def handle_timeout(self):
	print ("I'm IDLE")
#This here is just to do something while the script recieves no information....
server.handle_timeout = types.MethodType(handle_timeout, server)

def CombineSinks (path, tags, args, source):
        state = int(args[0])
        if state == 1:
           subprocess.call("sudo pactl load-module module-combine sink_name=Combined slaves= 2,3", shell=True)
                
def KillSwitch(path, tags, args, source):
	state=int(args[0])
	print "Kill Switch:", state
	if state == 1:
		server.close()

def VolumeScript(path, tags, args, source):
        state=(args)
        volume = int((state[0])*100)
        #print ("pactl set-source-volume 6 " + (str(volume)) +"%")
        subprocess.call("pactl set-source-volume 22 " + (str(volume)) +"%", shell=True)

def StartBluetooth(path, tags, args, source):
        state =  int(args[0])
        if state == 1:
            #subprocess.call(["bluetoothctl", "default-agent", "make discoverable on", "exit"], shell=True)
            process = ['bluetoothctl']
            subprocess.call(process)
            #stdout, stderr = process.call()
            print "hi"
            #subprocess.Popen(["bluetoothctl", "default-agent", "make discoverable on", "exit"], shell=True, stdout=subprocess.PIPE).stdout.read()
def ExitBluetooth(path, tags, args, source):
        state =  int(args[0])    
	if state == 1:
            rocess = ['bluetoothctl']
            subprocess.call(process)
            
            print("FUCK")
            
           # subprocess.call("exit", shell=True)
            
server.addMsgHandler("/syntien/untitled/1/button1", KillSwitch)
server.addMsgHandler("/syntien/untitled/1/button2", CombineSinks)
server.addMsgHandler("/syntien/untitled/1/button3", StartBluetooth)
server.addMsgHandler("/syntien/untitled/1/button4", ExitBluetooth)
server.addMsgHandler("/syntien/untitled/1/slider1", VolumeScript)
while True:
	server.handle_request()

server.close()
#This will kill the server when the program ends
