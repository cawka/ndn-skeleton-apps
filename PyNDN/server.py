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
import pyndn.security as ndnsec
import sys
try:
    import asyncio
except ImportError:
    import trollius as asyncio
import logging
logging.basicConfig()

class Server:
    def __init__(self, face):
        self.face = face
        self.baseName = ndn.Name("/my-local-prefix/simple-fetch/file")
        self.counter = 0
        self.keyChain = ndnsec.KeyChain()

        self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
        self.face.registerPrefix(self.baseName,
                                 self._onInterest, self._onRegisterFailed)

    def _onInterest(self, prefix, interest, *k):
        print >> sys.stderr, "<< PyNDN %s" % interest.name
                
        content = "PyNDN LINE #%d\n" % self.counter
        self.counter += 1

        data = ndn.Data(interest.getName())

        meta = ndn.MetaInfo()
        meta.setFreshnessPeriod(5000)
        data.setMetaInfo(meta)

        data.setContent(content)

        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
        
        self.face.putData(data)

    def _onRegisterFailed(self, prefix):
        print >> sys.stderr, "<< PyNDN: failed to register prefix"

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    face = ndn.ThreadsafeFace(loop, None)
    server = Server(face)

    loop.run_forever()
    face.shutdown()
