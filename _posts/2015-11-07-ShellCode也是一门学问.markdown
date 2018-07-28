---
layout: post
title:  ShellCode也是一门学问
date:   2015-11-07
time:   15:18:00
tags : [ 技术相关 ,汇编+bin, ShellCode ]

---

## 开个头
最近拿到一道题，推测应该是西电的CTF题，来源很模糊，我也道不清原委，反正几经辗转到了我手里。  
这道题非常好，即考察了逆向能力，又考察了shellcode变形的一些知识。  

如果有机会再参与CTF出题，这道题绝对是一个值得花心思借鉴的题目。

## 题目概述
这里不准备把题目说的太细，就贴两张IDA逆向的结果图。简单描述一下题目的要求。

![rootkiter](/images/2015_11_07_18_29/1.png)
![rootkiter](/images/2015_11_07_18_29/2.png)

从这两张图可以提取出以下几个关键条件。
> 1. 用户输入的内容要在内存中进行一次异或解码;   
> 2. 解码后的内容必须为可视字符串，即只能为大小写字母，数字以及少部分标点字符，其他ascii中的无法显示的字符不能存在于ShellCode中;    
> 3. 当解码后的字符有“Bigtang”锚点子串时，则将解码的字符串当作代码进行执行;  
> 4. 在 图2 中可以看出，当解密数据被执行时，eax正好指向ShellCode基地址。


## 纯字符ShellCode
从题目描述可以得知，实际上这个题目的考点并不是软件类漏洞的利用，反而是对shellcode有一些极端的要求限制，当你通过了这些限制之后，自然就得到了执行条件。在这些限制条件中最难达到的其实就是纯字符的ShellCode了。  

对于纯可视字符类ShellCode的探索，网上也有过非常多的文章，国内比较好的文章有这样几篇：  

> [<<纯字母shellcode揭秘>>](http://bbs.pediy.com/showthread.php?t=113177)  
> [<<纯字符数字的shllcode及Alpha2.c使用>>](http://blog.csdn.net/instruder/article/details/6050048)  
> [<<纯ascii的shellcode编写>>](http://blog.csdn.net/v_ling_v/article/details/42824007)

以上三篇都是国内安全圈人对可视化ShellCode的经典论述。然而最吸引我的却是一篇却是圈外人的博文。
[<< ASCII Assembly技术简介>>](http://demon.tw/programming/ascii-assembly.html)  这足以说明：对“可视化字符ShellCode”的探索是部分极客的一种追求。

在这些文章中也多次出现了一个域名 http://skypher.com/ ，在我写这篇博文时，该链接中是一片空白，只留得无尽遐想。想必他就是这种极客技术的领路人吧，不知他最近还好嘛。

## ShellCode编码变形
> 悄悄的skypher走了，
> 正如他轻轻的来，
> 他挥一挥衣袖，
> 不带走一片云彩。

在他没带走的云彩中，有这样一个工具托管
[https://code.google.com/p/alpha3/](https://code.google.com/p/alpha3/)
是一个可以对ShellCode进行字符编码的工具，该工具由python编写，不过我在Linux下竟然没运行起来，只在Windows下运行成功。

在做这道题时我用到了一个执行/bin/sh的ShellCode，来源地址：
[http://shell-storm.org/shellcode/files/shellcode-752.php](http://shell-storm.org/shellcode/files/shellcode-752.php),这个网站中有非常多种ShellCode适用各种姿势。不过该部分内容已经停止更新了，原因在于现代漏洞利用技术已经很少再集中精力写shellcode，而是更注意ROP的开发以及编写了。

使用 ALPHA3 工具之前，需要将 ShellCode 以二进制形式写到一个文件中，效果如下所示：

![rootkiter](/images/2015_11_07_18_29/3.png)

然后就可以使用如下指令进行 ShellCode 编码了，我编码的目标为“X86 平台下、大写字符”，ShellCode开始执行那一刻，EAX寄存器保存了ShellCode的基地址。
所以指令如下所示：

<cmd>
	python ALPHA3.py x86 ascii uppercase EAX --input="shellcode"
</cmd>


![rootkiter](/images/2015_11_07_18_29/4.png)

得到的结果如下：  
<code>
PYVTX10X41PZ41H4A4I1TA71TADVTZ32PZNBFZDQC02DQD0D13DJE1D485C3E1YKM6L7L0  
60Y011T2OKO2B5NJO90MM9M3I00
</code>

## 字符型 ShellCode 样例
这里有两段从他人博客找到的 ShellCode 样例：

[/files/shellcode.txt](/files/shellcode.txt)


## 结个尾
事实上对 ShellCode 的探索一直就没有停止过， ShellCode 免杀，字符型 ShellCode，JIT下ShellCode，DVE中的虚拟执行层 ShellCode，正如<< ASCII Assembly技术简介>>中所说的：

> 没有什么神秘可言  
> 可执行程序是二进制文件  
> 文本文件也是二进制文件  
> 它们本质上没有什么区别  
> in.com 程序的特殊性在于   
> 所有的代码全部分布于ASCII码表的可显示字符范围中  
> 当然这样的程序不是碰巧得到的  
> 而是人为的构造出来的  
> 其中需要用到许多技巧   

再附上一篇关于Unicode的ShellCode编写的文章，作为结尾。  
[<<编写Unicode有效的Shellcode>>](http://huaidan.org/archives/1214.html)
