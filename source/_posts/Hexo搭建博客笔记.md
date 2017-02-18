title: Hexo搭建博客笔记
date: 2016-01-10 16:01:25
tags: hexo
categories: Configure

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
3. categories和tags 找不到

   `hexo new page categories`
   `hexo new page tags`
   `vim source/tags/index.md `
   `add line: type: "tags"`
   `vim source/categories/index.md`
   `add line: type: "categories" `
   `git pull`

