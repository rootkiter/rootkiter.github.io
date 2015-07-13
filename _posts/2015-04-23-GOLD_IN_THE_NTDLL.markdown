---
layout: post
title:  "ntdll 空间中的金疙瘩"
date:   2015-04-23
time:   22:23:00
categories : [ exploit-rop , 技术相关, 汇编+bin ] 

---

背景
====================


通过阅读[第一篇笔记](/2014/02/28/ROPIntroduce.html "ROP介绍")，可以知道，ROP构造是软件类漏洞利用中很重要的一环(为了绕过dep保护)，然而用过mona工具的童鞋应该都清楚，这个工具似乎不太好用。即使你通过mona搞定了ROP骨架的生成，有时仍然需要微调，特别是当mona结果中拥有和漏洞环境相关的坏字符时，修复ROP-chain 也成为了软件类漏洞利用的重要一环。

此时这篇笔记的意义就出现了：***如何找到有用的ROP素材，并将存在问题的ROP-chain修复。***

文中提到的代码素材均来自于ntdll.dll文件，其中  
<code>
ntdll.dll版本号为：6.1.7601.17514  
本机Win7 启动后ntdll的偏移： 0x77880000
</code>

声明：  
不同版本，得到的代码偏移可能不同。  
至于DLL模块基地址嘛。。。那是一定不同滴。。。因为我是在Win7环境下查找的指令，看客可以通过搜索特定指令序列，或通过我给出的偏移计算出来。  
本段将纪录，我在 ntdll.dll 中找到的各种指令，它们可以用来做四则运算，甚至用来处理内存拷贝。

有趣的代码片段
=================

## XCHG系列

这个系列的指令，在ROP构造中有奇效。ROP-chain中每个寄存器中的值都是宝贝，遗失不得。而在执行 xchg 指令时，完全不会干扰到其他寄存器的内容，他们之间真的非常般配。

### xchg eax,esp

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_1_1_1.png)

这是 IE 漏洞利用中经常用到的一条控制ESP的指令。它在漏洞触发的那一刻能够将ESP从“栈指针”，改成“堆指针”，配合“堆喷射”技术完成漏洞利用。

### xchg eax,edx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_1_2_1.png)

这是一条可用来保存 eax 的指令。由于多数汇编指令都会用到eax寄存器，这条指令刚好能把当前寄存器中的数据同 edx 交换一下，用起来很方便。

### xchg eax,ecx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_1_3_1.png)

当我想把 ECX 作为内存指针时，完全可以通过 EAX 计算出相应地址，然后放到交换到ECX中。

## add 系列

### sub eax,edx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_2_1_1.png)

看到这里不明真相的群众一定会问，这明明是 sub指令，为毛划分到 add系列 中呢？  
这是因为 sub指令 比 add指令 有效得多，如果使用ADD指令执行 eax +0x20 的操作，得到的ROP素材应该是这样的：  
<code>
Address -> { POP EDX # RETN }  
0x00000020  
Address -> { ADD EAX,EDX …… }  
</code>

此时，这样的ROP-chain中出现了一个坏字符%u0000％u2000，这个坏字符将会非常难以去除。然而如果用 sub 指令，就可以是这样的：  
<code>
Address -> { POP EDX # RETN }  
0xffffffe0  
Address -> { SUB EAX,EDX …… }  
</code>

坏字符被巧妙的避开了，减去一个负数 等同于 加上一个正数，初中数学绝对不白学。

### inc xxx

#### inc ecx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_2_2_1.png)

这条指令，我是找了很久才发现的。它出现的时候，我真的眼前一亮，它意味着，我可以不用EAX来做简单的加法运算了，当我仅需要给一个数字 +4 时，我只要写四次这个地址就好了。  
<code>
Address -> { INC ECX ,RETN  }  
Address -> { INC ECX ,RETN  }  
Address -> { INC ECX ,RETN  }  
Address -> { INC ECX ,RETN  }  
</code>

这可以节省我很多 备份数字的操作，更棒的地方在于 retn 指令没有参数，完全不需要垃圾字符填充。绝对是一条高效的 rop 指令素材。

#### inc eax

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_2_2_2.png)

这个指令素材，有两种功效，当我需要向EAX写入1时，我可以使用三条指令，ROP示例如下：  
<code>
Address -> { XOR EAX,EAX # INC EAX # RETN }
</code>

而当我仅需要将 EAX + 1 时，我可以使用：  
<code>
Address -> { INC EAX # RETN  }
</code>

#### inc ebx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_2_2_3.png)

这条指令应该不用说了，和前面的 inc ecx 有相似之处。

#### inc edx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_2_2_4.png)

同上

### 其他运算

#### xor eax,ecx 

xor系列指令貌似都比较少，也都不够高效，需要填充很多垃圾字符：

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_3_1_1.png)

它的使用大概是这样的：  
<code>
Address  -> { XOR EAX,ECX # POP ESI # POP EBP # RETN 8  }
0x41414141   // skip 4 for pop esi  
0x41414141   // skip 4 for pop esi  
Address  -> { 下一条指令 }
0x41414141   //skip  4 for retn 8
0x41414141   //skip  4 for retn 8
</code>  

这条指令还是可以用来处理一些通常情况无法绕过的垃圾字符滴。

#### xor eax,edx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_3_2_1.png)

使用方法参照 xor eax,ecx ,不过看起来似乎比那条指令更好用一些，垃圾字符填充也会少一些。

#### idiv ecx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_3_3_1.png)

这是一个有趣的素材，它能计算除法，因为除法对寄存器的干扰实在太明显了，所以在ROP中用处也不会太大。但有一条就比没有强，没准会遇到什么样子的奇葩环境。

#### not eax

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_3_4_1.png)

这条指令，是偶然发现的，并运用到了一次ROP构造中，非常好用，很可惜的是过于浪费空间，一句 RETN 0C 就要浪费 3个DWORD。使用方法大致如下：  
<code>
Address -> { POP EAX # RETN}
Address -> { NOT EAX # POP EBP # RETN 0C }
0x41414141     // skip 4  for pop ebp
Address -> { 下一条指令 }
0x41414141     // skip 4  for  retn0c
0x41414141     // skip 4  for  retn0c
0x41414141     // skip 4  for  retn0c
</code>

## 赋值系列指令

### POP XXX

这系列指令大概不用讲了，都清楚，当你需要执行 MOV EAX，0x43434343 时，
直接用  
<code>
Address -> { POP EAX # RETN }
0x43434343
</code>  
即可。
对应的4个寄存器的pop指令素材为：  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_1_1.png)  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_1_2.png)  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_1_3.png)  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_1_4.png)  

###  寄存器间传值

#### mov eXX,eXX 

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_1_1.png)  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_1_2.png)  

