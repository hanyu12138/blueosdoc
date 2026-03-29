> 来源：[https://developers-watch.vivo.com.cn/api/system/settings/](https://developers-watch.vivo.com.cn/api/system/settings/)
> 更新时间：2024/09/02 14:53:40

# 系统设置

## 接口声明

```json
{ "name": "blueos.service.settings" }
```

## 导入模块

```ts
import settings from '@blueos.service.settings'
```

## 在工程里面的 manifest 文件中配置如下内容

### 申请权限

```json
{
  "permissions": [{ "name": "watch.permission.SETTINGS" }]
}
```

## 接口定义

### settings.getValue(OBJECT)

获取设置

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| key | String | 是 | 相应设置的字段名 |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| key | String | 相应设置的字段名 |
| value | String/Object/Array 等 JS 原生对象 | 相应设置的值 |

#### 示例：

```ts
settings.getValue({
  key: 'brightness',
  success: function (data) {
    console.log(data.key + ': ' + data.value)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### settings.getValueSync(String)

同步获取设置

#### 参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| key | String | 是 | 相应设置的字段名 |

#### 返回值

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| value | String/Object/Array 等 JS 原生对象 | 相应设置的值 |

#### 示例

```ts
const value = settings.getValueSync('brightness')
```

#### 设置相关的字段

##### brightness 屏幕亮度

| 字段名 | 类型 | 功能 | 说明 |
| --- | --- | --- | --- |
| brightness | Number | 系统屏幕亮度值设置 | 取值范围 0-255 |

```js
{
  brightness: 60
}
```

##### wearHand 佩戴手

| 字段名 | 类型 | 功能 | 说明 |
| --- | --- | --- | --- |
| wearHand | String | 佩戴手设置 | `L`: 左手， `R`: 右手 |

```js
{
  wearHand: 'R'
}
```

##### raiseWristSwitch 抬腕监听开关

注意: 此处的监听仅代表用户感知的监听设置，和真实的监听无关

| 字段名 | 类型 | 功能 | 说明 |
| --- | --- | --- | --- |
| raiseWristSwitch | Boolean | 抬腕监听开关设置 | `true`: 开启抬腕监听， `false`: 关闭抬腕监听 |

```js
{
  raiseWristSwitch: true
}
```

##### raiseWristSensitivity 抬腕监听灵敏度

注：灵敏度改变会影响 sensor 接口监听的灵敏度

| 字段名 | 类型 | 功能 | 说明 |
| --- | --- | --- | --- |
| raiseWristSensitivity | String | 抬腕监听灵敏度设置 | `H`: 高灵敏度， `M`: 标准灵敏度 |

```js
{
  raiseWristSensitivity: `H`
}
```

##### silentMode 静音模式

| 字段名 | 类型 | 功能 | 说明 |
| --- | --- | --- | --- |
| silentMode | Boolean | 静音模式设置 | `true`: 开启静音模式， `false`: 关闭静音模式 |

```js
{
  silentMode: false
}
```

##### flipScreen 屏幕翻转

| 字段名 | 类型 | 功能 | 说明 |
| --- | --- | --- | --- |
| flipScreen | Boolean | 屏幕翻转设置 | `true`: 翻转到正向， `false`: 翻转到反向 |

```js
{
  flipScreen: false
}
```
