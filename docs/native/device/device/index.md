> 来源：[https://developers-watch.vivo.com.cn/native/device/device/](https://developers-watch.vivo.com.cn/native/device/device/)
> 更新时间：2023/11/07 10:55:31

# 设备信息

头文件<hardware/device_info.h>

## 接口定义

### 获取设备信息

```ts
int BDevice_getInfo(BDevice_DeviceInfo* info);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| info | BDevice_DeviceInfo* | 设备信息（详见 《结构体 设备信息》） |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

### 获取设备唯一标识

```ts
int BDevice_getDeviceId(char** device_id);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| device_id | char** | 设备唯一标识 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

#### 权限

需要申请 DEVICE_INFO 权限。

### 获取用户唯一标识

```ts
int BDevice_getUserId(char** user_id);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| user_id | char** | 用户唯一标识 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

#### 权限

需要申请 DEVICE_INFO 权限。

### 获取设备 MAC 地址

```ts
int BDevice_getMac(char** mac);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| mac | char** | 设备 mac 地址 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

#### 权限

需要申请 DEVICE_INFO 权限。

### 获取设备广告标识

```ts
int BDevice_getAdvertisingId(char** advertising_id);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| advertising_id | char** | 设备广告标识 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

#### 权限

需要申请 DEVICE_INFO 权限。

### 获取设备序列号

```ts
int BDevice_getSerial(char** serial_id);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| serial_id | char** | 设备序列号 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

#### 权限

需要申请 DEVICE_INFO 权限。

### 获取设备存储空间总大小

```ts
int BDevice_getTotalStorage(int* total_storage);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| total_storage | int* | 设备存储空间总大小 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

### 获取设备存储空间可用大小

```ts
int BDevice_getAvailableStorage(int* available_storage);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| available_storage | int* | 设备存储空间可用大小 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

### 获取设备卡识别码

```ts
int BDevice_getDeviceICCID(char** device_iccid);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| device_iccid | char** | 设备卡识别码 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

### 获取设备 CPU 信息

```ts
int BDevice_getCpuInfo(char** cpu_info);
```

#### 参数

| 参数(输出) | 类型 | 说明 |
| --- | --- | --- |
| cpu_info | char** | 设备 CPU 信息 |

#### 返回值

| 返回值 | 类型 | 说明 |
| --- | --- | --- |
| result | int | 结果代码（详见 《枚举 操作结果代码》） |

## 枚举

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| BDEVICE_OK | 0 | 操作成功 |
| BDEVICE_ERROR | -1 | 操作失败 |

## 结构体

### 设备信息 BDevice_DeviceInfo

```ts
typedef struct BDevice_DeviceInfo {
  char* brand;
  char* manufacturer;
  char* model;
  char* product;
  char* os_type;
  char* os_version_name;
  int os_version_code;
  char* platform_version_name;
  int platform_version_code;
  char* language;
  char* device_name;
  char* hardware_version;
  char* software_version;
  char* region;
  int screen_width;
  int screen_height;
  int window_width;
  int window_height;
  int status_bar_height;
  int screen_density;
  char* vendor_os_name;
  char* vendor_os_version;
  char* device_type;
  int screen_refresh_rate;
} BDevice_DeviceInfo;
```

#### 内容说明

| 内容 | 类型 | 说明 |
| --- | --- | --- |
| brand | char* | 设备品牌 |
| manufacturer | char* | 设备生产商 |
| model | char* | 设备型号 |
| product | char* | 设备代号 |
| os_type | char* | 操作系统名称 |
| os_version_name | char* | 操作系统版本名称 |
| os_version_code | int | 操作系统版本号 |
| platform_version_name | char* | 运行平台版本名称 |
| platform_version_code | int | 运行平台版本号 |
| language | char* | 系统语言 |
| device_name | char* | 设备名称 |
| hardware_version | char* | 硬件版本 |
| software_version | char* | 软件版本 |
| region | char* | 系统地区 |
| screen_width | int | 屏幕宽度 |
| screen_height | int | 屏幕高度 |
| window_width | int | 可使用窗口宽度 |
| window_height | int | 可使用窗口高度 |
| status_bar_height | int | 状态栏高度 |
| screen_density | int | 设备的屏幕密度 |
| vendor_os_name | char* | 手表系统的名称，如 BlueOS |
| vendor_os_version | char* | 手表系统的版本号 |
| device_type | char* | 当前 vivo 手表引擎的设备类型，手表版为'watch' |
| screen_refresh_rate | int | 获取屏幕显示刷新率(获取帧率可能不为 60, 90, 144 等标准帧率) |
