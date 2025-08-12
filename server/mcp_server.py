# 全局导入
import json
import os
from hashlib import md5
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import sys

load_dotenv()

mcp = FastMCP("海关大数据", instructions="海关大数据", dependencies=["python-dotenv", "requests"])

INTEGRATOR_ID = os.environ.get("INTEGRATOR_ID")
SECRET_ID = os.environ.get("SECRET_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")

def call_api(product_id: str, params: dict) -> dict:
    """
    调用API接口
    
    参数:
      - product_id: 数据产品ID
      - params: 接口参数
    
    返回:
      - 接口返回的JSON数据
    """
    if not params:
        params = {}
    
    if not INTEGRATOR_ID:
        return {"error": "对接器ID不能为空"}
    
    if not SECRET_ID:
        return {"error": "密钥ID不能为空"}
    
    if not SECRET_KEY:
        return {"error": "密钥不能为空"}
    
    if not product_id:
        return {"error": "产品ID不能为空"}
    
    call_params = {
        "product_id": product_id,
        "secret_id": SECRET_ID,
        "params": json.dumps(params, ensure_ascii=False)
    }
    
    # 生成签名
    keys = sorted(list(call_params.keys()))
    params_str = ""
    for key in keys:
        params_str += str(call_params[key])
    params_str += SECRET_KEY
    sign = md5(params_str.encode("utf-8")).hexdigest()
    call_params["signature"] = sign
    
    # 调用API
    url = f'https://console.handaas.com/api/v1/integrator/call_api/{INTEGRATOR_ID}'
    try:
        response = requests.post(url, data=call_params)
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("data", None) or response_json.get("msgCN", None) or response_json
        else:
            return f"接口调用失败，状态码：{response.status_code}"
    except Exception as e:
        return "查询失败"
    
@mcp.tool()
def customs_bigdata_export_trends(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口的功能是根据企业的身份标识信息（如企业名称、注册号、统一社会信用代码等）查询该企业的外贸出口趋势，包括每年的出口金额和订单数量等数据。此接口适用于分析企业在国际市场中的表现，帮助企业管理者或研究人员了解企业的出口能力以及市场份额的变化趋势。具体场景包括企业在进行市场分析时需要了解自身或竞争对手在外贸方面的增长潜力、银行或投资机构在金融评估时用于判断企业的国际贸易风险和收益、以及政府或行业协会在统计和研究企业整体外贸出口趋势时使用。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码)

    返回参数:
    - exportTrend: 出口年份列表 类型：list of dict
        - amount: 金额 类型：float - 美元
        - count: 订单数量 类型：int
        - year: 年份 类型：string
    - total: 出口年份总数 类型：int
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66aa4eac4bb1f40b86c46eab', params)


