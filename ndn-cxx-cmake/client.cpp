/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/**
 * Copyright 2013,2015 Alexander Afanasyev
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <ndn-cxx/face.hpp>
#include <ndn-cxx/interest.hpp>
#include <ndn-cxx/data.hpp>

#include <iostream>
#include <string>

class Client
{
public:
  explicit
  Client(ndn::Face& face, const std::string& filename)
    : m_face(face)
    , m_baseName(ndn::Name("/my-local-prefix/simple-fetch/file").append(filename))
    , m_currentSeqNo(0)
  {
    std::cerr << "Base name: " << m_baseName << std::endl;
    requestNext();
  }

private:
  void
  requestNext()
  {
    ndn::Name nextName = ndn::Name(m_baseName).appendSequenceNumber(m_currentSeqNo);
    std::cerr << ">> C++ " << nextName << std::endl;
    m_face.expressInterest(ndn::Interest(nextName).setMustBeFresh(true),
                           std::bind(&Client::onData, this, _2),
                           std::bind(&Client::onNack, this, _1),
                           std::bind(&Client::onTimeout, this, _1));
    ++m_currentSeqNo;
  }


  void
  onData(const ndn::Data& data)
  {
    std::cerr << "<< C++ "
              << std::string(reinterpret_cast<const char*>(data.getContent().value()),
                                                           data.getContent().value_size())
              << std::endl;

    if (data.getName().get(-1).toSequenceNumber() >= 10) {
      return;
    }

    requestNext();
  }

  void
  onNack(const ndn::Interest& interest)
  {
    std::cerr << "<< got NACK for " << interest << std::endl;
  }

  void
  onTimeout(const ndn::Interest& interest)
  {
    // re-express interest
    std::cerr << "<< C++ timeout for " << interest << std::endl;
    m_face.expressInterest(ndn::Interest(interest.getName()),
                           std::bind(&Client::onData, this, _2),
                           std::bind(&Client::onNack, this, _1),
                           std::bind(&Client::onTimeout, this, _1));
  }

private:
  ndn::Face& m_face;
  ndn::Name m_baseName;
  uint64_t m_currentSeqNo;
};

int
main(int argc, char** argv)
{
  if (argc < 2) {
    std::cerr << "You have to specify filename as an argument" << std::endl;
    return -1;
  }

  try {
    // create Face instance
    ndn::Face face;

    // create client instance
    Client client(face, argv[1]);

    // start processing loop (it will block until everything is fetched)
    face.processEvents();
  }
  catch (const std::exception& e) {
    std::cerr << "ERROR: " << e.what() << std::endl;
  }

  return 0;
}
