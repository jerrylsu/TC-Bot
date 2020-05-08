## case1 公司员工 

### 1.1 姓名不匹配
你好，请问你是我们公司得员工吗？
is_staff
是的
is_staff: true
请问你叫什么？
self_name
我叫杰瑞
self_name:jierui  is_valid_staff: false
不好意思，名字不正确，为你联系前台。
self_name

### 1.2 姓名匹配， 密码不匹配
你好，请问你是我们公司的员工吗？
是的
请问你叫什么？
我叫杰瑞
请问你的数字密码是什么？
我的数字密码是123456
不好意思，数字密码不正确，为你联系前台

### 1.3 姓名和密码匹配

0 你好，请问你是我们公司的员工吗？
0 sys: request, inform_slots: {}, request_slots: {'is_staff': UNK}
1 是的呀！
1 usr: inform, inform_slots: {'is_staff': True}, request_slots: {}
2 请问你的名字叫什么？
2 sys: request, inform_slots: {}, request_slots: {'self_name': UNK}
3 我叫杰瑞。
3 usr: inform, inform_slots: {'self_name': 杰瑞}, request_slots: {}
4 请问你的员工数字密码是多少？
4 sys: request, inform_slots: {}, request_slots: {'digits_key': UNK}
5 我的数字密码是123456。
5 usr: inform, inform_slots: {'digits_key': 123456}, request_slots: {}
6 欢迎你，杰瑞！请进！
6 sys: inform, inform_slots: {'self_name': 杰瑞}, request_slots: {}

## case2 预约访客

### 2.1 有预约，姓名不匹配, 不找人

### 2.2 有预约，姓名不匹配, 找人， 员工名匹配

### 2.3 有预约，姓名不匹配, 找人， 员工名不匹配

### 2.4 有预约，姓名匹配，手机号不匹配，不找人

### 2.5 有预约，姓名匹配，手机号不匹配， 找人， 员工名匹配
你好，请问你是我们公司的员工吗？
is_staff
不是的
is_staff:false
请问你有预约吗？
is_reserve_visitor
我有预约
is_reserve_vistor:true
请问你的名字是什么？
self_name
我是杰瑞
self_name:jierui
请问你的手机号后四位是什么？
digits_key
我的手机号是1234
digits_key:1234
欢迎你

### 2.6 有预约，姓名匹配，手机号不匹配， 找人， 员工名不匹配

### 2.7 有预约，姓名匹配，手机号匹配，是面试

### 2.8 有预约，姓名匹配，手机号匹配，非面试， 接待

### 2.9 有预约，姓名匹配，手机号匹配，非面试， 不接待

## case3 临时访客

### 3.1 无预约，不找人

### 3.2 无预约，找人，员工名匹配
你好，请问你是我们公司的员工吗
is_staff
不是
is_staff: False
请问你有预约吗？
is_reserve_visitor
我没有预约
is_reserve_visitor: False
请问你找谁？
host_name
我找杨球松
host_name: 杨球松
为你通知杨球松
### 3.3 无预约，找人，员工名不匹配

