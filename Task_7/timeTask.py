from requests import get
from datetime import datetime
from config import *

url = URL + '/index.php/indexCx/mlist/mobile/13151208539'

now = datetime.now()
logtime = now.strftime('%Y-%m-%d %H:%M:%S')

with open('timeTask.log', mode='a') as f:
    try:
        res = get(url)
        status = res.reason
        log = '%s - logger - INFO - TIMETASK %s' % (logtime, status)
        f.write(log)
        f.write('\n')
        print(log)
    except:
        log = '%s - logger - INFO - TIMETASK %s' % (logtime, 'ERROR')
        f.write(log)
        f.write('\n')
        print(log)
