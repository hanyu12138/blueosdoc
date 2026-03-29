> 来源：[https://developers-watch.vivo.com.cn/api/connect/development-guidance/watch-guidance/](https://developers-watch.vivo.com.cn/api/connect/development-guidance/watch-guidance/)
> 更新时间：2023/10/31 19:37:39

# 穿戴业务 Kit

## 代码示例

#### 创建连接实例

```ts
 create() {
    console.log(`click here!`)
    connect = interconnect.instance({ package: 'com.vivo.health.deviceRpcSdk.demo', fingerprint: '5de8782b74c1e2e064786428c229ab68884e7563704d0642466bf5f51dfa1330' })
    this.create_text = "成功创建"
    this.onopen()
    this.onclose()
    this.onerror()
    this.onmessage()
    timer = setTimeout(() => {
      console.log(`等待 3s 执行send`)
      this.send()
    }, 3 * 1000)

  },
```

#### 数据发送

```ts
  send() {
    console.log('send--------')
    const self = this;
    if (connect == null) {
      console.log('interconnect feature not instanced!!')
      return
    }
    connect.send({
      data: {
        type: 'getIsLogin'
      },
      success: function () {
        self.send_status = '是'
        console.log(`handling success`)
      },
      fail: function (data, code) {
        self.send_status = '否'
        console.log(`handling fail, code = ${code}`)
      }
    })
  },
```

#### 数据接收

```ts
  onmessage() {
    console.log('onmessage--------')
    // 监听手机侧应用的数据
    const self = this
    if (connect == null) {
      console.log('interconnect feature not instanced!!')
      return
    }
    connect.onmessage = function (data) {
      if (data && data.isFileType) {
        console.log('filename is', data.fileName)
      } else {
        console.log('msg is', data)
      }
      self.onmessage_data = data
    }

  },
```

#### 断开及销毁

```ts
  close() {
    const self = this
    if (connect == null) {
      console.log('interconnect feature not instanced!!')
      return
    }
    connect.close({

      success() {
        console.log(`close success`)
        self.close_data = 'success!'
      },
      fail(data, code) {
        console.log(`handling fail, code = ${code}`)
        self.close_data = 'fail!'
      },
    })
  },

  onDestroy() {
    if(timer != null){
      clearTimeout(timer) // 清除定时函数
    }
    this.close()
  },
```

## API 参考

[vivo 智能终端设备侧](../../interconnect/index.md)
