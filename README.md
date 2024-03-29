# 一、开发规范:

### 1.  开发模式

​	前后端分离



### 2.后端环境

- Python 3.7.3 

- Django 1.11.8
- Redis 4.0.9
- Mysql 5.5
- Ubuntu19.04

- Vim







admin后台

账号 admin

密码 admin123

### 3. 通信协议

​	https



### 4. 通信格式

​	josn



### 5.API 规范

​	一定程度上符合 RESTful 定义



# 二 、数据库结构：

采购单列表

| 字段名       | 类型 | 作用       | 备注1  | 备注2 |
| ------------ | ---- | ---------- | ------ | ----- |
|              |      | 单据类型   | 外键   |       |
|              |      | 供应商名称 |        |       |
|              |      | 是否完成   |        |       |
|              |      | 商品总量   |        |       |
|              |      | 入库总量   |        |       |
|              |      | 未入库数量 |        |       |
|              |      | 已发货数量 |        |       |
| created_time |      | 采购时间   |        |       |
| is_active    |      |            | 伪删除 |       |
| is_active    |      |            |        |       |
| info         |      | 备注       |        |       |





# 三、 接口说明：

## 1.进销存



### 1.1采购单列表

#### 展示字段:

| 单据类型   | 商务专员   | 供应商名称 | 是否完成 | 商品总数量 | 入库总量 |
| ---------- | ---------- | ---------- | -------- | ---------- | -------- |
| 未入库数量 | 已发货数量 | 单据金额   | 入库金额 | 采购时间   | 备注     |

#### **功能:**

​	修改采购单:  url

​	查看入库与发货明细:url   v1/模块/资源   

​	终止: 待定

​	删除 url



### 1.1.1修改采购单

#### 展示字段

| **基础**   | **付款信息** | **产品信息**        |      |      |      |
| ---------- | ------------ | ------------------- | ---- | ---- | ---- |
| 日期       | 申请单号     | 产品名称            |      |      |      |
| 总金额     | 申请人       | 目标仓库            |      |      |      |
| 申请人：   | 申请时间     | 数量                |      |      |      |
| 合同图片   | 申请金额     | 单价                |      |      |      |
| 公司       | 申请状态     | 小计(数量*单价)     |      |      |      |
| 采购人：   | 付款完成时间 | 操作(删除/申请入库) |      |      |      |
| 结算类型： |              |                     |      |      |      |
| 供应商：   |              |                     |      |      |      |
| 备注：     |              |                     |      |      |      |

#### **功能:**

​	申请入库: url 

​	删除:  url 



### 1.1.2查看入库与发货明细:

#### 展示字段

| **基础**       | 入库信息       | 发货信息   |      |      |      |
| -------------- | -------------- | ---------- | ---- | ---- | ---- |
| 日期           | 入库明细ID     | 入库明细ID |      |      |      |
| 申请人：       | 入库时间       | 出货仓库   |      |      |      |
| 总金额         | 入库商品       | 发货ID     |      |      |      |
| 状态(是否完成) | 仓库           | 发货日期   |      |      |      |
| 供应商         | 入库(调整)类型 | 订单号     |      |      |      |
|                | 数量           | 客户       |      |      |      |
|                | 单位           | 发货状态   |      |      |      |
|                | 合计           | 发货商品   |      |      |      |
|                |                | 发货破损   |      |      |      |
|                |                | 发货单价   |      |      |      |
|                |                | 发货合计   |      |      |      |
|                |                | 入库单价   |      |      |      |
|                |                | 入库成本   |      |      |      |
|                |                | 物流成本   |      |      |      |

#### **功能:**

​	无







### 1.2入库单列表

#### 展示字段

| **进出货单列表** | 采购明细(异步响应) |
| ---------------- | ------------------ |
| 明细ID           | 明细ID             |
| 单据类型         | 单据ID             |
| 申请人：         | 采购ID             |
| 供应商名称       | 商品名称           |
| 商品总数量       | 单价               |
| 单据金额         | 数量               |
| 入库时间         | 单位               |
|                  | 合计               |
|                  |                    |

#### **功能:**

​	查看入库单: url 

​	打印:  前端print

​	修改物流

​	下载入库单: 













​	查看明细(就换个样式假装一下)

​	终止(发短信提示)

- 入库单列表



- 入库明细



- 运费表



## 2. 商品(commodity)

### 2.1.0 商品列表

#### 数据库:

​	商品表   BaseClass

| 字段名       | 类型 | 作用     | 备注1                              | 备注2 |
| ------------ | ---- | -------- | ---------------------------------- | ----- |
|              |      | 商品名称 |                                    |       |
|              |      | 供应商   | 外键                               |       |
|              |      | 商品类别 | 外键     字典配置表                |       |
|              |      | 商品简介 |                                    |       |
|              |      | 商品单价 |                                    |       |
|              |      | 商品单位 | 吨/个/间/件/桶/包台/平方米/再议... |       |
|              |      | 理论重量 |                                    |       |
|              |      | x        |                                    |       |
|              |      | y        |                                    |       |
|              |      | z        |                                    |       |
| created_time |      |          |                                    |       |
| updated_time |      |          |                                    |       |
| is_active    |      |          |                                    |       |

#### 功能:

