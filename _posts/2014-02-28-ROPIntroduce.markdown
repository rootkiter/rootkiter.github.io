---
layout: post
title:  "ROP Introduce"
date:   2014-02-28
time:   20:56:17
tags:   
     - nil
music:  backmusic.mp3
---
## 背景介绍

*DEP保护*

DEP 保护是缓冲区溢出攻击出现后，出现的一种防护机制，
它的核心思想就是将内存分块后，设置不同的保护标志，
令表示代码的区块拥有执行权限，而保存数据的区块仅有
读写权限，进而控制数据区域内的shellcode无法执行。

下面的两幅图分别表示了数据区域内“不可执行”和“
可执行”的状态：
<img 
src="http://rootkiter.{{ site.domain }}/image/ropimage/ROP1-1.png" title="ropimage/ROP1-3.png" align="center">

<img 
src="http://rootkiter.{{ site.domain }}/image/ropimage/ROP1-2.png" title="ropimage/ROP1-3.png" align="center">

DEP的实现分为两种，一种为软件实现，是由各个操作系统
编译过程中引入的，在微软中叫SafeSEH。 另一种为硬件
实现，由 英特尔这种CPU硬件生产厂商固化到硬件中的，
也称作NX保护机制。

单从DEP的定义可以发现，这种机制应该是能够有效抑制数据
区域内shellcode执行的。此时攻击者的面前出现了一座难以
逾越的山，我喜欢叫它“王屋山”。

要想知道如何绕过这种保护机制，请详细阅读本文下面的部分。

*Ret-to-lib*

DEP 保护机制出现后，攻击者几乎无法令数据段中的shellcode
直接执行，看起来“防御技术”此时占得了先机。
    这里插一句题外话：我觉得 Hacker 永远是这个世界上
    最聪明的一群人，它们总能发现一些常人无法发现的东西。

Hacker中此时出现了一位天才，他开始教育大家，既然数据区
域没有执行状态那我们就让他们只保存数据吧，反正地址也是
数据的一部分，而内存中有还有无尽的代码供我们使用，只要
我们能把某些有趣的代码片段按照一定思路拼接起来，那么数
据区域是否可执行完全和漏洞利用就完全没有关系了。

下面我将开始详细阐述这位“天才 Hacker” 的“天才想法”：
<ul>
<li>一方面</li>
</ul>
汇编语言中有一系列非常有用的指令，我管它们叫做“RETN系列指
令”，这些指令的原始功能是当函数调用完成时，回退到上一层调
用<img 
src="http://rootkiter.{{ site.domain }}/image/ropimage/ROP1-3.png" title="ropimage/ROP1-3.png" align="center">

函数，并继续下面的执行，示意图如下：
这种DEP的保护机制，虽然安全，却令操作系统在做某些操作时受
到限制，所以操作系统中又提供了一些解除DEP保护的API供软件
开发人员调用，当攻击者在内存中定位到这些API并调用时，DEP
保护便失去作用了。这些API一直散落于内存的某些角落，当攻击
者触发它们时，就好像触发了某个密室的暗门一样，豁然开朗。

当RETN指令同这些API联系在一起时，就会产生一些奇妙的化学反
应，首先看一下原本缓冲区溢出的攻击模式：
<img 
src="http://rootkiter.{{ site.domain }}/image/ropimage/ROP1-4.png" title="ropimage/ROP1-4.png" align="center">

有了DEP后的间接利用攻击的示意图：
<img 
src="http://rootkiter.{{ site.domain }}/image/ropimage/ROP1-5.png" title="ropimage/ROP1-5.png" align="center">

可以看到在第二种模式下，EIP的控制是通过栈中的地址，以及
代码中的RETN指令共同控制的，此时栈中的数据仍然是“数据
”，而执行位置却转移到了内存的代码空间，如此下来便巧妙的
绕过了DEP保护。

那么这种绕过技术其实是基于一个特定条件的，那就是你到某个
地址一定能找到对应的包含RETN的代码片段，可以说这是当前漏
洞利用方式的薄弱环节。

