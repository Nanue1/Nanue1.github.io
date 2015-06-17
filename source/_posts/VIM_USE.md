title: Vim_Use
date: 2015-06-4 20:45:16
categories: Editor
toc: true
tags: Vim
---


 参考
  http://easwy.com/blog/archives/advanced-vim-skills-taglist-plugin/

##1)、vimrc 文件
	cp /usr/share/vim/vim70/vimrc_example.vim ~/.vimrc 
	filetype plugin indent on


##2)、安装插件管理器vundle
	参考：http://zuyunfei.com/2013/04/12/killer-plugin-of-vim-vundle/
	      http://avnpc.com/pages/vim-of-allovince
	bundle分为三类：
	在Github vim-scripts 用户下的repos,只需要写出repos名称
	在Github其他用户下的repos, 需要写出”用户名/repos名”
	不在Github上的插件，需要写出git全路径
<!--more-->
##3)、安装taglist
 	 cp taglist_46.zip ~/.vim
  	 unzip taglist_46.zip 
	要使用taglist plugin，必须满足：

	1、：filetype on
	2、系统中装了Exuberant ctags工具，
	  并且taglist plugin能够找到此工具
	 （因为taglist需要调用它来生成tag文件）
	yum install ctags
	3、vim支持system()调用

	vim 1.java +Tlistopen
##4)、HTML 插件
   http://www.vim.org/scripts/script.php?script_id=453
   http://christianrobinson.name/vim/HTML/
   
   :help 'runtimepath'
