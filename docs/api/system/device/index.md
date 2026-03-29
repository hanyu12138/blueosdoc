> 来源：[https://developers-watch.vivo.com.cn/api/system/device/](https://developers-watch.vivo.com.cn/api/system/device/)
> 更新时间：2025/03/31 14:41:09

# 设备信息

## 接口声明

```json
{ "name": "blueos.hardware.deviceInfo" }
```

## 导入模块

```ts
import device from '@blueos.hardware.deviceInfo' 或 const device = require('@blueos.hardware.deviceInfo')
```

#### 开发者需要在 manifest.json 里面配置权限：

```json
{
  "permissions": [{ "name": "watch.permission.DEVICE_INFO" }]
}
```

## 接口定义

### device.getInfo(OBJECT)

获取设备信息

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| brand | String | 设备品牌 |
| manufacturer | String | 设备生产商 |
| model | String | 设备型号 |
| product | String | 设备代号 |
| osType | String | 操作系统名称 |
| osVersionName | String | 操作系统版本名称 |
| osVersionCode | Integer | 操作系统版本号 |
| platformVersionName | String | 运行平台版本名称 |
| platformVersionCode | Integer | 运行平台版本号 |
| language | String | 系统语言 |
| deviceName | String | 设备名称 |
| hardwareVersion | String | 硬件版本 |
| softwareVersion | String | 软件版本 |
| region | String | 系统地区 |
| screenWidth | Integer | 屏幕宽 |
| screenHeight | Integer | 屏幕高 |
| windowWidth | Integer | 可使用窗口宽度 |
| windowHeight | Integer | 可使用窗口高度 |
| statusBarHeight | Integer | 状态栏高度 |
| screenDensity | Float | 设备的屏幕密度 |
| vendorOsName | String | 系统的名称，如 BlueOS |
| vendorOsVersion | String | 蓝河应用的版本号 |
| cutout | Array | 针对异形屏(比如刘海屏、水滴屏和开孔屏)返回异形区域的位置大小。Array 中每个 item 表示一个异形区域的描述。item 参数：<br>left:cutout 左边界距离屏幕左边距离<br>top:cutout 上边界距离屏幕上边距离<br>right:cutout 右边界距离屏幕右边距离<br>bottom:cutout 下边界距离屏幕下边距离<br>cutout 的坐标描述以竖屏为基准。即在横屏和竖屏下获取的 cutout 参数描述都是一样的。 |
| deviceType | String | 当前蓝河应用引擎的设备类型，手表版为'watch' |
| screenRefreshRate | Float | 获取屏幕显示刷新率(获取帧率可能不为 60, 90, 144 等标准帧率) |

#### 示例：

```ts
device.getInfo({
  success: function (ret) {
    console.log(`handling success， brand = ${ret.brand}`)
  },
})
```

### device.getInfoSync()

同步获取设备信息

#### 参数

无

#### 返回值

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| deviceInfo | Object | 当前设备信息,deviceInfo 参数信息如上 device.getInfo success 返回值 |

#### 示例

```ts
const deviceInfo = device.getInfoSync()
```

### device.getApiLevel(OBJECT)

获取系统支持的支持API Level

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | (apiLevel: number) => void | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 类型 | 说明 |
| --- | --- |
| number | 系统支持的支持API Level |

#### 示例

```ts
device.getApiLevel({
  success(apiLevel) {
    console.log(`apiLevel=${apiLevel}`)
  },
  fail() {}
})
```

### device.getApiLevelSync()

同步获取系统支持的支持API Level

#### 参数

无

#### 返回值

| 类型 | 说明 |
| --- | --- |
| number | 系统支持的支持API Level |

#### 示例

```ts
const apiLevel = device.getApiLevelSync();
console.log(`apiLevel=${apiLevel}`)
```

### device.getRegionSync()

同步获取设备地区信息

#### 参数

无

#### 返回值

| 类型 | 说明 |
| --- | --- |
| string | CN 中国<br>ID 印度尼西亚<br>TH 泰国<br>MY 马来西亚<br>SG 新加坡<br>PH 菲律宾<br>ZA 南非<br>CO 哥伦比亚<br>TR 土耳其<br>RU 俄罗斯 |

#### 示例

```ts
const region = device.getRegionSync()
console.log('region is', region)
```

### device.getRegion()

异步获取设备地区信息

#### 参数：

| 属性 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| success | 否 | Function | 成功回调 |
| fail | 否 | Function | 失败回调 |

#### success 返回值:

| 类型 | 说明 |
| --- | --- |
| string | CN 中国<br>ID 印度尼西亚<br>TH 泰国<br>MY 马来西亚<br>SG 新加坡<br>PH 菲律宾<br>ZA 南非<br>CO 哥伦比亚<br>TR 土耳其<br>RU 俄罗斯 |

#### 示例：

```ts
device.getRegion({
  success: function (region) {
    console.log('region is', region)
  },
})
```

### device.getPeerDeviceInfo(OBJECT)

获取连接手机的信息

#### 参数：

| 属性 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| success | 否 | Function | 成功回调 |
| fail | 否 | Function | 失败回调 |

#### success 返回值:

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| brand | String | 设备品牌 |
| osType | String | 操作系统名称 |

#### fail 返回值:

#### 示例：

```ts
device.getPeerDeviceInfo({
  success: function (ret) {
    console.log(`handling success， brand = ${ret.brand}`)
  },
})
```

### device.getId(OBJECT)

批量获取设备标识

#### 权限要求

获取手表状态

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| type | Array | 是 | 支持 device、mac、user、advertising 四种类型，可提供一至多个 |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

按照传入的 type 返回对应的 id，未在 type 中出现的 id 类型不会返回

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| device | String | 设备唯一标识。 |
| mac | String | 设备的 mac 地址。 |
| user | String | 用户唯一标识。 |
| advertising | String | 广告唯一标识 |

##### fail 返回错误代码

| 错误码 | 说明 |
| --- | --- |
| 400 | 拒绝授予权限 |
| 402 | 权限错误（未声明该权限） |

#### 示例：

```ts
device.getId({
  type: ['device', 'mac'],
  success: function (data) {
    console.log(`handling success: ${data.device}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}, errorMsg=${data}`)
  },
})
```

