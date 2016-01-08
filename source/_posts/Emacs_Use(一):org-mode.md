
title: Emacs 使用笔记
date: 2016-01-07 19:15:23
tags: Emacs
toc: true
categories: Configure
---

# Org-mode<a id="sec-1" name="sec-1"></a>

Org-mode is an Emacs mode for note keeping, project planning, TODO lists and authoring

## Basic Grammar<a id="sec-1-1" name="sec-1-1"></a>

### 章节<a id="sec-1-1-1" name="sec-1-1-1"></a>

    *表示章节
    S-Tab   展开所有章节
    Tab     展开所在章节
    M-Left/M-Right  降级升级章节
    M-RET   换行生成同一级别条目

### 列表<a id="sec-1-1-2" name="sec-1-1-2"></a>

     checkbox [ ]
    + 无序列表
      - 子列表
      - 子列表
    1. [-]有序列表任务一[33%]
       1）[ ]有序子任务一
       2）[x]有序子任务二
    2. [ ]有序列表任务二

### 脚注<a id="sec-1-1-3" name="sec-1-1-3"></a>

### 表格<a id="sec-1-1-4" name="sec-1-1-4"></a>

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="left" />

<col  class="right" />

<col  class="right" />

<col  class="right" />

<col  class="right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="left">name</th>
<th scope="col" class="right">phone</th>
<th scope="col" class="right">sub1</th>
<th scope="col" class="right">sub2</th>
<th scope="col" class="right">total</th>
</tr>
</thead>

<tbody>
<tr>
<td class="left">manue1</td>
<td class="right">12346947588</td>
<td class="right">30</td>
<td class="right">20</td>
<td class="right">50</td>
</tr>


<tr>
<td class="left">Nanue1</td>
<td class="right">13356498787</td>
<td class="right">56</td>
<td class="right">25</td>
<td class="right">81</td>
</tr>
</tbody>
</table>

       所选位置中 =$3+$4
       C-u C-c C-c 计算 
    -   C-c C-c  对齐表格
    -   Tab 跳到下一格
    -   RET 跳到下一行
    -   S-  反方向
    -   M-方向键     移动表格
    -   M-S-方向键   插入表格

### 链接<a id="sec-1-1-5" name="sec-1-1-5"></a>

`【[链接地址][内容名称]】`

### 代办事项（TODO）<a id="sec-1-1-6" name="sec-1-1-6"></a>

-   操作命令：
    -   C-c C-t 转换TODO状态到DONE
    -   C-c / t 以树的形式展现TODO
    -   C-c C-c 改变checkbox的状态
    -   C-c ,   设置优先级 包括放括号内的ABC
    -   M-S-RET 插入同级TODO

### 时间<a id="sec-1-1-7" name="sec-1-1-7"></a>

    C-c C-s 开始时间
    C-c C-d 结束时间
    C-c .   时间段
    C-c !   [一个提示作用的时间戳]
    C-c a  选择选项来管理时间列表
    C-c L  任务列表
    C-c t  TODO-->DONE
    加入时间戳++1d 每天都要完成的任务<2015-06-15 Mon ++1d> 
    C-c C-t  选择TODO 的管理选项

### 富文本导出<a id="sec-1-1-8" name="sec-1-1-8"></a>

1.  设置样例

        这里的内容直接导出不会被转义

2.  设置注释

