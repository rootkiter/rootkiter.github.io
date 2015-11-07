---
layout: post
title:  ARM 架构下的 ShellCode
date:   2015-07-04
time:   22:54:00
tags : [ ARM , 汇编+bin , 技术相关 , ShellCode]

---

## 引言
这是我很久以前写的一些学习 ANDROID＋ARM 的学习笔记，这是其中一篇，其他笔记会在适当的时候继续整理出来。先整理一下这一篇。

## 写段 HelloWorld

我编写shellcode也是从HelloWorld开始滴，下图是相应的代码截图：

![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/1.png)

然后编译链接运行：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/2.png)

## ShellCode 提取
到目前为止，自己编写的ARM汇编程序已经完全可执行了，下一步就是提炼16进制的shellcode，可以通过以下命令获取16进制结果：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/3.png)

然后就是固定的shellcode测试代码（C语言格式），如下图所示：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/4.png)

## RecvShell 的 ShellCode
这段代码是网上有人给出的，但是给出的却是objdump-d 版本，在还原指令的时候遇到很多语法问题，也就顺便学了一些Thumb语法，收获挺大的，看下面的截图（可以通过右键菜单中查看原图来查看放大图）：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/5.png)

程序编译连接后的执行结果如下所示：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/6.png)

还是利用objdump提取16进制shellcode，得到如下代码：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/7.png)

执行后运行结果如下图所示：


![rootkiter.com](http://rootkiter.com/images/2015_07_04_19_25/8.png)

## 结束
这里没有高深的技术点，只是一篇学习笔记和一些很详细的操作截图。

