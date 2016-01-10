title: Hexo搭建博客笔记
date: 2016-01-10 16:01:25
tags: hexo

---
>       OS :linux x64
        AIM:采用Markdown写点文档笔记,Node.js写的hexo完美的将md格式的
        文章转化为html,本地ubuntu搭建hexo环境发布文章后,将public的目
        录上传到个人vps上发布,利用git托管本地文章,以作备份

<!-- more -->
***
### 0x01 环境搭建
1. 安装node.js,npm,git
      `sudo yum install nodejs
       sudo yum install npm
       sudo yum install git git-gui`
2. 本地连接github
    + 生成SSH认证密钥： ssh-keygen -t rsa -C “manue1@foxmail.com”
    + 复制密钥到github：
      配置Key参考连接:
      https://help.github.com/articles/generating-ssh-keys/
      `ssh-agent -s
      eval $(ssh-agent -s)
      ssh-add ~/.ssh/id_rsa
      复制这个 ~/.ssh/id_rsa.pub
      xclip -sel clip < ~/.ssh/id_rsa.pub`
    + 帐号认证：
    `git config --global user.name "Nanue1"
     git config --global user.email "manue1@foxmail.com"
     ssh git@github.com`

***
### 0x02 安装配置Hexo
1. 安装 hexo
  	`npm install -g hexo`
       参考文档:http://www.freehao123.com/hexo-node-js/
        更新安装源：（三选一）
        1.通过config命令:
       `npm config set registry http://registry.cnpmjs.org
        npm info underscore`  
        （如果上面配置正确这个命令会有字符串response）
        2.命令行指定
        `npm –registry http://registry.cnpmjs.org info underscore`
        3.编辑 ~/.npmrc 加入下面内容
        ` registry = http://registry.cnpmjs.org`
2.  配置 hexo    
    官方文档：http://hexo.io/zh-cn/docs/
    1) 部署在本地
    `hexo init
    hexo generate （npm install hexo –save 没法执行提示安装）
    hexo server (新版本都没有安装server这些插件 sudo npm install     hexo-server –save）
    npm install (打开本地网站 Connt GET/ 需要执行这条)`
    2) 部署到github
    首先配置_config.yml
`deploy:
type: git # 注意git前面的空格
repository: https://github.com/username/username.github.io.git
branch: master #仓库名使用ID建立的必须把blog放到master中`
hexo d (需要安装 npm install hexo-deployer-git –save)
这里多次报错都是因为_config.yml里面的格式问题，真是醉了
***
### 0x03上传项目到github来备份md文档
1. 提交备份
>cd ~/blog
本地提交：
`git init
git add .
git commit -m “第一次提交”`
提交到github：
`git checkout -b SRC150604 创建本地分支
git push origin SRC150604 创建远程分支
git push origin :SRC150604 删除远程分支
git push origin SRC150604:SRC150604 本地分支传到远程分支`
删除远程仓库文件：先删除本地 再 git add -A
2. 使用备份的仓库
    `git clone url -b SRC150604 new_name `
  参考文档:
    `http://www.zhixing123.cn/ubuntu/37865.html
    http://rongjih.blog.163.com/blog/static/335744612010112562833316/`

***
### 0x04Hexo 主题使用记录
1. 文章开头
>title: Git_Base
date: 2015-06-04 19:15:23
tags: Hexo
toc: true
categories: Configure  (---结束)

2. 主题
wixo主题： http://wzpan.github.io/hexo-theme-wixo/
NexT主题： https://github.com/iissnan/hexo-theme-next

3. categories和tags 找不到
   `hexo new page categories
    hexo new page tags`
  vim source/tags/index.md 
   add line: type: "tags"
  vim source/categories/index.md
  add line: type: "categories" 
  git pull
4. 博文中添加图片和音乐
   ![](七牛连接) 和 网易云音乐外链

