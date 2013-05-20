import time
from ConfigParser import ConfigParser, NoOptionError
from twisted.python import log
import zope
from txsnowflake.remote import SnowflakeService
from txsnowflake.remote.ttypes import TXSnowflakeException


class Config(object):

    _config = None
    debug = None

    _rd_master = None

    _db_master = None

    @staticmethod
    def init(loc):
        Config._config = ConfigParser()
        Config._config.readfp(open(loc))
        Config.debug = Config.getbool('debug')


    @staticmethod
    def get(key, default=None, namespace='txsnowflake'):
        try:
            return Config._config.get(namespace, key)
        except NoOptionError:
            return default

    @staticmethod
    def getbool(key, default=None, namespace='txsnowflake'):
        try:
            obj = Config._config.get(namespace, key)

            obj = obj.strip().lower()
            if obj in ['true', 'yes', 'on', 'y', 't', '1']:
                return True
            elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
                return False

            return False

        except NoOptionError:
            return default

    @staticmethod
    def getint(key, default=None, namespace='txsnowflake'):
        try:
            return int(Config._config.get(namespace, key))
        except NoOptionError:
            return default



class SnowflakeServiceHandler(object):
    zope.interface.implements(SnowflakeService.Iface)

    def __init__(self, workerId, datacenterId, sequence=0):
        self.workerIdBits = 5L
        self.datacenterIdBits = 5L
        self.maxWorkerId = -1L ^ (-1L << self.workerIdBits)
        self.maxDatacenterId = -1L ^ (-1L << self.datacenterIdBits)
        self.sequenceBits = 12L
        self.workerIdShift = self.sequenceBits
        self.datacenterIdShift = self.sequenceBits + self.workerIdBits
        self.timestampLeftShift = self.sequenceBits + self.workerIdBits + self.datacenterIdBits
        self.sequenceMask = -1L ^ (-1L << self.sequenceBits)
        self.lastTimestamp = -1L
        self.twepoch = 1288834974657L

        self.workerId = workerId
        self.datacenterId = datacenterId
        self.sequence = sequence

        # *** START GLOBAL CONFIGURATION ***
        if self.workerId > self.maxWorkerId or self.workerId < 0:
            log.err("worker Id can't be greater than {0} or less than 0".format(self.maxWorkerId))
            raise Exception("worker Id can't be greater than {0} or less than 0".format(self.maxWorkerId))

        if self.datacenterId > self.maxDatacenterId or self.datacenterId < 0:
            log.err("datacenter Id can't be greater than {0} or less than 0".format(self.maxDatacenterId))
            raise Exception("datacenter Id can't be greater than {0} or less than 0".format(self.maxDatacenterId))

        log.msg("worker starting. timestamp left shift %d, datacenter id bits %d, worker id bits %d, sequence bits %d, workerid %d" % (
            self.timestampLeftShift, self.datacenterIdBits, self.workerIdBits, self.sequenceBits, self.workerId))

    def _get_time(self):
        return long(time.time() * 1000)

    def _till_next_millis(self, lastTimestamp):
        timestamp = self._get_time()
        while timestamp <= lastTimestamp:
            timestamp = self._get_time()

        return timestamp

    def get_id(self, user_agent):

        #todo uzix: validate useragent here...

        try:
            timestamp = self._get_time()

            if timestamp < self.lastTimestamp:
                msg = "clock is moving backwards. Rejecting requests until %d." % self.lastTimestamp
                log.err(msg)
                raise TXSnowflakeException(msg)

            if self.lastTimestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.sequenceMask
                if self.sequence == 0:
                    timestamp = self._till_next_millis(self.lastTimestamp)
            else:
                self.sequence = 0

            self.lastTimestamp = timestamp
            return ((timestamp - self.twepoch) << self.timestampLeftShift) | (self.datacenterId << self.datacenterIdShift) | (self.workerId << self.workerIdShift) | self.sequence
        except Exception as e:
            log.err("Error generating id: %s" % e)
            raise TXSnowflakeException(e.message)
