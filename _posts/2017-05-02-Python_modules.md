--- 
layout: post
title:  新写的几个Python模块
date:   2017-05-02
time:   20:19:00
tags : [ 技术相关, Python , 数据分析 ]

---


## 模块功能

最近工作中经常遇到 

> 数据比对  
> hex 数值输出  

这些功能很简单，但已有的解决方案普遍很笨重，不适合快速验证结论的场景。

所以简单整理了一下近期的需求，写了几个基础模块，并放在[github上](https://github.com/rootkiter/easycode)，用的时候 curl/wget 一下即可直接用了，这样会舒服一些。

## 制表模块

### 为了续命
很多时刻，我只想得到一个这样的表格，以便找到程序中的 Bug 或者对比一坨新数据：

```
+-------+-----------------+-----------------+--------+
|       |      title1     |      title2     | title3 |
+-------+-----------------+-----------------+--------+
| item1 |       Hello 1*1 | Hello 1*2 AAAAA |     20 |
| item2 | Hello 2*1 BBBBB |       Hello 2*2 |    500 |
+-------+-----------------+-----------------+--------+
```

原始的重量级做法是配置一个简单的 Django 服务器，写一段配套代码，去展示。
而轻量一些的做法是将每一次的处理结果拷贝到 excel 表格中用表格去做统计分析。

如果每天都面对不同纬度的数据，每一次分析都要用无数次实验才能得到合理结果，你就会有想死的冲动了（不开玩笑，最近一直在研读《死亡美学》这本书，收获颇丰）。

最终我只好写个模块为自己续命，tablemap 肩上的重担很重呀。

### 如何获取

输入以下命令即可获得到最新版的模块。

```
wget https://raw.githubusercontent.com/rootkiter/easycode/master/tablemap.py
```

在文件的 \_\_main\_\_ 函数中有使用样例，方便记忆，也可以参考下面的说明来使用。


### 一个简单的样例

同把“大象装冰箱”一样简单的三步，创建一个表格 / 把内容装进去 / 输出表格，完活。

代码样例：


```
##  创建一个表格
from tablemap import *
tbmap = tablemap()
```

```
##  添加元素
tbmap.additem("title1",'item1',"Hello 1*1")
tbmap.additem("title2",'item1',"Hello 1*2 AAAAA")
tbmap.additem("title3",'item1','20')
tbmap.additem("title1",'item2',"Hello 2*1 BBBBB")
tbmap.additem("title2",'item2',"Hello 2*2")
tbmap.additem("title3",'item2','500')
```

```
##  表格输出
print tbmap.printMap()
```

通常来讲，`步骤1` 和 `步骤3` 是死代码， 拿过来直接用即可，无需更改，只需要把精力放在填表即可，以上代码的运行结果效果图如下：

```
$ python test.py 
+-------+-----------------+-----------------+--------+
|       |      title1     |      title2     | title3 |
+-------+-----------------+-----------------+--------+
| item1 |       Hello 1*1 | Hello 1*2 AAAAA |     20 |
| item2 | Hello 2*1 BBBBB |       Hello 2*2 |    500 |
+-------+-----------------+-----------------+--------+
```

“列名部分”居中，“内容部分”右对齐，每一列的大小也由模块自动计算调整。
在`第2步`中，每一次指定了表格的一个内容元素，以及其对应的行名和列名，模块自动完成填表过程，对于未定义过的行列名，模块也可以自动处理，无需人为干预。

### 指定列展示

如果只想挑选某几列的内容进行内容展示，可以通过向 printMap() 传参的方式来控制。当我只需要对比  title1,title3 两列的结果时，调用方法如下：

```
##  Only title1, title3
print tbmap.printMap( ['title1','title3'] )
```

此时即可得到如下忽略 title2 的输出结果：

```
$ python test.py 
+-------+-----------------+--------+
|       |      title1     | title3 |
+-------+-----------------+--------+
| item1 |       Hello 1*1 |     20 |
| item2 | Hello 2*1 BBBBB |    500 |
+-------+-----------------+--------+
```

### 指定列展示顺序

列顺序还可以通过调整参数顺序来指定：

```
##  调整列顺序
print tbmap.printMap( ['title2','title3','title1'] )
```

```
+-------+-----------------+--------+-----------------+
|       |      title2     | title3 |      title1     |
+-------+-----------------+--------+-----------------+
| item1 | Hello 1*2 AAAAA |     20 |       Hello 1*1 |
| item2 |       Hello 2*2 |    500 | Hello 2*1 BBBBB |
+-------+-----------------+--------+-----------------+
```

### 对齐样式

观察列表内容不难发现，title3 这一列在右对齐下有比较好的展示效果，
而余下的两列展示效果欠佳，调整为右对齐会获得比较直观的结果，左对齐可以通过添加减号的方式来指定，样例如下：

```
##  将title1 列设置为左对齐，其他列不变
print tbmap.printMap( ['title2','title3','-title1'] )
```

```
$ python test.py 
+-------+-----------------+--------+-----------------+
|       |      title2     | title3 |     title1      |
+-------+-----------------+--------+-----------------+
| item1 | Hello 1*2 AAAAA |     20 | Hello 1*1       |
| item2 |       Hello 2*2 |    500 | Hello 2*1 BBBBB |
+-------+-----------------+--------+-----------------+
```

### 为表格命名

当表格数量过多时，需要对表格进行一个命名，以便区分表格，
在输出前为表格指定一个名字即可完成这一目标，代码样例如下：

```
##  为表格指定名字
tbmap.setTitle("Test Table")
print tbmap.printMap()
```

```
$ python test.py 
+----------------------------------------------------+
|                    *Test Table*                    |
+-------+-----------------+-----------------+--------+
|       |      title1     |      title2     | title3 |
+-------+-----------------+-----------------+--------+
| item1 |       Hello 1*1 | Hello 1*2 AAAAA |     20 |
| item2 | Hello 2*1 BBBBB |       Hello 2*2 |    500 |
+-------+-----------------+-----------------+--------+
```

## 十六进制输出

在逆向统计中，要经常验证提取出的数据内容，`hexdump`可以在大部分情况获得比较好的执行结果， 但总有一些情况，我希望能从代码中直接展示出来，hexmap就是这样一个模块，用法如下：

### 模块获取
```
wget https://raw.githubusercontent.com/rootkiter/easycode/master/hexmap.py
```


### 模块使用
```
from hexmap import *
Adata = "ABCDEFGHIJK\x11\x22\x33\x44\x55\x66"
print str(hexmap(Adata))
```

### 执行结果
```
$ python test.py
0x0000    41 42 43 44 45 46 47 48  49 4a 4b 11 22 33 44 55    ABCDEFGHIJK*"3DU
0x0010    66                                                  f               
-----> packet size :hex(0x11),ord(17) <-------
```

## 其他
在项目库中还有一个`多线程参数更新`的小模块，模块很小，只完成了随时更新线程的功能，感兴趣可以去看一下主函数中的样例，这里就不再细说了。

## 结

春暖花开，又到了博客长草的季节，今天碰巧是“国际除草日”，例行除草（**没错，就是在一本正经地胡说八道**）。

上周刚刚取得工具链搭建的阶段性胜利，目前 IoT 样本逆向工具链中的几个关键点都成功占坑，在后面的工作中要实际测试效果了。

如果碰巧效果比较符合预期，可能还会挑选几个低耦合的模块在这里介绍下。从已知资料来看这套工具的设计思路大概是前无古人的，其整体目标性很明确，且模块间功能互补，希望它们能辅助一波 IoT 的僵尸网络追踪。
