
1.路径: /add_item 添加事项
==============
只支持post请求，post数据参数为
--------------
<br>
1.content 代表事项内容
2.status 代表事项状态，0表示待办，1表示已完成
3.addtime 代表事项添加时间，格式为XXXX.XX.XX
4.deadline 代表事项截止时间，格式同上
<br>
# 2.路径: /set_to_finished/<id> 将待办设为已完成
## **只支持put请求**
<br>
### id = 0时，设置所有待办项为已完成
### id = n（n>0）时,设置相应id 的事项为已完成
### 当该id的事项不存在时，返回404错误，终止程序
<br>
# 3.路径:/get_item/<instruction>
## **只支持get请求**
<br>
### instruction = "all" 时，查询所有事项的具体记录
### instruction = "todo" 时，查询所有待办事项的记录
### instruction = "finished" 时，查询所有已完成事项的记录
### instruction 不等于上面三个之一时，返回404错误，终止程序
### 查询数据包含在返回的字典中
<br>
#4.路径:get_count/<instruction> 获取事项个数
##**只支持get请求**
<br>
### instruction = "all" 时，查询所有事项的个数
### instruction = "todo" 时，查询所有待办事项的记录个数
### instruction = "finished" 时，查询所有已完成事项的记录个数
### 返回的int变量包含在data中
### 否则返回405错误码
<br>
#5.路径:del_item_by_id/<id> 删除指定id的事项
##**只支持delete请求**
<br>
### id = x,删除id = x的事项
### 未找到该id的事项时返回404
<br>
# 6.路径:del_item_by_instruction/<instruction> 删除指定类的事项
##**只支持delete请求**
<br>
### instruction = "all" 时，删除所有事项的记录
###instruction = "todo" 时，删除所有待办事项的记录
###instruction = "finished" 时，删除所有已完成事项的记录
<br>
