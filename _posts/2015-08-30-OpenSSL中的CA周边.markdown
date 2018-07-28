---
layout: post
title:  OpenSSL中的CA周边（三）
date:   2015-08-29
time:   23:09:00
tags : [ 技术相关,OpenSSL , 数字签名 , CA , RSA＋DSA＋DH ]

---

## 前言   
最近在读OpenSSL的命令参数，在这个学习过程中发现OpenSSL之中，架构了一个非常庞大的理论系统，结果原以为学习一两天就能学完的基础知识，整整学了两个星期，才学到一些皮毛。

之前整理了一些OpenSSL相关的学习笔记，这篇将涉及一些OpenSSL中和CA有关的知识。  

## 架设CA服务器  

OpenSSL提供了CA指令用于CA服务器的模拟，这个模拟环境能够可以模拟证书的签发吊销等常见CA的操作。CA服务器的目录结构相对复杂，如下所示：

![rootkiter.com](/images/2015_08_30_00_02/1.png) 

为便于测试人员使用，OpenSSL提供了一个perl脚本（/usr/lib/ssl/misc/CA.pl），以便自动生成CA的环境目录，命令序列如下所示：  
<cmd>
$ mkdir CA/ && cd CA/  
$ cp /usr/lib/ssl/misc/CA.pl ./  
$ ./CA.pl -newca  
</cmd>

命令执行后，环境中会自动生成一个自签名的CA根证书(demoCA/cacert.pem)，以及对应的私钥文件(demoCA/private/cakey.pem)。  
可以使用x509和rsa 两个指令查看相应文件的内容。指令如下所示：  
<cmd>
$ openssl x509 -in demoCA/cacert.pem -text -noout  
$ openssl rsa -in demoCA/private/cakey.pem -passin pass:12345678 -text –noout  
</cmd>

相关字段的具体含义请参考《[从百度证书开始](/2015/08/25/从百度证书开始.html)》和《[OpenSSL中的非对称算法](/2015/08/27/OpenSSL中的非对称算法.html)》两篇学习笔记中的介绍。

## 生成证书请求 

CA签发证书前，要对客户的证书请求进行验证（除了对文件的内容进行验证以外，更多的其实是申请流程的认证，提交各种不同种类的证明材料），当验证无误后才会进行证书的颁发。所以证书请求一般由客户方提出，下面分别介绍下不同种类的证书请求生成方法.

### 生成RSA证书请求

#### 直接生成

在创建rsa密钥的同时生成证书请求，指令格式如下：  
<cmd>
$ openssl req -new -newkey rsa:1024 -keyout privkey.pem -passout pass:12345678 -out req.pem
</cmd>

查看证书请求中的内容，指令格式如下：  
<cmd>
$ openssl req -in req.pem -text -noout
</cmd>

![rootkiter.com](/images/2015_08_30_00_02/2.png) 

可以看到证书请求文件中包含公钥以及证书所属者的字段，下方的Signature Algorithm字段为自己的私钥的签名值，可确保证书请求的真实性。

#### 从RSA密钥生成  

有些时候客户手中已经握有密钥，且希望从已有的密钥生成证书请求。指令如下所示：  
<cmd>
$ openssl req -new -key rsaprivkey.pem -out req.pem
</cmd>

在openssl的交互提示下录入必要的申请者信息即可。此时生成的请求文件同直接生成的请求结构大体相同，如下所示：  
<cmd>
$ openssl req -in req.pem -text -noout
</cmd>

![rootkiter.com](/images/2015_08_30_00_02/3.png) 

### 生成DSA证书请求

#### 直接生成

由于dsa密钥的生成需要有一个dsa参数文件， dsa参数文件的生成可以使用以下命令：  
<cmd>
$ openssl dsaparam -out dsaparam.pem 1024
</cmd>

在创建dsa密钥的同时生成证书请求，指令格式如下：  
<cmd>
$ openssl req -new -newkey dsa:dsaparam.pem -keyout dsakey.pem -out req.pem -passout pass:12345678
</cmd>

查看证书请求中的内容，指令如下所示：  
<cmd>
$ openssl req -in req.pem -text -noout
</cmd>

DSA的证书请求看起来似乎复杂一些，但多出来的内容也只是dsa公钥的相关参数，所以单从请求结构上看还是相同的。

![rootkiter.com](/images/2015_08_30_00_02/4.png) 

#### 从DSA密钥生成
有些时候客户手中已经握有密钥，且希望从已有的密钥生成证书请求。指令如下所示：  
<cmd>
$ openssl req -new -key dsa512\_1.key -out req.pem
</cmd>

在openssl的交互提示下录入必要的申请者信息即可。此时生成的请求文件同直接生成的请求结构大体相同，如下所示：  
<cmd>
$ openssl req -in req.pem -text -noout
</cmd>

![rootkiter.com](/images/2015_08_30_00_02/5.png) 

## CA操作

### 签发一个证书

CA收到证书请求后，会对客户提供的各种证明资料进行审核，审核通过后会进行证书颁发工作，证书的颁发指令格式如下所示：  
<cmd>
rootkiter@PC:~/CA$ openssl ca -in ~/RSA/req.pem -out ~/RSA/cert.cer -notext
</cmd>

此时，cert.cer就是颁发完成的证书了。可以通过x509指令进行内容查看，指令如下所示：

![rootkiter.com](/images/2015_08_30_00_02/6.png) 

### 批量签署证书请求
在“生成证书请求”的章节，已经生成了多个种类的证书，可以将这些证书放到一个目录下，进行批量签署，如下所示：

![rootkiter.com](/images/2015_08_30_00_02/7.png) 

批量签署命令格式如下所示：  
<cmd>
$ openssl ca -notext -infiles ~/reqs\_file/careq\_dsa\_req.pem ~/reqs\_file/careq\_rsa\_req.pem ~/reqs\_file/dsa\_req.pem
</cmd>

### 查看CA签署过的证书
demoCA目录下有个index文件，该文件记录着该CA签署过的证书内容，可以通过cat指令查看，如下所示：   
<cmd>
$ cat demoCA/index.txt
</cmd>

![rootkiter.com](/images/2015_08_30_00_02/8.png) 

其中第三列为证书的序列号内容，在ca指令的 status选项下，可以通过指定这个序列号，来查看这个证书当前的状态，指令如下所示：  
<cmd>
rootkiter@PC:~/CA$ openssl ca -status FE2B37D676F58905
</cmd>

![rootkiter.com](/images/2015_08_30_00_02/9.png) 

### 证书吊销
当客户的密钥出现问题后（被窃取或者丢失），需要进行证书吊销，吊销指令如下所示：  
<cmd>
$ openssl ca -revoke ~/RSA/cert.cer -crl\_reason keyCompromise
</cmd>

吊销后在查看该证书，可以发现其已经吊销成功，如下图所示：  

![rootkiter.com](/images/2015_08_30_00_02/10.png) 

### 生成吊销列表

为了方便公众查询证书的吊销状态，ca指令提供了生成吊销列表的指令，格式如下所示：  
<cmd>
$ openssl ca -gencrl -crldays 7 -crlhours 7 -out crl.crl
</cmd>

可以通过 crl指令查看吊销列表内容，指令格式如下所示：  
<cmd>
$ openssl ca -crl -in crl.crl -text -noout
</cmd>

![rootkiter.com](/images/2015_08_30_00_02/11.png) 

## 证书验签
证书验签方法可以参考《[从百度证书开始](/2015/08/25/从百度证书开始.html)》笔记中的相关内容。

## 总结  
这篇学习笔记记录了OpenSSL中和CA相关的一些操作指令，以及背景知识。


