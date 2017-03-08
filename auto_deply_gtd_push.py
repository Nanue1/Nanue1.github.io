import os
import time
arg_path = '/home/manue1/github/note/note-gtd.html'
target_path = '/home/manue1/github/blog/source/about/'
if os.path.exists(arg_path):
    cmd = 'mv %s %s -f' % (arg_path,target_path)
    s = os.system(cmd)
    print "copy status: %s" % str(s)
    hexo = 'hexo g && hexo d' 
    os.system(hexo)
else:
    print "not-gtd.html not exist!"
    hexo = 'hexo g && hexo d' 
    os.system(hexo)

int_t = int(time.time())
cmd = "git add . && git commit -m '%d' && git push " % int_t
s = os.system(cmd)
print "push status : %s" % str(s)
