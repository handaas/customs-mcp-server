# 招投标大数据服务

[该MCP服务提供全面的进出口贸易数据查询功能，包括出口趋势分析、商品类别统计、订单地理分布、海外认证信息等，帮助用户了解企业的国际贸易情况。](https://www.handaas.com/)

## 主要功能

- 🔍 企业关键词模糊搜索
- 📈 出口趋势分析
- 📦 出口商品分析
- 🌍 订单地理分布
- 👥 外贸招聘分析
- 📋 海外认证查询

## 环境要求

- Python 3.10+
- 依赖包：python-dotenv, requests, mcp

## 本地快速启动

### 1. 克隆项目
```bash
git clone https://github.com/handaas/customs-mcp-server
cd customs-mcp-server
```

### 2. 创建虚拟环境&安装依赖

```bash
python -m venv mcp_env && source mcp_env/bin/activate
pip install -r requirements.txt
```

### 3. 环境配置

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下环境变量：

```env
INTEGRATOR_ID=your_integrator_id
SECRET_ID=your_secret_id
SECRET_KEY=your_secret_key
```

### 4. streamable-http启动服务

```bash
python server/mcp_server.py streamable-http
```

服务将在 `http://localhost:8000` 启动。

#### 支持启动方式 stdio 或 sse 或 streamable-http

### 5. Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "handaas-mcp-server": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

## STDIO版安装部署

### 设置Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "customs-mcp-server": {
      "command": "uv",
      "args": ["run", "mcp", "run", "{workdir}/server/mcp_server.py"],
      "env": {
        "PATH": "{workdir}/mcp_env/bin:$PATH",
        "PYTHONPATH": "{workdir}/mcp_env",
        "INTEGRATOR_ID": "your_integrator_id",
        "SECRET_ID": "your_secret_id",
        "SECRET_KEY": "your_secret_key"
      }
    }
  }
}
```

## 使用官方Remote服务

### 1. 直接设置Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "customs-mcp-server":{
      "type": "streamableHttp",
      "url": "https://mcp.handaas.com/customs/customs_bigdata?token={token}"  
      }
  }
}
```

### 注意：integrator_id、secret_id、secret_key及token需要登录 https://www.handaas.com/ 进行注册开通平台获取


## 可用工具

### 1. customs_bigdata_fuzzy_search
**功能**: 企业关键词模糊查询

根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。

**参数**:
- `matchKeyword` (必需): 匹配关键词
- `pageIndex` (可选): 分页开始位置
- `pageSize` (可选): 分页结束位置

**返回值**:
- `total`: 总数

### 2. customs_bigdata_export_trends
**功能**: 出口趋势分析

根据企业的身份标识信息查询该企业的外贸出口趋势，包括每年的出口金额和订单数量等数据。

**参数**:
- `matchKeyword` (必需): 企业名称/注册号/统一社会信用代码/企业id
- `keywordType` (可选): 主体类型枚举

**返回值**:
- `exportTrend`: 出口年份列表
  - `amount`: 金额（美元）
  - `count`: 订单数量
  - `year`: 年份
- `total`: 出口年份总数

### 3. customs_bigdata_export_product_trends
**功能**: 出口商品趋势分析

查询并分析企业外贸商品的发展趋势，提供企业在不同年份的出口商品订单量及海关HS编码分布信息。

**参数**:
- `matchKeyword` (必需): 企业名称/注册号/统一社会信用代码/企业id
- `keywordType` (可选): 主体类型枚举

**返回值**:
- `exportGoodsOrderDistribution`: 出口商品订单量分布
  - `orderCountOfYear`: 每年的订单量
  - `count`: 数量
  - `hsCode`: 海关HS商品编码
  - `year`: 年份
- `exportGoodsOrderTrend`: 出口商品订单量趋势
  - `year`: 年份
  - `count`: 数量
  - `name`: 名称

### 4. customs_bigdata_export_recruitment_profile
**功能**: 外贸招聘分析

根据输入的企业标识信息，获取企业在过去三个月内的外贸相关岗位的招聘情况。

**参数**:
- `matchKeyword` (必需): 企业名称/注册号/统一社会信用代码/企业id
- `keywordType` (可选): 主体类型枚举

