from KQueue import *
import os
import sys
from socket import *

add = []
delete = []
kq = KQueue()
print kq
print kq.kfd
file = socket(AF_INET, SOCK_STREAM)
file.bind("", 80)
file.listen(-1) 
# This is a no-no. Mits off of the data field!
# kev = KEvent(file.fileno(), (FILTER_READ|FILTER_WRITE), None, 'l')
kev = KEvent(file.fileno())
add.append(kev)
while 1:
  watch = add
  if len(delete) > 0: watch.append(delete)
  for thing in watch:
	print thing.ident
  todo = kq.event(watch, 250, 30000)
  add = []
  print todo
  for event in todo:
  # This is a bit of a quandary .. is the triggered file descriptor we 
  # get back awaiting accept() or already connection?  The data
  # field has a number in it but you can't use it for determination.
	delete.append(KEvent(file.fileno()))
	chat, addr = file.accept()
	add.append(KEvent(chat.fileno()))
	data = chat.recv(1024)
	if not chat: 
		delete.append(KEvent(chat.fileno(), (FILTER_READ|FILTER_WRITE), EV_DELETE))
		chat.close()
	chat.send(data)
