namespace py txsnowflake.remote

#
# Generate python stubs with:
#   thrift --gen py:twisted -out . txsnowflake.thrift
#
# For py clients use:
#   thrift --gen py -out client txsnowflake.thrift
#

#
# exception
#

exception TXSnowflakeException {
    1: required string why
}


service SnowflakeService {
  i64 get_id(1: string user_agent) throws (1: TXSnowflakeException ex)
}