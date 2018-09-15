#!/usr/bin/python3

from sharedconfigfile import SharedConfigFile

f = open('sharedconfig.vdf')
vdf = SharedConfigFile(f)
vdf.clear_all_tags()
vdf.generate_all_tags()
n = open('sharedconfig.vdf.new', 'w')
n.write(str(vdf))
n.close()
f.close()
