> 来源：[https://developers-watch.vivo.com.cn/api/system/screen/](https://developers-watch.vivo.com.cn/api/system/screen/)
> 更新时间：2023/12/25 11:01:05

# 屏幕管理

## 接口声明

```json
{ "name": "blueos.hardware.display.screen" }
```

## 导入模块

```ts
import screen from '@blueos.hardware.display.screen' 或 const screen = require('@blueos.hardware.display.screen')
```

## 接口定义

### screen.getScreenOffTime()

获取熄屏时间

##### 参数：

无

#### 返回值：

| 类型 | 说明 |
| --- | --- |
| Number | 1-999 秒 |

#### 示例：

```ts
screen.getScreenOffTime()
```

### screen.getAodStatus()

获取 AOD 状态

> AOD：Always on Display，即不点亮整块屏幕的情况下，控制屏幕局部亮起，将一些重要的信息一直显示在屏幕上。

#### 参数：

无

#### 返回值：

| 类型 | 说明 |
| --- | --- |
| Number | 0: AOD 关闭; 1: AOD 打开 |

#### 示例：

```ts
screen.getAodStatus()
```