**返回值**:
- `recruitingLatestThreeMonthCount`: 近三个月招聘岗位数
- `recruitingCityCount`: 招聘城市数量
- `recruitingCityList`: 招聘城市
- `recruitingCount`: 招聘岗位数
- `recruitingPositions`: 招聘岗位名称
- `recruitingPlatforms`: 外贸相关岗位平台
- `recruitingSourceCount`: 招聘渠道数量
- `recruitingSourceList`: 招聘渠道

### 5. customs_bigdata_export_order_regions
**功能**: 出口订单地理分布

根据提供的企业标识信息查询该企业外贸订单的地理分布情况，包括各地区的订单金额、数量等。

**参数**:
- `matchKeyword` (必需): 企业名称/注册号/统一社会信用代码/企业id
- `pageIndex` (可选): 页码 - 从1开始
- `pageSize` (可选): 分页大小 - 一页最多获取50条
- `keywordType` (可选): 主体类型枚举

**返回值**:
- `resultList`: 订单地区分布列表
  - `amount`: 金额（美元）
  - `count`: 订单数
  - `destCountry`: 国家/地区
  - `weight`: 净重（千克）
- `total`: 分布地区总数

### 6. customs_bigdata_overseas_certifications
**功能**: 海外认证信息查询

根据企业的名称、注册编号等查询企业的海外认证信息，包括认证类别、证书编号及相关产品信息。

**参数**:
- `matchKeyword` (必需): 企业名称/注册号/统一社会信用代码/企业id
- `keywordType` (可选): 主体类型枚举

**返回值**:
- `certType`: 认证类别
- `certId`: 证书号
- `certCount`: 总数
- `certDomain`: 认证领域
- `certProductName`: 产品名称

## 使用场景

1. **企业国际贸易分析**: 了解企业的出口能力和市场份额变化趋势
2. **竞争对手研究**: 分析竞争对手在国际市场中的表现
3. **金融风险评估**: 银行或投资机构评估企业的国际贸易风险和收益
4. **市场拓展策略**: 制定更加有效的国际市场拓展策略
5. **政府统计研究**: 政府或行业协会统计企业整体外贸出口趋势
6. **招投标资质验证**: 企业在申请招投标过程中提交资质证明

## 使用注意事项

1. **企业全称要求**: 在调用需要企业全称的接口时，如果没有企业全称则先调取customs_bigdata_fuzzy_search接口获取企业全称
2. **分页限制**: 一页最多获取50条数据
3. **金额单位**: 出口金额以美元为单位
4. **重量单位**: 净重以千克为单位
5. **时间范围**: 招聘信息为过去三个月内的数据
6. **HS编码**: 商品分类基于海关HS编码标准

## 使用提问示例

### customs_bigdata_export_trends (出口趋势分析)
3. 华为近年来的出口金额趋势如何？订单数量有什么变化？
4. 比亚迪的外贸出口表现怎么样？
5. 小米的出口业务是增长还是下降趋势？

### customs_bigdata_export_product_trends (出口商品趋势分析)
6. 华为主要出口哪些商品？各类产品的订单量分布如何？
7. 比亚迪的出口商品结构是怎样的？HS编码分布情况如何？
8. 小米不同年份的出口商品类别有什么变化？

### customs_bigdata_export_recruitment_profile (外贸招聘分析)
9. 华为最近三个月有在招聘外贸相关岗位吗？
10. 比亚迪的外贸团队招聘情况如何？在哪些城市招人？
11. 小米的外贸招聘主要通过哪些平台？岗位需求量大吗？

### customs_bigdata_export_order_regions (出口订单地理分布)
12. 华为的出口订单主要分布在哪些国家和地区？
13. 比亚迪的海外市场覆盖情况如何？各地区订单金额如何？
14. 小米的产品主要出口到哪些市场？

### customs_bigdata_overseas_certifications (海外认证查询)
15. 华为获得了哪些海外认证？认证领域主要是什么？
16. 比亚迪有多少个海外产品认证？证书类别有哪些？
17. 小米的产品都通过了哪些国际认证？