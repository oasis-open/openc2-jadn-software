import os

from libs import OpenC2MessageFormats
from libs.codec import Codec, jadn_load
from libs.message import OpenC2Message

msgs = {}
dir = './message/'

print("Load Messages")
for msg_file in os.listdir(dir):
    if msg_file.startswith(('.', '_')): continue

    n, t = msg_file.split('.')
    k = "{}-{}".format(t, n)
    msgs[k] = t, OpenC2Message(os.path.join(dir, msg_file), OpenC2MessageFormats.get(t.upper()))

print("Load Schema")
schema = jadn_load('schema/openc2-wd06_functional.jadn')
tc = Codec(schema, True, True)

print("Validate Messages\n")
for n, tup in msgs.items():
    t, o = tup
    print(n)

    print("{}_dump -> {}\n".format(t, o.__getattribute__(t + "_dump")()))

    m = tc.decode('OpenC2-Command', o.json_dump())
    print("Decoded Msg -> {}\n\n".format(m))
