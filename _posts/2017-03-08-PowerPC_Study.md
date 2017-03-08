--- 
layout: post
title:  PPC学习笔记
date:   2017-03-08
time:   20:19:00
tags : [ 技术相关, Mirai ,汇编+bin, Iot安全 , 嵌入式汇编 , PowerPC ]

---

## PowerPC指令

**内容参考** 

《[PPC Vers202 Book1 public.pdf](http://101.96.8.165/moss.csc.ncsu.edu/~mueller/cluster/ps3/SDK3.0/docs/arch/PPC_Vers202_Book1_public.pdf)》

## 基础内容

### 基础数据结构

|基础结构| 汉语名  | 长度 | 
|:---|:---|:---|
|Quadword|四字|128bits  |
|Doubleword|双字|64bits  |
|Word|字   |32bits  |
|Halfword|半字 |16bits  |
|Byte|字节 |8bits  |

### 数字表示

*二进制  ：0bnnnn*  
*十六进制：0xnnnn*

### 通用寄存器

PPC中通用寄存器供32个，编号为 r0-r31,分别如下：

| 寄存器名  | 描述 |
|:---|:---|
|r0 | 函数开始时使用？ |
|r1 | 堆栈指针，IDA中标识为 $sp |
|r2 | 内容表指针，IDA中标识为 rtoc |
|r3|  函数调用中作为第一参数，以及返回值 |
|r4-r10|  函数或系统调用开始的参数 |
| r11 | 用在指针的调用和当做一些语言的环境指针 |
| r12 | 用于异常处理和glink代码 |
| r13 | 保留作为系统线程ID |
| r14-r31 | 作为本地变量,非易失性 |

### 专用寄存器

| 寄存器名  | 描述 |
|:---|:---|
| lr |链接寄存器，它用来存放函数调用结束处的返回地址。|
| ctr |计数寄存器,循环计数器，随特定转移操作而递减。
|xer| 定点异常寄存器，存放整数运算操作的进位以及溢出信息。|
|msr |机器状态寄存器，用来配置微处理器的设定。|
|cr | 条件寄存器，它分成8个4位字段，cr0-cr7,它反映了某个算法操作的结果并且提供条件分支的机制。|

### 浮点寄存器

由于样本逆向过程中未涉及浮点寄存器，所以这里不总结了。

### 指令格式

四字节定长指令系统，字（4字节）对齐，因此，当在指令中要表达指令地址时，低两位二进制位是无效的，对于任意合法的指令地址，低二位二进制都必然是0。

PPC全部指令集，被分为15种不同的指令格式，每种指令格式的解码方法各不相同。

## 常见指令列表：

### 基础运算

| 指令 | 指令格式 | 指令功能 |
|:---|:---|:---|
| divw  | divw rd,rs1,rs2 | rd=rs1/rs2 |
| add   | add r11, r11, r9 | r11 = r11+r9 |
| addi  | addi rd,rs,xxx | rd = rs + xxx 立即数加 |
| mullw | mullw r0, r0, r3 | r0 = r0\*r3 |
| srawi | srawi r0, r11, 8 | r0 = r11 >> 8 |
| slwi  | slwi r0, r0, 8 | r0 = r0 << 8 |
| subf  | subf r0, r0, r8 | r0 = r8-r0 |
| addze | addze r0, r0 |　推测是数值扩充指令。 0xf -> 0x0f 这种含义　｜
| clrlwi | clrlwi rd,rs,imm | rd=rs & ((1<<(32-imm)) -1) 将 rs 的高imm 位清零，结果放置于 rd寄存器| 

### 寄存器操作指令

| 指令 | 指令格式 | 指令功能 |
|:---|:---|:---|
| mflr | mflr r0 | r0=lr 函数调用起始使用，一般用于保存函数返回地址 |
| mtlr | mtlr r0 | lr=r0 函数结尾使用，还原函数返回地址，常和blr指令配合使用 |
| stwu | stwu rs,imm(rd) | 保存rs寄存器内容到内存 |
| stbx |　stbx rs,rd1,rd2   | mem[rd1+rd2] = rs 内存赋值 | 
| li  | li rd,imm | rd = imm 寄存器赋值 |
| lbzx | lbzx rd,rs1,rs2 | rd = [rs1+rs2] 内存取值 |
| lis | lis rd,imm |寄存器高位赋值 r9=xxx << 16 常和 addi 配合使用 |
| lbz | lbz rd,imm(rs) | rd=mem[rs+imm] 按字节取 |
| lhz | lhz rd, imm(rs)| rd=mem[rs+imm] 按半字取值 |
| lwz | lwz rd, imm(rs)| rd=mem[rs+imm] 按字取值 |


### 程序流控制相关指令

| 指令 | 指令格式 | 指令功能 |
|:---|:---|:---|
| mtctr | mtctr rs | 用rs寄存器的值更新计数器ctr，一般用于循环判断 |
| bdnz  |　bdnz imm | if (ctr!=0) goto pc+imm 检查ctr寄存器，并按偏移跳转 |
| cmpwi | cmpwi rd, rs, imm | rd=rs-imm 比较指令,结果放rd寄存器，常和跳转指令连用 |
| ble   | ble rs, imm |  if (rs <=0 ) goto pc+imm 按偏移跳转 |
| cmpw  | cmpw rd, rs1, rs2 | rd=rs1-rs2 比较指令，结果放rd寄存器，常和跳转指令连用 |
| bgt | bgt rs,imm | if(rs>0) goto pc+imm   按偏移跳转 |
| bl | bl imm | 以imm 地址为目标地址，跳转。 |
| blr | blr | 以lr寄存器的值为目标地址。常用在函数退出位置 |

## 总结

PowerPC(PPC)指令体系，为RISC指令集，同时也是32位定长指令，从已掌握的指令结构体系来看，除 Motorola 那个嵌入式指令集为变长指令集外，其他嵌入式CPU均为定长指令体系，定长指令的优点在于取指方便，更方便CPU从硬件层面实现流水线指令处理，从逆向结果来看，PowerPC同样具有延时指令的特点（流水线型嵌入式指令体系均有这一特点）。

PowerPC对基础数据结构的定义同其他体系不同。这是一个在算法逆向中需要注意的点。

由于指令体系为32位定长指令，而寄存器也为32位，所以在寄存器赋值时，无法在一条指令中完成32位立即数的操作，这也是所有嵌入式CPU的共性问题。

