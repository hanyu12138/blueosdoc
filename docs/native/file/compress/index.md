> 来源：[https://developers-watch.vivo.com.cn/native/file/compress/](https://developers-watch.vivo.com.cn/native/file/compress/)
> 更新时间：2023/11/07 10:55:31

# 压缩解压

头文件<storage/compress.h>

## 接口定义

### 解压

```ts
int BFile_decompress(
    const char* srcUri,
    const char* dstUri
);
```

#### 参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| srcUri | const char* | 源文件 uri |
| dstUri | const char* | 目标文件 uri |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 操作状态（详见 《枚举 文件压缩相关操作状态》） |

## 枚举

### 文件压缩相关操作状态

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| BFILE_COMPRESS_OK | 0 | 文件压缩相关操作成功 |
| BFILE_COMPRESSE_RROR | -1 | 文件压缩相关操作失败 |
