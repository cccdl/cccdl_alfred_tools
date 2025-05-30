# CCCDL Alfred 工具集

一套为Alfred工作流设计的实用工具集合，提高您的日常工作效率。

## 功能概述

本工具集包含以下实用功能：

1. **密码生成器**：快速生成多种类型的随机密码
2. **IP地址转换器**：将IP地址转换为整数格式
3. **AES加密解密工具**：简便的文本加密和解密
4. **时间转换工具**：多种格式的时间/日期相互转换

## 详细功能说明

### 1. 密码生成器

提供两种密码生成模式：

- **简单密码**：由字母和数字组成，适合一般用途
- **复杂密码**：包含字母、数字和特殊字符，满足高安全性要求

使用方法：
- 在Alfred中输入触发关键词，然后输入所需密码长度
- 选择密码类型（简单/复杂）并复制使用

### 2. IP地址转整数

将IPv4地址转换为对应的整数表示，对网络开发和调试非常有用。

使用方法：
- 在Alfred中输入触发关键词，后跟IP地址（如192.168.1.1）
- 结果将显示转换后的整数值，可直接复制使用

### 3. AES加密解密

基于AES算法的加密解密功能，支持文本的安全传输和存储。

加密功能：
- 使用AES-ECB模式加密文本
- 结果以Base64编码输出

解密功能：
- 解密Base64编码的密文
- 还原为原始文本

### 4. 时间转换工具

支持多种格式的时间和日期互相转换，包括：

- **时间戳（秒）**：Unix 时间戳，从1970年1月1日起的秒数
- **时间戳（毫秒）**：毫秒级时间戳
- **中国本地时间 (UTC+8)**：北京时间的日期时间格式
- **中国本地日期 (UTC+8)**：北京时间的日期格式
- **UTC 标准时间**：世界协调时的日期时间格式
- **UTC 标准日期**：世界协调时的日期格式

使用方法：
- 在Alfred中输入触发关键词，后跟任意格式的时间/日期/时间戳
- 选择需要的输出格式并复制使用
- 支持多种输入格式，如"2025-05-08"、"2025/05/08 14:30"、时间戳等

## 系统要求

- macOS 操作系统
- Alfred 4或更高版本（需要Powerpack许可证）
- Python 3.6+
- 相关Python库：pycryptodome（用于AES加密）

## 安装步骤

1. 下载 `dl.alfredworkflow` 文件
2. 双击文件将其导入到Alfred
3. 确保系统中已安装Python 3.x
4. 安装必要的依赖库：
   ```
   pip install pycryptodome
   ```

## 使用指南

### 密码生成器

- 触发关键词：`pw`
- 参数：密码长度（数字）
- 示例：`pw 12`（生成12位密码）

### IP转换器

- 触发关键词：`ip2int`
- 参数：IPv4地址
- 示例：`ip2int 192.168.1.1`

### 加密解密

- 加密触发关键词：`encrypt`
- 解密触发关键词：`decrypt`
- 参数：需要加密或解密的文本

### 时间转换工具

- 触发关键词：`time`
- 参数：任意格式的时间/日期/时间戳
- 示例：
  - `time 2025-05-08` （转换日期）
  - `time 1715105445` （转换时间戳）
  - `time now` （转换当前时间）

## 文件结构

```
dl.alfredworkflow       - Alfred工作流文件
main.py                 - 主入口文件
des/                    - 加密解密功能
├── aes.py              - AES加密实现
└── des.py              - 解密实现
iptoint/                - IP转换功能
└── input.py            - IP转整数实现
password/               - 密码生成功能
├── input.py            - 密码类型选择界面
├── input1.py           - 密码生成实现（简单/复杂密码）
└── password.py         - 通用密码生成器
time_converter/         - 时间转换功能
├── converter.py        - 时间转换实现
└── input.py            - 时间转换输入界面
```

## 自定义配置

您可以在Alfred的偏好设置中修改工作流的关键词和快捷键，以满足个人使用习惯。

## 开发者信息

本工具集由CCCDL开发，旨在提高日常工作效率。

## 更新日志

**v1.1.0** (2025-05-08)
- 添加时间转换功能，支持多种格式的转换

**v1.0.0** (2025-05-08)
- 初始版本发布
- 包含密码生成、IP转换和加密解密功能

## 许可证

MIT License

## 反馈与贡献

如有问题或建议，欢迎通过以下方式联系：
- 提交Issue
- 发送邮件至[您的邮箱]

## 故障排除

### 时间转换功能提示“错误: 转换脚本未收到有效输入”

如果您在使用时间转换功能时（例如输入 `time` 后选择一个选项），最终看到类似“错误: 转换脚本未收到有效输入”或“错误: 没有接收到输入”的提示，这通常意味着 Alfred Workflow 中脚本之间的参数传递配置有误。

**主要检查点：**

1.  打开 Alfred 偏好设置，进入您的 “CCCDL 工具集” Workflow。
2.  找到负责执行时间转换的**第二个 "Run Script" 动作**（它连接在生成选项列表的第一个 "Run Script" 动作之后）。
3.  双击打开这个动作的配置界面。
4.  **确保其 "Argument" 输入框是完全空的。** 如果这里有任何内容（包括空格），都可能导致问题。
5.  确保输入处理方式（通常是 "Handling of {query} input:"）设置为 **"with input as {query}"**。

这个配置确保了当您从第一个脚本生成的列表中选择一个项目时，该项目的 `arg` 值能够正确地作为输入传递给第二个脚本进行处理。