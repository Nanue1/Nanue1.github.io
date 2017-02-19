title: Hexo搭建博客笔记
date: 2015-08-21 16:01:25
tags: hexo

---

对于个人的博客,我自己的定位需求,其实主要还是方便以后查看,作为一个内容的展示平台,并不需要多少花哨的渲染,相比而言hexo使用markdown,完美支持我自己的需求,ok下面记录下我ubuntu下的配置方式,避免后续环境迁移再折腾.
在这里平时可以将public目录上传到个人vps服务器上发布,利用git托管也是很不错的选择,master存放静态文件,分支存放hexo源文件.
##   环境准备
1. 安装node.js,npm,git
   `sudo apt-get install nodejs`
   `sudo apt-get install git` 
    这里推荐使用 [nvm](https://github.com/creationix/nvm#install-script) 安装 nodejs  [参考]( https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-an-ubuntu-14-04-server#how-to-install-using-nvm)
    <!-- more -->

2. 本地连接github
   + 生成SSH认证密钥:		 
     `ssh-keygen -t rsa -C “manue1@foxmail.com”`
   + 复制密钥到github:
      [配置Key](https://help.github.com/articles/generating-ssh-keys/):
     `ssh-agent -s`
     `eval $(ssh-agent -s)`
     `ssh -add ~/.ssh/id_rsa`
     `xclip -sel clip < ~/.ssh/id_rsa.pub  #复制这个 ~/.ssh/id_rsa.pub`
   + 帐号认证：
     `git config --global user.name "Nanue1"`
     `git config --global user.email "manue1@foxmail.com"`
     `ssh git@github.com`

##    hexo设置
1.  [hexo安装](http://www.freehao123.com/hexo-node-js/)
    `npm install -g hexo`

     如果安装hexo出问题,下面是三种更新安装源方案：（三选一）
    - 通过config命令:
      `npm config set registry http://registry.cnpmjs.org`
      `npm info underscore   #如果上面配置正确这个命令会有字符串response`
    - 命令行指定
      `npm –registry http://registry.cnpmjs.org info underscore`
    - 编辑 ~/.npmrc 加入下面内容
      `registry = http://registry.cnpmjs.org`

2.  [部署hexo博客](http://hexo.io/zh-cn/docs/)
    - 部署在本地
      `hexo init	#生成博客,只能第一次使用`
      `hexo generate 	#需要安装 npm install hexo –save `
      `hexo server    	#需要安装 sudo npm install hexo-server –save`
      `npm install	#打开本地网站 Connt GET/ 需要执行这条`

    - 部署到github master分支
      需要配置_config.yml文件
      `deploy:`
      `type: git # 注意git前面的空格`
      `repository: https://github.com/username/username.github.io.git`
      `branch: master #仓库名使用ID建立的必须把blog放到master中`
      部署命令
      `hexo d #需要安装 npm install hexo-deployer-git –save`

## 用github备份博客
1.  提交备份
    - 本地提交：
      `git init`
      `git add . `
      `git commit -m “first” `

    - 提交到github：
      `git checkout -b SRC150604 #创建本地分支`
      `git push origin SRC150604 #创建远程分支`
      `git push origin :SRC150604 #删除远程分支`
      `git push origin SRC150604:SRC150604 #本地分支传到远程分支`
      删除远程仓库文件,需要先删除本地在提交 
      `git add -A`

2.  [使用备份的仓库](http://rongjih.blog.163.com/blog/static/335744612010112562833316/)
    `git clone url -b SRC150604 new_name` 

## Hexo 主题使用

1. 文章开头
    `title: Git_Base`
    `date: 2015-06-04 19:15:23`
    `tags: Hexo`
    `categories: Configure ` 
    `---`
2. 主题
   [NexT主题]( https://github.com/iissnan/hexo-theme-next)
   [Cactus Dark](https://github.com/probberechts/cactus-dark#configuration)
3. categories和tags 找不到
   `hexo new page categories`
   `hexo new page tags`
   `vim source/tags/index.md `
   `add line: type: "tags"`
   `vim source/categories/index.md`
   `add line: type: "categories" `
   `git pull`

##  [Hexo部署到VPS](http://atomlx.com/2016/08/12/test/#more)

将Hexo在本地通过 `hexo generate` 生成静态文件，在通过 `hexo deploy` 部署到VPS上面，使用Nginx直接做Web服务器.网上有两种做法:git部署和rsync部署,由于我前面部署到github上使用了git,这里部署到VPS就选择rsync,各取所需.

1. Nginx 部署
- nginx install
  ` apt-get install nginx`

- nginx config
  `cp /etc/nginx/sites-available/default /etc/nginx/sites-available/hexo`
  `vi /etc/nginx/sites-available/hexo`

  配置文件内容
  ```json
  server {
         	listen 80 default_server; 		 # 服务器配置端口，不修改
         	listen [::]:80 default_server;
         	root /home/manue1/hexo;  # 文件路径，改成你需要设置的路径
         	# Add index.php to the list if you are using PHP
         	index index.html index.htm index.nginx-debian.html;
         	server_name manue1.site www.manue1.site *.manue1.site; 
    		# 域名配置，可以按照我设置的方式进行设置，记得还需要配置域名解析
         	location / {
         		# First attempt to serve request as file, then
         		# as directory, then fall back to displaying a 404.
         		try_files $uri $uri/ =404;
  }
  ```
  `rm /etc/nginx/sites-enabled/default`
  `ln -s /etc/nginx/sites-available/hexo /etc/nginx/sites-enabled/`

- 重启nginx

  `sudo  service nginx restart`

2. rsync部署Hexo
- 安装rsync
  `apt-get install rsync #本地-服务端 默认系统自带`
  `npm install hexo-deployer-rsync --save  #本地Hexo配置`
- 本地Hexo _config.xml配置
```json
deploy:
  type: rsync
  host: vps-ip  		 # 这里填写你VPS的IP地址，比如：202.201.112.98
  user: vps-user 		# 这里填写你登陆VPS所用的用户名，比如：manue1
  root: /home/manue1/hexo  # 这里填写你在nginx中配置的文件路径
  port: 22 				# SSH默认端口号，不需要修改
```
- 更新文章
  `hexo generate && hexo deploy`

