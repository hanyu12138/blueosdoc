> 来源：[https://developers-watch.vivo.com.cn/api/storage/localstorage/](https://developers-watch.vivo.com.cn/api/storage/localstorage/)
> 更新时间：2025/10/09 11:25:10

# K-V 数据存储

## 接口声明

```json
{ "name": "blueos.storage.storage" }
```

## 导入模块

```ts
import storage from '@blueos.storage.storage' 或 const storage = require('@blueos.storage.storage')
```

## 接口定义

### storage.get(OBJECT)

读取存储内容

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| key | String | 是 | 索引 |
| default | String | 否 | 如果 key 不存在，返回 default。如果 default 未指定，返回长度为 0 的空字符串 |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

#### success 返回值：

key 对应的存储内容

#### 示例：

```ts
storage.get({
  key: 'A1',
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### storage.getSync(OBJECT)

同步读取存储内容

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| key | String | 是 | 索引 |

#### 返回值：

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| value | String \| Boolean \| Number \| Object \| Array | key 对应的存储内容 |

#### 示例：

```ts
const value = storage.getSync({ key: 'A1' })
```

### storage.set(OBJECT)

修改存储内容

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| key | String | 是 | 索引 |
| value | String \| Boolean \| Number \| Object \| Array | 否 | 新值。如果新值是长度为 0 的空字符串，会删除以 key 为索引的数据项 |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

#### 示例：

```ts
storage.set({
  key: 'A1',
  value: 'V1',
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

#### 示例：

```ts
storage.set({
  key: 'A1',
  value: true,
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

#### 示例：

```ts
storage.set({
  key: 'A1',
  value: 18,
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

#### 示例：

```ts
storage.set({
  key: 'A1',
  value: { name: '李四', age: 18 },
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

#### 示例：

```ts
storage.set({
  key: 'A1',
  value: [18, 20],
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### storage.clear(OBJECT)

清空存储内容

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

#### 示例：

```ts
storage.clear({
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### storage.delete(OBJECT)

删除存储内容

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| key | String | 是 | 索引 |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

#### 示例：

```ts
storage.delete({
  key: 'A1',
  success: function (data) {
    console.log('handling success')
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### storage.key(OBJECT)

返回存储中某个 index 的键名

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| index | Number | 是 | 要查询的键名对应的索引 |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

#### success 返回值：

index 对应的键名

#### 示例：

```ts
storage.key({
  index: 1,
  success: function (data) {
    console.log(`handling success, key = ${data}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### 属性

| 名称 | 参数类型 | 是否可读 | 是否可写 | 描述 |
| --- | --- | --- | --- | --- |
| length | Number | 是 | 否 | 存储里的数据项的数量 |

#### 示例：

```ts
let length = storage.length
```

#### 通用 fail 回调参数定义

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| data | string | 接口失败信息描述 |
| code | FailCodeEnum | 接口失败业务码 |

#### FailCodeEnum

| 属性 | 说明 |
| --- | --- |
| 302 | 存储空间不足 |
