import sys
import time
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTwisted
from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from txsnowflake import Config, SnowflakeServiceHandler
from txsnowflake.remote import SnowflakeService

__author__ = 'uzix'


def main():
    if len(sys.argv) < 2:
        print 'Usage: %s config_file' % sys.argv[0]
        sys.exit()

    log.startLogging(sys.stdout)

    Config.init(sys.argv[1])

    if Config.debug:
        log.startLogging(sys.stdout)
    else:
        log.startLogging(DailyLogFile.fromFullPath(Config.get('log.file')))

    handler = SnowflakeServiceHandler(Config.getint('worker.id'), Config.getint('datacenter.id'))
    processor = SnowflakeService.Processor(handler)
    server = TTwisted.ThriftServerFactory(processor=processor, iprot_factory=TBinaryProtocol.TBinaryProtocolFactory())
    reactor.listenTCP(Config.getint('port', default=9999), server, interface=Config.get('listen', default="0.0.0.0"))
    reactor.run()


if __name__ == '__main__':
    main()