- 增
  - get
  - v1/commodity
  - {'code':200,'data':[{}..{}..]}
  - {'code':10210,'error':'字符串'}

- 删
  - delete
  - v1/commodity    (请求体   body.id = 1)
  - {'code':200,'data':"删除成功"}
  - {'code':10220,'error':'字符串'}

- 改
  - put
  - v1/commodity    (请求体   body.id = 1 ... 详细参数)
  - {'code':200,'data':"删除成功"}
  - {'code':10220,'error':'字符串'}

- 查

  - get

  - v1/commodity    (请求体   body is None)  查全部       (请求体   body.id   )查单独
  - {'code':200,'data':"删除成功"}
  - {'code':10220,'error':'字符串'}











## 3. 基础设置(dict_con)  (wwn)

### 3.1.0字典类型表

#### 数据库:

​	字典类型表   BaseClass

| 字段名       | 类型 | 作用     | 备注1 | 备注2 |
| ------------ | ---- | -------- | ----- | ----- |
| type_name    |      | 类型名称 |       |       |
| created_time |      |          |       |       |
| is_active    |      |          |       |       |

#### 功能  字典类型表操作 :

- 增: 
  - /v1/dict_con/class
  - post
  - {'code':200} 
- {'code':10111,'error':'已经存在这个类型名称'}
- 删:  /v1/dict_con    delete
  - {'code':200}
  - {'code':10120,'error':''}
- 改:   v1/dict_con    put
  - {'code':200}
  - {'code':10130,'error':''}
- 查:   v1/dict_con    
  - get
  - 参数 {id=3 }          {'code':200,'data':[{}..{}..]}
  - 参数 { }                     {'code':200,'data':[{}..{}..]}
  - {'code':10140,'error':''}
    - 10141 插入数据库报错



展示字段 id  名称 父级 字典类型 是否 展示 排序号 





### 3.2.1	类型配置表

​	类型配置表  BaseType

| 字段名            | 类型 | 作用     | 备注1               | 备注2 |
| ----------------- | ---- | -------- | ------------------- | ----- |
| type_name         |      | 类型名称 |                     |       |
| order             |      | 排序号   | 由大到小 优先级降低 |       |
| parent_type       |      | 父级类型 |                     |       |
| parent_class_type |      | 字典类型 | 外检 >字典类型表    |       |
| created_time      |      |          |                     |       |
| updated_time      |      |          |                     |       |
| is_active         |      |          |                     |       |





### 3.3.1 供应商管理

​	





### 3.4.1 仓库管理

#### 数据库:

 Warehouse

| 字段名       | 类型 | 作用       | 备注1 | 备注2 |
| ------------ | ---- | ---------- | ----- | ----- |
|              |      | 仓库名称   |       |       |
|              |      | 仓库别名   | 外键  |       |
|              |      | 仓库类型： | 外键  |       |
|              |      | 商品简介   |       |       |
| created_time |      |            |       |       |
| updated_time |      |            |       |       |
| is_active    |      |            |       |       |

#### 功能:

- 增
  - post
  - v1/dict_con/warehouse  (body中有id 查询某一个 ) {'code':200,'data':[{}..{}..]}
  - v1/dict_con/warehouse ( body没有id    返回所有激活数据)
  - {'code':10310,'error':'错误信息')所有列表
- 删
  - delete
  - 
- 改
  - put
- 查
  - get















------



------





















## 仓库管理

## 供应商管理

## 报表

## 对账单

## 物流

## 用户

### 增加

- /v1/user/





### 供应商

| 字段名       | 类型 | 作用       | 备注1             | 备注2 |
| ------------ | ---- | ---------- | ----------------- | ----- |
|              |      | 供应商名称 |                   |       |
|              |      | 供应商类别 | 外键   字典配置表 |       |
|              |      | 采购专员   | 可以为空          |       |
|              |      | 商务专员   | 可以为空          |       |
| created_time |      |            |                   |       |
| updated_time |      |            |                   |       |
| is_active    |      |            |                   |       |





### 仓库

| 字段名       | 类型 | 作用       | 备注1 | 备注2 |
| ------------ | ---- | ---------- | ----- | ----- |
|              |      | 仓库名称   |       |       |
|              |      | 仓库别名   | 外键  |       |
|              |      | 仓库类型： | 外键  |       |
|              |      | 商品简介   |       |       |
|              |      |            |       |       |
|              |      |            |       |       |
|              |      |            |       |       |
| created_time |      |            |       |       |
| updated_time |      |            |       |       |
| is_active    |      |            |       |       |



### 字典配置表

| 字段名       | 类型    | 作用       | 备注1            | 备注2 |
| ------------ | ------- | ---------- | ---------------- | ----- |
|              | varchar | 类型名称   |                  |       |
|              | int     | 所属关系表 | 仓库/商品/供应商 |       |
| created_time |         |            |                  |       |
| updated_time |         |            |                  |       |
| is_active    |         |            |                  |       |





### 用户表



| 字段名 | 类型 | 作用   | 备注1 | 备注2 |
| ------ | ---- | ------ | ----- | ----- |
|        |      | 用户名 |       |       |
|        |      | 密码   | md5   |       |
|        |      | 权限   | 外键  |       |
|        |      |        |       |       |
|        |      |        |       |       |































