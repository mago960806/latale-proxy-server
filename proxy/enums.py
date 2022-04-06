from enum import IntEnum


class Method(IntEnum):
    NO_AUTHENTICATION_REQUIRED = 0x00
    GSSAPI = 0x01
    AUTHENTICATION_REQUIRED = 0x02
    NO_ACCEPTABLE_METHODS = 0xFF


class Command(IntEnum):
    CONNECT = 0x01
    BIND = 0x02
    UDP_ASSOCIATE = 0x03


class AddressType(IntEnum):
    IPv4 = 0x01
    DOMAIN_NAME = 0x03
    IPv6 = 0x04


class Reply(IntEnum):
    SUCCEEDED = 0x00
    GENERAL_SOCKS_SERVER_FAILURE = 0x01
    CONNECTION_NOT_ALLOWED_BY_RULESET = 0x02
    NETWORK_UNREACHABLE = 0x03
    HOST_UNREACHABLE = 0x04
    CONNECTION_REFUSED = 0x05
    TTL_EXPIRED = 0x06
    COMMAND_NOT_SUPPORTED = 0x07
    ADDRESS_TYPE_SUPPORTED = 0x08
