---
layout: post
title: MBR分区表数据结构
category: linux
tags: []
date: 2018-02-02 11:04:20
---
<table cellspacing="0" cellpadding="0" border="1">
<tbody>
<tr>
<td valign="top">
<p><strong>起始地址（16进制）</strong></p>
</td>
<td valign="top">
<p><strong>起始地址（10进制）</strong></p>
</td>
<td valign="top">
<p><strong>长度（字节）</strong></p>
</td>
<td valign="top">
<p><strong>内容</strong></p>
</td>
</tr>
<tr>
<td valign="top">
<p>0</p>
</td>
<td valign="top">
<p>0</p>
</td>
<td valign="top">
<p>440</p>
</td>
<td valign="top">
<p>引导启动代码</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1B8</p>
</td>
<td valign="top">
<p>440</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>签名</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1BC</p>
</td>
<td valign="top">
<p>444</p>
</td>
<td valign="top">
<p>2</p>
</td>
<td valign="top">
<p>保留</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1BE</p>
</td>
<td valign="top">
<p>446</p>
</td>
<td valign="top">
<p>16×4 = 64</p>
</td>
<td valign="top">
<p>主分区表（最多四个主分区）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1FE</p>
</td>
<td valign="top">
<p>510</p>
</td>
<td valign="top">
<p>2</p>
</td>
<td valign="top">
<p>可引导磁盘签名0x55，0xAA</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<h2>MBR主分区表数据结构</h2>
<table cellspacing="0" cellpadding="0" border="1">
<tbody>
<tr>
<td valign="top">
<p><strong>起始地址（16进制）</strong></p>
</td>
<td valign="top">
<p><strong>起始地址（10进制）</strong></p>
</td>
<td valign="top">
<p><strong>长度（字节）</strong></p>
</td>
<td valign="top">
<p><strong>内容</strong></p>
</td>
</tr>
<tr>
<td valign="top">
<p><span style="color:red">1BE</span></p>
</td>
<td valign="top">
<p><span style="color:red">446</span></p>
</td>
<td valign="top">
<p><span style="color:red">16</span></p>
</td>
<td valign="top">
<p><span style="color:red">第一主分区</span></p>
</td>
</tr>
<tr>
<td valign="top">
<p>1BE</p>
</td>
<td valign="top">
<p>446</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>00：非活动，80：活动</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1BF</p>
</td>
<td valign="top">
<p>447</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C0</p>
</td>
<td valign="top">
<p>448</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C1</p>
</td>
<td valign="top">
<p>449</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C2</p>
</td>
<td valign="top">
<p>450</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>分区类型</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C3</p>
</td>
<td valign="top">
<p>451</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C4</p>
</td>
<td valign="top">
<p>452</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C5</p>
</td>
<td valign="top">
<p>453</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1C6</p>
</td>
<td valign="top">
<p>454</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第一主分区之前的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1CA</p>
</td>
<td valign="top">
<p>458</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第一主分区的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p><span style="color:red">1CE</span></p>
</td>
<td valign="top">
<p><span style="color:red">462</span></p>
</td>
<td valign="top">
<p><span style="color:red">16</span></p>
</td>
<td valign="top">
<p><span style="color:red">第二主分区</span></p>
</td>
</tr>
<tr>
<td valign="top">
<p>1CE</p>
</td>
<td valign="top">
<p>462</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>00：非活动，80：活动</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1CF</p>
</td>
<td valign="top">
<p>463</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D0</p>
</td>
<td valign="top">
<p>464</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D1</p>
</td>
<td valign="top">
<p>465</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D2</p>
</td>
<td valign="top">
<p>466</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>分区类型</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D3</p>
</td>
<td valign="top">
<p>467</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D4</p>
</td>
<td valign="top">
<p>468</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D5</p>
</td>
<td valign="top">
<p>469</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1D6</p>
</td>
<td valign="top">
<p>470</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第二主分区之前的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1DA</p>
</td>
<td valign="top">
<p>474</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第二主分区的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p><span style="color:red">1DE</span></p>
</td>
<td valign="top">
<p><span style="color:red">478</span></p>
</td>
<td valign="top">
<p><span style="color:red">16</span></p>
</td>
<td valign="top">
<p><span style="color:red">第三主分区</span></p>
</td>
</tr>
<tr>
<td valign="top">
<p>1DE</p>
</td>
<td valign="top">
<p>478</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>00：非活动，80：活动</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1DF</p>
</td>
<td valign="top">
<p>479</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E0</p>
</td>
<td valign="top">
<p>480</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E1</p>
</td>
<td valign="top">
<p>481</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E2</p>
</td>
<td valign="top">
<p>482</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>分区类型</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E3</p>
</td>
<td valign="top">
<p>483</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E4</p>
</td>
<td valign="top">
<p>484</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E5</p>
</td>
<td valign="top">
<p>485</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1E6</p>
</td>
<td valign="top">
<p>486</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第三主分区之前的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1EA</p>
</td>
<td valign="top">
<p>490</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第三主分区的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1EE</p>
</td>
<td valign="top">
<p>494</p>
</td>
<td valign="top">
<p><span style="color:red">16</span></p>
</td>
<td valign="top">
<p><span style="color:red">第四主分区</span></p>
</td>
</tr>
<tr>
<td valign="top">
<p>1EE</p>
</td>
<td valign="top">
<p>494</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>00：非活动，80：活动</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1EF</p>
</td>
<td valign="top">
<p>495</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F0</p>
</td>
<td valign="top">
<p>496</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F1</p>
</td>
<td valign="top">
<p>497</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>起始柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F2</p>
</td>
<td valign="top">
<p>498</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>分区类型</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F3</p>
</td>
<td valign="top">
<p>499</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束磁头（Head）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F4</p>
</td>
<td valign="top">
<p>500</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束扇区（Sector）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F5</p>
</td>
<td valign="top">
<p>501</p>
</td>
<td valign="top">
<p>1</p>
</td>
<td valign="top">
<p>结束柱面（Cylinder）</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1F6</p>
</td>
<td valign="top">
<p>502</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第四主分区之前的扇区数</p>
</td>
</tr>
<tr>
<td valign="top">
<p>1FA</p>
</td>
<td valign="top">
<p>506</p>
</td>
<td valign="top">
<p>4</p>
</td>
<td valign="top">
<p>第四主分区的扇区数</p>
</td>
</tr>
</tbody>
</table>
