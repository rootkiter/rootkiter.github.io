---
layout: post
title:  Android下的NDK
date:   2015-08-06
time:   23:13:00
tags : [ ARM , NDK , ANDROID ,技术相关 ]

---

## 前言 
这也是很久之前写的一篇学习笔记，刚翻出来瞅了一眼，有些小细节还是已经有些过时了，看来技术的变更速度真的是太快了。既然也是曾经的劳动成果，那就同样拿出来简单的整理一下吧。

该笔记参考http://blog.sina.com.cn/s/blog_61b056970100sy0u.html博文而成。

### 环境搭建   
首先，jdk，eclipse，android sdk ，android ndk ，cygwin ，cdt，adt你肯定要安装好吧，没安装好的同学请百度下相关配置教程，这不是我文章的重点。  

## 编写helloworld  

### 编写Jni接口：  
1. 在资源目录下创建 jni.java文件
![rootkiter.com](/images/2015_08_06_22_43/1.png)  
2. 声明jni接口
![rootkiter.com](/images/2015_08_06_22_43/2.png)   
3. 命令行模式下进入src目录执行javac jni.java  
![rootkiter.com](/images/2015_08_06_22_43/3.png)    
4. 将生成的 .class 文件拷贝到 /bin 目录下的对应路径并覆盖
![rootkiter.com](/images/2015_08_06_22_43/4.png)  

5. 命令行进入 /bin/classes/ 目录 执行javah  –jni com.example.killndk.Jni  生成一个 .h  文件：
![rootkiter.com](/images/2015_08_06_22_43/5.png)  

6. 在根目录下创建jni文件夹用于保存C程序代码，并将刚生成的.h文件拷贝进去：  

7. 以jni目录为根目录建立C工程，添加C源码以及.mk  文件。
![rootkiter.com](/images/2015_08_06_22_43/6.png)   
[Android.mk](/files/Android.txt)  
[com\_example\_killndk\_Jni.c](/files/com_example_killndk_Jni.txt)  
8. 在android工程上配置编译选项：
![rootkiter.com](/images/2015_08_06_22_43/7.png)  

9. 左侧选择Builders，右侧选择New按钮，添加编译选项：  
填写编译配置信息：  
![rootkiter.com](/images/2015_08_06_22_43/8.png)  
10. 这一页主要是填写与cygwin相关的绝对路径，以及工程的绝对路径，各位需要根据实际情况予以调整。  
![rootkiter.com](/images/2015_08_06_22_43/9.png)  
11. C代码被编译后会放在libs目录下。  
![rootkiter.com](/images/2015_08_06_22_43/10.png)  
12. C的相关代码放在jni目录下。    
配置完成后，每次jni文件夹发生变化，就会自动执行makefile命令了。  
13. 现在可以通过Jni定义的接口来访问C语言函数了：  
![rootkiter.com](/images/2015_08_06_22_43/11.png)  

14. 看看执行效果吧，还算不错：
![rootkiter.com](/images/2015_08_06_22_43/12.png)  


## 编写内嵌汇编

由于NDK的C代码是通过gcc编译而成的，则必然支持内嵌汇编式的编程，并通过汇编方式实现C语言无法实现的功能，下面就介绍一下通过NDK如何进行内嵌汇编式编程。  

注意：gcc本身的去除冗余效率是非常高的，除极特殊原因不建议使用内嵌汇编式编程。

内嵌汇编式编程同其它NDK编程基本类似，需要注意的是Arm的函数调用方式采用快速调用的方法，形参均通过寄存器进行直接传递，在编写内嵌汇编程序时要注意形参同寄存器的对应关系。下面给出“参数加一函数”的内嵌汇编实现。
![rootkiter.com](/images/2015_08_06_22_43/13.png)  

可以看出，key的值被自动关联为R2寄存器，且返回值也被自动的关联为R0寄存器。

如果想要关注更多关于gcc for arm下的内嵌汇编编程可以参照这篇文章[传送门](www.ethernut.de/en/documents/arm-inline-asm.html)。


## 结束  
13年的学习笔记，现在看就有些过时了。知识更新真是太快了。。。当时高考报志愿，怎么就偏偏选了这么一个专业呢。。。

 



