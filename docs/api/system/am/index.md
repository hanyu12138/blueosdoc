> 来源：[https://developers-watch.vivo.com.cn/api/system/am/](https://developers-watch.vivo.com.cn/api/system/am/)
> 更新时间：2024/03/14 09:45:42

# 应用管理

## 接口声明

### JS 接口声明

```json
{ "name": "blueos.app.appmanager.appState" }
```

### 导入模块

```ts
import am from '@blueos.app.appmanager.appState'
```

## 在工程里面的 manifest 文件中配置如下内容

### 申请权限

```json
{
  "permissions": [{ "name": "watch.permission.AM" }]
}
```

### 应用状态

蓝河应用的状态有三种，应用处于前台，后台以及应用未运行。对应的三种状态值枚举如下：

| 状态值 | 说明 |
| --- | --- |
| foreground | 应用处于前台 |
| background | 应用处于后台 |
| noRunning | 应用未运行 |

## JS 接口定义

### am.moveTaskToBack()

将当前栈顶应用移动到后台

#### 参数

无

#### 返回值

如果当前任务成功移动到后台，则返回值为 `true`，否则返回值为 `false`。

示例

```js
am.moveTaskToBack()
```
