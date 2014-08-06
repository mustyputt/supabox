from entertainment import common
import os

common._update_settings_xml()

services_path = os.path.join(common.addon_path, 'services')

sti=1

for dirpath, dirnames, files in os.walk(services_path):
    for f in files:
        if f.endswith('.py'):
            service_py = os.path.join(dirpath, f)
            #cmd = 'RunScript(%s,%s)' % (service_py, '1')
            #xbmc.executebuiltin(cmd)
            common.SetScriptOnAlarm(f[:-3], service_py, duration=sti)
            sti = sti + 1
