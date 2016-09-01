--- 
layout: post
title:  IDAPython的列表选择器
date:   2016-09-01
time:   21:49:00
tags : [ 技术相关 ]

---

### IDAPython

最近在研究IDAPython，在做选择器相关的学习的时候，发现书上和网上大部分都是idc脚本的知识，而IDAPython的资料相对较少。搞了一天，才把选择器相关的东西搞清楚，这里记录一下。

### 弹出式选择框

#### 执行效果

弹出展示对话框，当双击相应选项时，得到选择结果并销毁该对话框。
![]()

#### 对应代码

<code>
itemlist=["item1","item2"]mchoose= Choose(itemlist,"choose an item",1)mchoose.width=20itemid=mchoose.choose()print "itemid :",itemidprint "itemvalue:",itemlist[itemid-1]
</code>

### 嵌入式选择框

#### 执行效果

在最上层窗口新建一个tab标签，并展示该选择框，这种选择框会一直存在直到用户主动关闭。当用户进行选择时，输出窗口会以默认格式输出选择结果：
![]()
![]()

#### 对应代码

<code>
itemlist=["item1","item2"]mchoose= Choose(itemlist,"choose an item",0)mchoose.width=20itemid=mchoose.choose()print "itemid :",itemidprint "itemvalue:",itemlist[itemid-1]
</code>

### 自定义选择框在嵌入式选择框中，输出结果为默认格式，且窗口为异步交互，开发者完全无法进行选择结果的捕获，此时如果开发者想要捕获选择结果，则需要通过类继承的方式实现。
#### 执行效果

在嵌入式对话框中，以自定义格式输出选择结果。
![]()

#### 对应代码

<code>
class MyChoose(Choose):      def __init__(self,mlist,title,flag):          Choose.__init__(self,mlist,title,flag)          self.mlist=mlist          self.width=20      def enter(self,n):          print "Item ID : ",n          print "Item Value: ",self.mlist[n-1]  itemlist=["item1","item2"]  mchoose= MyChoose(itemlist,"choose an item",0)  itemid=mchoose.choose()  
</code>

### 嵌入式多列选择框

在之前的选择框中，均为单列选择框（每一选项只有一列内容），当需要对该选项进行更详细的描述时，便无法展示了。此时使用多列的选择框，便可以展示更多的细节信息。

#### 执行效果


![]()

#### 对应代码

<code>
class MyChoose2(Choose2):      def __init__(self, title,header,items):          Choose2.__init__(self, title, header)          self.n = 0          self.icon = 41          self.items = items      def OnClose(self):          print "closed ", self.title      def OnSelectLine(self, n):          print str(self.items[n-1])      def OnGetLine(self, n):          return self.items[n]      def OnGetSize(self):          return len(self.items)  header=[ ["header1", 10 | Choose2.CHCOL_HEX], ["header2", 30 | Choose2.CHCOL_PLAIN] ]  items =[["item2","hit item2"],["item1","hit item1"]]  c = MyChoose2("My Item Choose list",header,items)  print c.Show()  
</code>

### 弹出式多列选择框主体代码同“嵌入式多列选择框”相同。仅有Show函数调用时要指定一个参数。#### 执行效果

弹出展示对话框，当双击相应选项时，得到选择结果并销毁该对话框。
![]()

#### 对应代码

<code>
class MyChoose2(Choose2):      def __init__(self, title,header,items):          Choose2.__init__(self, title, header)          self.n = 0          self.icon = 41          self.items = items      def OnClose(self):          print "closed ", self.title      def OnSelectLine(self, n):          print str(self.items[n-1])      def OnGetLine(self, n):          return self.items[n]      def OnGetSize(self):          return len(self.items)  header=[ ["header1", 10 | Choose2.CHCOL_HEX], ["header2", 30 | Choose2.CHCOL_PLAIN] ]  items =[["item2","hit item2"],["item1","hit item1"]]  c = MyChoose2("My Item Choose list",header,items)  itemid=c.Show(True)  print "itemID   :",itemid  print "itemValue:",items[itemid]  
</code>