@mcp.tool()
def customs_bigdata_export_product_trends(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口用于查询并分析企业外贸商品的发展趋势，提供企业在不同年份的出口商品订单量及海关HS编码分布信息。其功能包括通过输入企业的基本标识信息（如企业名称、注册号等），输出该企业历年出口商品的订单量变化情况及具体商品类别。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - exportGoodsOrderDistribution: 出口商品订单量分布 类型：list of dict
        - count: 数量 类型：int
        - hsCode: 海关HS商品编码 类型：string
        - orderCountOfYear: 每年的订单量 类型：list of dict
            - count: 数量 类型：int
            - hsCode: 海关HS商品编码 类型：string
            - year: 年份 类型：int
    - exportGoodsOrderTrend: 出口商品订单量趋势 类型：list of dict
        - year: 年份 类型：int
        - count: 数量 类型：int
        - name: 名称 类型：string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66c9a953268e9d7292c1a919', params)


@mcp.tool()
def customs_bigdata_export_recruitment_profile(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口的功能是根据输入的企业标识信息（如企业名称或统一社会信用代码）和主体类型枚举，获取企业在过去三个月内的外贸相关岗位的招聘情况。输出信息包括招聘岗位数量、招聘城市及数量、招聘渠道和外贸相关的招聘渠道名称等。此接口可能在以下场景中使用：企业想要了解竞争对手的外贸招聘动态，以帮助其优化招聘策略；政府机构分析某地区外贸企业的用工需求变化；招聘平台分析外贸行业的岗位需求趋势，以促进精准服务。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - recruitingLatestThreeMonthCount: 近三个月招聘岗位数 类型：int
    - recruitingCityCount: 招聘城市数量 类型：int
    - recruitingCityList: 招聘城市 类型：list of string
    - recruitingCount: 招聘岗位数 类型：int
    - recruitingPositions: 招聘岗位名称 类型：list of string
    - recruitingPlatforms: 外贸相关岗位平台 类型：list of string
    - recruitingSourceCount: 招聘渠道数量 类型：int
    - recruitingSourceList: 招聘渠道 类型：list of string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66d5b7e0537c3f61d646c346', params)


@mcp.tool()
def customs_bigdata_export_order_regions(matchKeyword: str, pageIndex: int = 1, pageSize: int = 10,
                         keywordType: str = None) -> dict:
    """
    该接口的功能是根据提供的企业标识信息（如企业名称、注册号等）查询该企业外贸订单的地理分布情况，输出包括订单地区列表、订单金额、订单数量、涉及的国家或地区、净重，以及分布地区的总数。此接口可用于企业管理系统中，帮助企业分析其国际市场的分布状况，评估各地区的订单贡献度，从而制定更加有效的市场拓展策略。


    请求参数:
    - pageIndex: 页码 类型：int - 默认从1开始
    - pageSize: 分页大小 类型：int - 一页最多获取50条
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码)
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。

    返回参数:
    - resultList: 订单地区分布列表 类型：list of dict
        - amount: 金额 类型：float - 美元
        - count: 订单数 类型：int
        - destCountry: 国家/地区 类型：string
        - weight: 净重 类型：float - 千克
    - total: 分布地区总数 类型：int
    """
    # 构建请求参数
    params = {
        'pageIndex': pageIndex,
        'pageSize': pageSize,
        'keywordType': keywordType,
        'matchKeyword': matchKeyword,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66aa4eac4bb1f40b86c46ea0', params)


@mcp.tool()
def customs_bigdata_overseas_certifications(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口的功能是根据企业的名称、注册编号、统一社会信用代码或企业ID查询企业的海外认证信息，包括认证类别、证书编号及相关产品信息。该接口可用于企业在寻求国际贸易机会时评估潜在合作伙伴的资质，帮助中介公司或行业分析者收集市场数据，或者企业在申请招投标过程中提交其资质证明文档。通过提供认证信息，还可方便监管机构和行业组织核实企业的合规性和认证情况。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - certList: 结果列表 类型：list of dict
        - certType: 认证类别 类型：string
        - certId: 证书号 类型：string
        - certDomain: 认证领域 类型：string
        - certProductName: 产品名称 类型：string
    - certCount: 总数 类型：int
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66c9a953268e9d7292c1a96e', params)


@mcp.tool()
def customs_bigdata_fuzzy_search(matchKeyword: str, pageIndex: int = 1, pageSize: int = 50) -> dict:
    """
    该接口的功能是根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。返回匹配的企业列表及其详细信息，用于查找和识别特定的企业信息。

    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 查询各类信息包含匹配关键词的企业
    - pageIndex: 分页开始位置 类型：int - 默认从1开始
    - pageSize: 分页结束位置 类型：int - 一页最多获取50条数据, 不能超过50, 超过50的统一用50代替

    返回参数:
    - total: 总数 类型：int
    - resultList:查询返回企业信息列表 类型：list of dict:
        - annualTurnover: 年营业额 类型：string
        - formerNames: 曾用名 类型：list of string
        - address: 注册地址 类型：string
        - foundTime: 成立时间 类型：string
        - enterpriseType: 企业主体类型 类型：string
        - legalRepresentative: 法定代表人 类型：string
        - legalRepresentativeId: 法定代表人id 类型：string
        - homepage: 企业官网 类型：string
        - prmtKeys: 推广关键词 类型：list of string
        - operStatus: 企业状态 类型：string
        - logo: 企业logo 类型：string
        - nameId: 企业id 类型：string
        - regCapitalCoinType: 注册资本币种 类型：string
        - regCapitalValue: 注册资本金额 类型：int
        - name: 企业名称 类型：string
        - catchReason: 命中原因 类型：dict
            - catchReason.name: 企业名称 类型：list of string
            - catchReason.formerNames: 曾用名 类型：list of string
            - catchReason.holderList: 股东 类型：list of string
            - catchReason.recruitingName: 招聘岗位 类型：list of string
            - catchReason.address: 地址 类型：list of string
            - catchReason.operBrandList: 品牌 类型：list of string
            - catchReason.goodsNameList: 产品名称 类型：list of string
            - catchReason.phoneList: 固话 类型：list of string
            - catchReason.emailList: 邮箱 类型：list of string
            - catchReason.mobileList: 手机 类型：list of string
            - catchReason.patentNameList: 专利 类型：list of string
            - catchReason.certNameList: 资质证书 类型：list of string
            - catchReason.prmtKeys: 推广关键词 类型：list of string
            - catchReason.socialCreditCode: 统一社会信用代码 类型：list of string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'pageIndex': pageIndex,
        'pageSize': pageSize,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('675cea1f0e009a9ea37edaa1', params)


if __name__ == "__main__":
    print("正在启动MCP服务...")
    # 解析第一个参数
    if len(sys.argv) > 1:
        start_type = sys.argv[1]
    else:
        start_type = "stdio"

    print(f"启动方式: {start_type}")
    if start_type == "stdio":
        print("正在使用stdio方式启动MCP服务器...")
        mcp.run(transport="stdio")
    if start_type == "sse":
        print("正在使用sse方式启动MCP服务器...")
        mcp.run(transport="sse")
    elif start_type == "streamable-http":
        print("正在使用streamable-http方式启动MCP服务器...")
        mcp.run(transport="streamable-http")
    else:
        print("请输入正确的启动方式: stdio 或 sse 或 streamable-http")
        exit(1)
    