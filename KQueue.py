#-
# Copyright (c) 2000 Doug White
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

# kqueue module interface for Python
# Version 1.1 (added copyright)

from kqsyscall import *

# Constants

# Event filters

EVFILT_READ   = -1
EVFILT_WRITE  = -2
EVFILT_AIO    = -3
EVFILT_VNODE  = -4
EVFILT_PROC   = -5
EVFILT_SIGNAL = -6
EVFILT_TIMER  = -7
EVFILT_NETDEV = -8
EVFILT_FS     = -9

# Event flags
EV_ADD      = 0x0001
EV_DELETE   = 0x0002
EV_ENABLE   = 0x0004
EV_DISABLE  = 0x0008
EV_ONESHOT  = 0x0010
EV_CLEAR    = 0x0020
EV_SYSFLAGS = 0xF000
EV_FLAG1    = 0x2000
EV_EOF      = 0x8000
EV_ERROR    = 0x4000

# Kernel note flags (for VNODE & PROC filter types)

NOTE_DELETE    = 0x0001
NOTE_WRITE     = 0x0002
NOTE_EXTEND    = 0x0004
NOTE_ATTRIB    = 0x0008
NOTE_LINK      = 0x0010
NOTE_RENAME    = 0x0020

NOTE_EXIT      = 0x80000000L
NOTE_FORK      = 0x40000000
NOTE_EXEC      = 0x20000000
NOTE_PCTRLMASK = 0xf0000000L
NOTE_PDATAMASK = 0x000fffff

NOTE_TRACK     = 0x00000001
NOTE_TRACKERR  = 0x00000002
NOTE_CHILD     = 0x00000004


# Kernel Queue main object
class KQueue:
    # File descriptor handle to the kernel queue
    def __init__ (self):
	self.kfd = kqueue()
	
    def event (self, kevs, wantEvents, timeout):
	# Call C kevent() here
	events = kevent(int(self.kfd), kevs, int(wantEvents), int(timeout))
	# events is a list of tuples; load KEvent list appropriately
	output = []
	for event in events:
	    # this is kinda ugly, but a dictionary seems bulky and this
	    # is somewhat of a private interface
	    output.append(KEvent(event[0], event[1], event[2], event[3], 
				 event[4], event[5]))
	return output

# Kernel Event object (1 per event to track)
class KEvent:

    def __init__(self, ident, filter=EVFILT_READ, flags=EV_ADD, fflags=None, data=None, udata=None):
	self.ident = ident
	self.filter = filter
	self.flags = flags
	self.data = data
	self.fflags = fflags
	self.udata = udata
    
