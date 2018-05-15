
class FrozenDict(dict):
    def __init__(self, *args, **kwargs):
        self._hash = None
        super(FrozenDict, self).__init__(*args, **kwargs)

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(sorted(self.items())))  # iteritems() on py2
        return self._hash

    def __getattr__(self, item):
        return self.get(item, None)

    def _immutable(self, *args, **kws):
        raise TypeError('cannot change object - object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    pop = _immutable
    popitem = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable


# Message Formats for OpenC2
OpenC2MessageFormats = FrozenDict({
    'JSON': 'json',
    'CBOR': 'cbor',
    'PROTO': 'proto',
    'XML': 'xml',
})

# Schema Formats for OpenC2
OpenC2SchemaFormats = FrozenDict({
    'JADN': 'jadn'
})

# Actions for OpenC2 Messages
OpenC2Actions = FrozenDict({
    'SCAN': 'scan',
    'LOCATE': 'locate',
    'QUERY': 'query',
    'REPORT': 'report',
    'NOTIFY': 'notify',
    'DENY': 'deny',
    'CONTAIN': 'contain',
    'ALLOW': 'allow',
    'START': 'start',
    'STOP': 'stop',
    'RESTART': 'restart',
    'PAUSE': 'pause',
    'RESUME': 'resume',
    'CANCEL': 'cancel',
    'SET': 'set',
    'UPDATE': 'update',
    'MOVE': 'move',
    'REDIRECT': 'redirect',
    'DELETE': 'delete',
    'SNAPSHOT': 'snapshot',
    'DETONATE': 'detonate',
    'RESTORE': 'restore',
    'SAVE': 'save',
    'THROTTLE': 'throttle',
    'DELAY': 'delay',
    'SUBSTITUTE': 'substitute',
    'COPY': 'copy',
    'SYNC': 'sync',
    'DISTILL': 'distill',
    'AUGMENT': 'augment',
    'INVESTIGATE': 'investigate',
    'MITIGATE': 'mitigate',
    'REMEDIATE': 'remediate',
    'RESPONSE': 'response',
    'ALERT': 'alert'
})

# Targets for OpenC2
OpenC2Targets = FrozenDict({
    'ARTIFACT': 'artifact',
    'DEVICE': 'device',
    'DIRECTORY': 'directory',
    'DISK': 'disk',
    'DISK_PARTITON': 'disk-partition',
    'DOMAIN_NAME': 'domain-name',
    'EMAIL_ADDR': 'email-addr',
    'EMAIL_MESSAGE': 'email-message',
    'FILE': 'file',
    'IP_CONNECTION': 'ip-connection',
    'IPV4_ADDR': 'ipv4-addr',
    'IPV6_ADDR': 'ipv6-addr',
    'MAC_ADDR': 'mac-addr',
    'MEMORY': 'memory',
    'OPENC2': 'openc2',
    'PROCESS': 'process',
    'SOFTWARE': 'software',
    'URL': 'url',
    'USER_ACCOUNT': 'user-account',
    'USER_SESSION': 'user-session',
    'VOLUME': 'volume',
    'WINDOWS_REGISTRY_KEY': 'windows-registry-key',
    'X509_CERTIFICATE': 'x509-certificate'
})

# Actuators for OpenC2
OpenC2Actuators = FrozenDict({
    'ENDPOINT': 'endpoint',
    'ENDPOINT_WORKSTATION': 'endpoint-workstation',
    'ENDPOINT_SERVER': 'endpoint-server',
    'NETWORK': 'network',
    'NETWORK_FIREWALL': 'network-firewall',
    'NETWORK_ROUTER': 'network-router',
    'NETWORK_PROXY': 'network-proxy',
    'NETWORK_SENSOR': 'network-sensor',
    'NETWORK_HIPS': 'network-hips',
    'NETWORK_SENSE_MAKING': 'network-sense-making',
    'PROCESS': 'process',
    'PROCESS_ANIT_VIRUS_SCANNER': 'process-anit-virus-scanner',
    'PROCESS_AAA_SERVICE': 'process-aaa-service',
    'PROCESS_VIRTUALIZATION_SERVICE': 'process-virtualization-service',
    'PROCESS_SANDBOX': 'process-sandbox',
    'PROCESS_EMAIL_SERVICE': 'process-email-service',
    'PROCESS_DIRECTORY_SERVICE': 'process-directory-service',
    'PROCESS_REMEDIATION_SERVICE': 'process-remediation-service',
    'PROCESS_LOCATION_SERVICE': 'process-location-service'
})
