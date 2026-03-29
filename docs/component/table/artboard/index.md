> 来源：[https://developers-watch.vivo.com.cn/component/table/artboard/](https://developers-watch.vivo.com.cn/component/table/artboard/)
> 更新时间：2025/02/24 15:08:18

# artboard

提供可交互的界面，接收用户的笔画输入

### 子组件

不支持

### 属性

支持[通用属性](../../common/common-attributes/index.md)

### 样式

支持[通用样式](../../common/common-styles/index.md)

| 名称 | 类型 | 默认值 | 必填 | 描述 |
| --- | --- | --- | --- | --- |
| default-pen-color | `<color>` | #000 | 否 | 画笔颜色 |
| default-pen-size | `<length>` | 24px | 否 | 画笔尺寸 |
| width | `<length>` \| `<percentage>` | - | 否 | 组件宽度 |
| height | `<length>` \| `<percentage>` | - | 否 | 组件高度 |

### 事件

支持[通用事件](../../common/common-events/index.md)

| 名称 | 参数 | 描述 |
| --- | --- | --- |
| changewritepanel | number[] | 轨迹点数据，格式为：[x1,y1,x2,y2,...,xn,yn,-1,0,-1,-1]，其中最后四位 -1,0,-1,-1 为笔画结束符 |

### 方法

| 名称 | 参数 | 描述 |
| --- | --- | --- |
| clearData | 无 | 清除轨迹 |
