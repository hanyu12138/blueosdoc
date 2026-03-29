> 来源：[https://developers-watch.vivo.com.cn/component/basic/qrcode/](https://developers-watch.vivo.com.cn/component/basic/qrcode/)
> 更新时间：2023/12/21 13:49:50

# qrcode

二维码，将文本内容转换为二维码展示。

### 子组件

不支持

### 属性

支持[通用属性](../../common/common-attributes/index.md)

| 名称 | 类型 | 默认值 | 必填 | 描述 |
| --- | --- | --- | --- | --- |
| value | `<string>` | - | 是 | 二维码内容，长度小于等于 400 字节 |
| eclevel | `<number>` | 1 | 否 | 二维码纠错等级 取值范围为 0 到 3 |
| type | normal \| circle | normal | 否 | 二维码样式设置 normal 常规样式，circle 圆点样式 |

### 样式

支持[通用样式](../../common/common-styles/index.md)

### 事件

支持[通用事件](../../common/common-events/index.md)
