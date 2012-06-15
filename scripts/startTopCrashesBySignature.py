#! /usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import logging.handlers
import sys
import time

try:
  import config.topCrashesBySignatureConfig as configModule
except ImportError:
  import topCrashesBySignatureConfig as configModule

import socorro.lib.ConfigurationManager as configurationManager
import socorro.cron.topCrashesBySignature as topcrasher
import socorro.lib.util as sutil

try:
  config = configurationManager.newConfiguration(configurationModule=configModule, applicationName="Top Crashes Summary")
except configurationManager.NotAnOptionError, x:
  print >>sys.stderr, x
  print >>sys.stderr, "for usage, try --help"
  sys.exit(1)

logger = logging.getLogger("topCrashBySignature")
logger.setLevel(logging.DEBUG)

sutil.setupLoggingHandlers(logger, config)
sutil.echoConfig(logger, config)

try:
  before = time.time()
  tc = topcrasher.TopCrashesBySignature(config)
  count = tc.processDateInterval()
  logger.info("Successfully processed %s items in %3.2f seconds",count, time.time()-before)
finally:
  logger.info("done.")