#### pushad

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_2_1.png)  
请， 先收起你的惊讶的表情... pushad 确实可以进行寄存器间赋值～～～
当你想动态定位shellcode位置时，可能会需要这样一条指令，MOV EAX，ESP，然而你找遍内存也可能搜索不到可用的素材，怎么办呢？这时，你就可以通过 PUSHAD RETN 来构造一条这样的指令。PUSHAD后堆栈的状态是这样的（如下图所示），此时再调用retn其实将会返回到EDI所指向的指令，如下图所示：  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_2_2.png)  
那么我只要让堆栈中是下面这种结构，就可以把ESP的值赋值给EAX了：  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_2_3.png)  
也就是说，调用PUSHAD前，你可以通过POP EDI、POP EBP、POP EBX、POP ECX等指令，部署各个寄存器所指向的地址，这样在调用PUSHAD RETN之后便可实现任意寄存器间的赋值了。下面是我在一次ROP构造时构造的 MOV ECX，ESP  
![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_2_4.png)  
这条指令很 cool 吧。
其实这条指令还可以在 PUSHAD 的 RETN 后，跳到某个API函数的地址，只要控制好各个寄存器的值，绝对能让人神清气爽！

#### 5POP指令  

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_3.png)  
我把这条指令放在这个位置，是想说明：5POP指令和PUSHAD可以很奇妙的组合在一起，当你在PUSHAD指令前将EBP指向 5POP，那么你就能非常快速的跳出 PUSHAD 对堆栈造成的影响，顺利回到ROP_chain的空间，5POP指令同样也可以拆分使用，甚至可以在一句话完成多个MOV操作，因为这条指令中同时有POP ECX 和POP EBX两条指令。

#### xchg eax，edx？

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_4.png)  
这段指令共有4条，全部组合在一起，就是一个通过 ecx 寄存器实现XCHG EAX，EDX，而当你使用其中的三条时，指令就变成了 MOV 【EAX：EDX】，【EDX：ECX】或者用其中的两条就变成了 MOV EDX，ECX。

#### mov [ecx],eax

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_5.png)  
这条指令可以实现向 ecx 指向的空间写入一个双字数据，功能很棒，当你无法通过常规方式（ROP的堆栈中存在坏字符）控制堆栈数据时，你同样可以通过这样一条指令完成前方堆栈数据的配置，以及API调用前堆栈的部署。

#### mov [edx],ecx

![图片丢失，请联系作者](http://rootkiter.com/images/2015_04_23_21_33/2_4_2_6.png)  
这片指令，也能起到写内存的作用，如果你有足够的闲心，再配合上 inc edx 这种指令进行内存计算，一定能把一整段shellcode写到一个可执行的内存片中。

## 回顾
本文介绍了ntdll中的一些有趣的指令素材，旨在扩充人们对于ROP指令素材的认识，很多人认为ROP素材能做的事情非常有限，通过这篇文章相信你就能很清楚的意识到，ROP指令也可以很艺术，其实我一直相信某些特殊组合的ROP指令素材同样也能具备“图灵完备”性质。当然了，这需要有足够的创造性能力。

***PS: 这是我两年之前写的一篇笔记，现在看这些文字，已经成为了上个世纪的东西。漏洞利用（软件类）的攻防也上升到了一个全新的阶段。现阶段软件漏洞利用让人感觉门槛更高了，DVE技术也开始要求利用者对脚本语言的JIT形态有一定了解，希望在掌握更多基础知识之后，回过头来能追上大牛们的步伐吧。***