### device.getDeviceId(OBJECT)

获取设备唯一标识

#### 权限要求

获取手表状态

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| deviceId | String | 设备唯一标识。 |

##### fail 返回错误代码

| 错误码 | 说明 |
| --- | --- |
| 400 | 拒绝授予权限 |
| 402 | 权限错误（未声明该权限） |

```ts
device.getDeviceId({
  success: function (data) {
    console.log(`handling success: ${data.deviceId}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### device.getSerial(OBJECT)

获取设备序列号

#### 权限要求

获取手表状态

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| serial | String | 设备序列号 |

```ts
device.getSerial({
  success: function (data) {
    console.log(`handling success: ${data.serial}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### device.getTotalStorage(OBJECT)

获取存储空间的总大小

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| totalStorage | Number | 存储空间的总大小，单位是 Byte。 |

```ts
device.getTotalStorage({
  success: function (data) {
    console.log(`handling success: ${data.totalStorage}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### device.getAvailableStorage(OBJECT)

获取存储空间的可用大小

#### 参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| availableStorage | Number | 存储空间的可用大小，单位是 Byte。 |

```ts
device.getAvailableStorage({
  success: function (data) {
    console.log(`handling success: ${data.availableStorage}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### device.getDeviceICCID(OBJECT)

获取卡识别码

#### 参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| iccid | String | 卡识别码 |

```ts
device.getDeviceICCID({
  success: function (data) {
    console.log(`handling success: ${data.iccid}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### device.getCpuInfo(OBJECT)

返回 CPU 信息

#### 参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 参数值 | 类型 | 说明 |
| --- | --- | --- |
| cpuInfo | String | CPU 信息。 |

```ts
device.getCpuInfo({
  success: function (data) {
    console.log(`handling success: ${data.cpuInfo}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}`)
  },
})
```

### device.isSupported(name: string)

断硬件设备能力是否支持

#### 参数

| 类型 | 必填 | 说明 |
| --- | --- | --- |
| String | 是 | 支持的硬件能力枚举，见下文【硬件设备能力枚举】 |

##### 返回值

| 类型 | 说明 |
| --- | --- |
| Boolean | 是否支持，true 支持，false 不支持 |

##### 示例

```ts
const isSupported = device.isSupported('sys.modem.support')
```

### device.getFeatureList(OBJECT)

获取全部硬件功能列表

#### 参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| success | Function | 否 | 成功回调 |
| fail | Function | 否 | 失败回调 |
| complete | Function | 否 | 执行结束后的回调 |

##### success 返回值：

| 类型 | 说明 |
| --- | --- |
| Array<string> | 获取全部硬件功能列表，见下文【硬件设备能力枚举】 |

##### 示例

```ts
device.getFeatureList({
  success: function (data) {
    console.log(`handling success: ${data}`)
  },
  fail: function (data, code) {
    console.log(`handling fail, code = ${code}, errorMsg=${data}`)
  },
})
```

| 类型 | 说明 |
| --- | --- |
| Array<string> | 硬件设备支持的功能列表 |

## 硬件设备能力枚举

| 枚举值 | 说明 |
| --- | --- |
| sys.modem.support | modem 功能 |
| sys.sensor.ecg.support | ecg 功能 |
