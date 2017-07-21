import os
import time
arg_path = '/home/manue1/github/note/'
target_path = '/home/manue1/github/blog/source/about/note-gtd.html'
post_path = '/home/manue1/github/blog/source/_posts/'

now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
for s in os.listdir(arg_path):
    mv_path = arg_path + s
    if s == 'note-gtd.html' :
        if os.path.exists(target_path):
            c = "rm %s -f" % target_path
            os.system(c)
        c1 = "echo '---\nlayout: false\n---\n' >> %s" % target_path
        os.system(c1)
        cmd = 'cat %s >> %s ' % (mv_path,target_path)
        s = os.system(cmd)
        continue
    if 'html' in s :
        cat_path = post_path + s 
        if os.path.exists(cat_path):
            c = "rm %s -f" % cat_path
            os.system(c)
        title = s.split(".")[0].split('-')[-1]
        tag = s.split(".")[0].split('-')[1]
        c1 = "echo '---\ntitle: %s\nlayout: post\nupdated: %s\ntags: %s\n---\n' >> %s" % (title,now,tag,cat_path)
        print c1
        os.system(c1)
        cmd = 'cat %s >> %s ' % (mv_path,cat_path)
        s = os.system(cmd)
        cmd_more = 'cat %s | sed -e " 300i\<\!--more--> " -i %s' % (cat_path,cat_path )
        os.system(cmd_more)
        print "cat html status: %s" % str(s)
        if s == 0 :
            c = "rm %s -f" % mv_path
            os.system(c)
    else:
        pass

hexo = 'hexo g && hexo d' 
os.system(hexo)

int_t = int(time.time())
cmd = "git add -A && git commit -m '%d' && git push -f origin SRC161123" % int_t
s = os.system(cmd)
print "push status : %s" % str(s)
#---
#layout: post
#title:
#date:
#updated: 
#tags:
#---