3.  插入代码

        public class TestReg {
        
            public static void main(String[] args) {
                /*
                 * 1、通过Scanner获取用户输入
                 * 2、获取连接
                 * 3、查询user表当前最大id
                 * 4、对这个id加1 计算出新的id
                 * 5、拼写insert语句插入新用户
                 * 6、通知用户注册结果
                 * 7、关闭连接
                 */
                Scanner scanner =new Scanner(System.in);
                System.out.println("请输入用户名");
                String username =scanner.nextLine();
                System.out.println("请输入密码");
                String password =scanner.nextLine();
        
                try {
                    Connection conn=DBUtil.getConnection();
                    Statement state = conn.createStatement();
                    //查看当前表中最大的id
                    String sql1 ="SELECT MAX(id)+1 id FROM user_manue1";
                    ResultSet rs =state.executeQuery(sql1);
                    int id=1;
                    if(rs.next()){
                        id=rs.getInt("id");
                    }
                    String sql2= "INSERT INTO user_manue1(id,username,password) VALUE ("+id+",'"+username+"','"+password+"')";
                    int flag =state.executeUpdate(sql2);
                    if(flag>0){
                        System.out.println("注册成功");
                    }else{
                        System.out.println("注册失败");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        
        }

## org&#x2013;>markdown<a id="sec-1-2" name="sec-1-2"></a>

由于hexo搭建的博客之支持markdown，所以需要将平时org格式的笔记转换成md [参考文档](http://randomgeekery.org/emacs/2014/05/16_exporting-from-org-to-markdown.html)
由于Emacs自带的orgmode版本过老，需要安装新版本的  [更新orgmode](http://orgmode.org/elpa.html)

出现这个问题 nvalid function: org-with-silent-modifications
解决方法
 转换命令： M-x org-md-export-to-md  或者 C-c C-e

## Org-mode 实现GDT<a id="sec-1-3" name="sec-1-3"></a>

参考文档<http://www.cnblogs.com/holbrook/archive/2012/04/17/2454619.html#sec-1-1>

### 1.如何实现GTD(Getting Things Done)<a id="sec-1-3-1" name="sec-1-3-1"></a>

-   收集
    mail, 电话，口头交流，网页，文档，想法  都记录下来
-   整理
    1.  丢弃每必要的
    2.  一些信息归档保存
    3.  重要事物创建任务
-   组织
    1.  将任务归入不同的工作清单
    2.  为任务增加标记
    3.  定义任务的完成状态
    4.  为任务定义优先级
    5.  为任务设定时间点
-   回顾
    1.  跑道：下一步行动（建议每日检视）
    2.  1万英尺：当前的项目（建议每周检视)
    3.  2万英尺：责任范围（建议每月检视）
    4.  3万英尺：1~2年的目标（建议每季检视）
    5.  4万英尺：3~5年的展望（建议每年检视）
    6.  5万英尺+：人生目的和价值观（面临重大变化和转折时）
-   执行
    给任务定性：重要/不重要  紧急/不紧急
    处理原则：先轻重，在缓急
    每完成一项任务，就将该任务标记为“已完成”，并归档。
    为了帮助判断，需要支持任务的筛选、搜索和排序 。

### 2.Org实现GTD<a id="sec-1-3-2" name="sec-1-3-2"></a>

-   文件划分
    1.  inbox.org     每天认为重要的知识记录在这个temp文件
    2.  journal       写日记
    3.  task.org      任务管理文件
    4.  note.org      用来写博客的文件 直接org转为md格式放到blog目录下

-   任务状态
    1.  TODO
    2.  NEXT
    3.  Someday
    4.  DONE
    5.  Abort
    6.  Waiting

### Emacs to do GTD config<a id="sec-1-3-3" name="sec-1-3-3"></a>

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;;org-mode设置
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;;设置org转换格式
    (setq org-export-backends (quote (ascii html icalendar latex md)))
    ;;安装最新org
    (require 'package)
    (add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/") t)
    ;;Org 基本的配置
    (global-set-key "\C-cl" 'org-store-link)
    (global-set-key "\C-ca" 'org-agenda)
    (global-set-key "\C-cb" 'org-iswitchb)
    ;; agenda view 查看的列表
    (setq org-agenda-files (list "~/doc/org/task.org"))
    
    ;;写日记和计划的快捷键
    (define-key global-map "\C-cc" 'org-capture)
    (setq org-capture-templates
          '(("t" "Todo" entry (file+headline "~/doc/org/task.org" "Tasks")
             "* TODO %?\n %i\n %a")
            ("j" "Journal" entry (file+datetree "~/doc/org/journal.org")
             "* %?\nEntered on %U\n %i\n %a")
             ("i" "Inbox" entry (file+datetree "~/doc/org/inbox.org")
             "* %?\nEntered on %U\n %i\n %a")
              ("n" "Note4Blog" entry (file+datetree "~/doc/org/note.org")
             "* %?\nEntered on %U\n %i\n %a")
     
    
            ))
    
    ;;设置任务状态
    (setq org-todo-keywords
         '((sequence "TODO(t!)" "SOMEDAY(s)" "|" "DONE(d@/!)" "UNDO(u@/!)" "ABORT(a@/!)")
                  ))    
    
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;; 实现全屏效果，快捷键为f11
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    (global-set-key [f11] 'my-fullscreen) 
    (defun my-fullscreen ()
    (interactive)
    (x-send-client-message
    nil 0 nil "_NET_WM_STATE" 32
    '(2 "_NET_WM_STATE_FULLSCREEN" 0))
    )
    
    
    ;; 最大化
    (defun my-maximized ()
    (interactive)
    (x-send-client-message
    nil 0 nil "_NET_WM_STATE" 32
    '(2 "_NET_WM_STATE_MAXIMIZED_HORZ" 0))
    (x-send-client-message
    nil 0 nil "_NET_WM_STATE" 32
    '(2 "_NET_WM_STATE_MAXIMIZED_VERT" 0))
    )
    
    ;; 启动emacs时窗口最大化
    (my-maximized)
