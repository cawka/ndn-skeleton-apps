#!/usr/bin/env python

# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil; -*-
# Copyright 2013,2015 Alexander Afanasyev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyndn as ndn
import sys
try:
    import asyncio
except ImportError:
    import trollius as asyncio
import logging
logging.basicConfig()

class Client:
    def __init__(self, face, filename):
        self.face = face
        self.baseName = ndn.Name("/my-local-prefix/simple-fetch/file").append(filename)
        self.currentSeqNo = 0

        self._requestNext()

    def _requestNext(self):
        interest = ndn.Interest(ndn.Name(self.baseName).appendSequenceNumber(self.currentSeqNo))
        interest.setMustBeFresh(True)
        self.face.expressInterest(interest, 
                                  self._onData, self._onTimeout)
        self.currentSeqNo += 1

    def _onData(self, interest, data):
        print >> sys.stderr, "PyNDN %s" % data.name
        print data.content,

        seqNum = interest.getName()[-1].toSequenceNumber()
        if seqNum >= 10:
            return
        
        self._requestNext()

    def _onTimeout(self, interest):
        self.face.expressInterest(interest.getName(), 
                                  self._onData, self._onTimeout)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    face = ndn.ThreadsafeFace(loop, None)
    client = Client(face, sys.argv[1])

    loop.run_forever()
    face.shutdown()
