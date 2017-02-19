import os
import time

int_t = int(time.time())
cmd = "git add . && git commit -m '%d' && git push " % int_t
s = os.system(cmd)
print "push status : %s" % str(s)
