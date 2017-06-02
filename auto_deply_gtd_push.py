import os
import time
arg_path = '/home/manue1/github/note/note-gtd.html'
target_path = '/home/manue1/github/blog/source/about/'
post_path = '/home/manue1/github/blog/source/_post/'
if os.path.exists(arg_path):
    cmd = 'mv %s %s -f' % (arg_path,target_path)
    s = os.system(cmd)
    print "copy not-gtd.html  status: %s" % str(s)
else:
    print "not-gtd.html not exist!"

html = 'mv *.html %s -f' % post_path
h = os.system(html)
print "copy html status: %s" % str(h)


hexo = 'hexo g && hexo d' 
os.system(hexo)

int_t = int(time.time())
cmd = "git add . && git commit -m '%d' && git push " % int_t
s = os.system(cmd)
print "push status : %s" % str(s)
