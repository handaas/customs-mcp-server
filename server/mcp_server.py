# 全局导入
import json
import os
from hashlib import md5
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import sys

load_dotenv()

mcp = FastMCP("标讯大数据", instructions="标讯大数据",dependencies=["python-dotenv", "requests"])

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
        return response.json().get("data", "查询为空")
    except Exception as e:
        return "查询失败"
    
@mcp.tool()
def bid_bigdata_bid_win_stats(matchKeyword: str, keywordType: str = None) -> dict:
    """
    根据企业名称、统一社会信用代码等获取企业标讯信息中中标信息统计项，包括标的分布、金额分布、区域分布及中标趋势等。如果没有企业全称则先调取fuzzy_search接口获取企业全称。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - winbidAmountStatList: 中标金额分布 类型：list of dict
    - range: 金额范围 类型：string
    - percent: 比例 类型：float
    - count: 数量 类型：int
    - winbidAreaStat: 区域分布 类型：list of dict
    - area: 区域 类型：int
    - winbidStatList: 中标标的分布 类型：list of dict
    - count: 数量 类型：int
    - winbidTrend: 中标趋势 类型：list of dict
    - percent: 比例 类型：float
    - subjectMatter: 标的物 类型：string
    - count: 数量 类型：int
    - count: 数量 类型：int
    - year: 年份 类型：int
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('6707813f7427e966078e391d', params)


@mcp.tool()
def bid_bigdata_bidding_info(matchKeyword: str, pageSize: int = None, keywordType: str = None, pageIndex: int = None) -> dict:
    """
    该接口的功能是根据输入的企业标识符（企业名称、注册号、统一社会信用代码或企业id）和主体类型，查询并返回该企业参与的招投标信息，包括招投标公告类型、项目地区、公告详情及与之相关的企业信息。此接口的用途主要是在招投标信息管理系统中，帮助用户获取特定企业的招投标参与记录和项目详情，可用于企业信用审查、合作伙伴评估、市场竞争分析等场景。如果没有企业全称则先调取fuzzy_search接口获取企业全称。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id
    - pageSize: 分页大小 类型：int - 一页最多获取50条数据
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）
    - pageIndex: 页码 类型：int - 从1开始

    返回参数:
    - total: 总数 类型：int
    - resultList: 结果列表 类型：list of dict
    - biddingId: 招投标Id 类型：string
    - infoType: 招投标公告类型 类型：string
    - projectRegion: 项目地区 类型：dict
    - publishDate: 公告发布时间 类型：int
    - subjectMatterList: 标的物 类型：list of string
    - title: 公告标题 类型：string
    - role: 招投标角色 类型：string - 招标，中标
    - projectAmount: 项目金额 类型：string
    - winningBidderList: 中标企业 类型：list of dict
    - name: 企业名称 类型：string
    - nameId: 企业ID 类型：string
    - purchasingBidderList: 招标企业 类型：list of dict
    - name: 企业名称 类型：string
    - nameId: 企业ID 类型：string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'pageSize': pageSize,
        'keywordType': keywordType,
        'pageIndex': pageIndex,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66bf124bf134a4c21b4fc2fa', params)


@mcp.tool()
def bid_bigdata_tender_stats(matchKeyword: str, keywordType: str = None) -> dict:
    """
    根据企业名称、统一社会信用代码等获取企业标讯信息中招标信息统计项，包括标的分布、金额分布、区域分布及招标趋势等。如果没有企业全称则先调取fuzzy_search接口获取企业全称。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - tenderAmountStatList: 招标金额分布 类型：list of dict
    - tenderAreaStat: 区域分布 类型：list of dict
    - count: 数量 类型：int
    - area: 区域 类型：int
    - count: 数量 类型：int
    - tenderStatList: 招标标的分布 类型：list of dict
    - count: 数量 类型：int
    - percent: 比例 类型：float
    - range: 金额范围 类型：string
    - percent: 比例 类型：float
    - tenderTrend: 招标趋势 类型：list of dict
    - count: 数量 类型：int
    - year: 年份 类型：int
    - subjectMatter: 标的物 类型：string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('6707813f7427e966078e392f', params)


@mcp.tool()
def bid_bigdata_procurement_stats(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口可以根据企业名称或ID，获取企业采购统计信息，包括采购产品分布、采购区域分布、采购数量、地区、占比、产品名称、客户数等，可以应用于市场分析、供应链优化、采购决策等领域，帮助企业了解采购趋势和市场分布。如果没有企业全称则先调取fuzzy_search接口获取企业全称。

    请求参数:
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id

    返回参数:
    - purchasingProductStatList: 采购产品分布 类型：list of dict
    - count: 采购数量 类型：int
    - percent: 占比 类型：float
    - product: 产品名称 类型：string
    - purchasingAreaStatList: 采购区域分布 类型：list of dict
    - times: 客户数 类型：int
    - area: 地区 类型：string
    """
    # 构建请求参数
    params = {
        'keywordType': keywordType,
        'matchKeyword': matchKeyword,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('6725e5b9ba65854594baebbc', params)


@mcp.tool()
def bid_bigdata_fuzzy_search(matchKeyword: str, pageIndex: int = None, pageSize: int = None) -> dict:
    """
    该接口的功能是根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。返回匹配的企业列表及其详细信息，用于查找和识别特定的企业信息。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 查询各类信息包含匹配关键词的企业
    - pageIndex: 分页开始位置 类型：int
    - pageSize: 分页结束位置 类型：int - 一页最多获取50条数据

    返回参数:
    - total: 总数 类型：int
    - resultList: 结果列表 类型：list of dict
    - annualTurnover: 年营业额 类型：string
    - formerNames: 曾用名 类型：list of string
    - catchReason: 命中原因 类型：dict
    - address: 注册地址 类型：string
    - holderList: 股东 类型：list of string
    - address: 地址 类型：list of string
    - name: 企业名称 类型：list of string
    - goodsNameList: 产品名称 类型：list of string
    - operBrandList: 品牌 类型：list of string
    - mobileList: 手机 类型：list of string
    - phoneList: 固话 类型：list of string
    - recruitingName: 招聘岗位 类型：list of string
    - emailList: 邮箱 类型：list of string
    - patentNameList: 专利 类型：list of string
    - certNameList: 资质证书 类型：list of string
    - socialCreditCode: 统一社会信用代码 类型：list of string
    - foundTime: 成立时间 类型：string
    - enterpriseType: 企业主体类型 类型：string
    - legalRepresentative: 法定代表人 类型：string
    - homepage: 企业官网 类型：string
    - legalRepresentativeId: 法定代表人id 类型：string
    - prmtKeys: 推广关键词 类型：list of string
    - operStatus: 企业状态 类型：string
    - logo: 企业logo 类型：string
    - nameId: 企业id 类型：string
    - regCapitalCoinType: 注册资本币种 类型：string
    - regCapitalValue: 注册资本金额 类型：int
    - name: 企业名称 类型：string
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


@mcp.tool()
def bid_bigdata_bid_search(matchKeyword: str = None, biddingType: str = None, biddingRegion: str = None,
               biddingAnncPubStartTime: str = None, biddingAnncPubEndTime: str = None, searchMode: str = None,
               biddingProjectMaxAmount: float = None, biddingPurchasingType: str = None,
               biddingProjectMinAmount: float = None, pageIndex: int = None, pageSize: int = None) -> dict:
    """
    该接口用于查询和筛选招投标信息，通过提供多种过滤条件如招标类型、招标单位类型、地理位置、项目金额范围等，返回符合条件的招投标公告详细信息，常用于政府、企业采购部门或相关单位进行招投标管理和分析。用户可以实时了解最新的招投标动态，以便决策和业务拓展。场景包括政府采购人员查询合适的招标项目，企业查找投标机会，以及分析招投标市场趋势等。


    请求参数:
    - matchKeyword: 搜索关键词 类型：string - 默认按最新发布时间返回全部
    - biddingType: 信息类型 类型：string - 招标类型枚举（招标预告，招标公告，变更补充，中标公告，采购意向，废标终止），可多选，输入格式举例：["招标预告","招标公告","采购意向"]
    - biddingRegion: 项目地区 类型：string - 多选，支持省份，城市，输入格式举例：[["福建省","厦门市"],["贵州省","安顺市"]]
    - biddingAnncPubStartTime: 发布开始日期 类型：string - 招投标公告发布开始时间，格式：“2024-08-01”
    - biddingAnncPubEndTime: 发布结束日期 类型：string - 招投标公告发布结束时间，格式：“2024-11-01”
    - searchMode: 搜索模式 类型：select - 搜索模式枚举（标题匹配，标的物匹配，全文匹配）
    - biddingProjectMaxAmount: 项目金额最大值 类型：float - 项目金额最大值，单位：万
    - biddingPurchasingType: 招标单位类型 类型：string - 招标单位类型枚举（政府，学校，医院，公安，部队，企业），可输入多个用英文逗号分隔，输入格式举例：“政府,学校”
    - biddingProjectMinAmount: 项目金额最小值 类型：float - 项目金额最小值，单位：万
    - pageIndex: 分页索引 类型：int
    - pageSize: 分页大小 类型：int - 一页最多获取50条

    返回参数:
    - biddingAnncTitle: 公告标题 类型：string
    - biddingContent: 正文 类型：string
    - resultList: 结果列表 类型：list of dict
    - total: 总数 类型：int
    - biddingId: 公告id 类型：string
    - biddingInfoType: 公告类型 类型：string
    - biddingProjectType: 项目类型 类型：string
    - biddingPublishTime: 公告时间 类型：string
    - biddingEndTime: 招标截止时间 类型：string
    - biddingProjectID: 项目编号 类型：string
    - biddingAgentInfoList: 招标代理机构信息列表 类型：list of dict
    - biddingPurchasingInfoList: 招标单位相关信息列表 类型：list of dict
    - biddingWinningInfoList: 中标单位相关信息列表 类型：list of dict
    - biddingRegion: 招投标所属地区 类型：string
    - hasFile: 有无附件 类型：int
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'biddingType': biddingType,
        'biddingRegion': biddingRegion,
        'biddingAnncPubStartTime': biddingAnncPubStartTime,
        'biddingAnncPubEndTime': biddingAnncPubEndTime,
        'searchMode': searchMode,
        'biddingProjectMaxAmount': biddingProjectMaxAmount,
        'biddingPurchasingType': biddingPurchasingType,
        'biddingProjectMinAmount': biddingProjectMinAmount,
        'pageIndex': pageIndex,
        'pageSize': pageSize,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66bf124bf134a4c21b4fc34c', params)


@mcp.tool()
def bid_bigdata_planned_projects(matchKeyword: str, pageIndex: int = None, pageSize: int = None, keywordType: str = None) -> dict:
    """
    该接口用于查询企业拟建公告的信息，提供了通过企业名称、注册号、社会信用代码或企业ID等多种方式检索拟建项目的相关详情。典型使用场景包括政府部门或行业协会在监管和分析企业拟建项目情况时，通过该接口获取企业的拟建公告及详细信息，以便进行统计分析、市场研究和行业动向监控，支持决策制定和政策出台。通过这一接口，用户可以高效地访问到关于某个企业在建或拟建项目的时效性和区域性信息，有助于提升信息获取的便利性和准确性。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id
    - pageIndex: 页码 类型：int - 从1开始
    - pageSize: 分页大小 类型：int - 一页最多获取50条数据
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码）

    返回参数:
    - total: 总数 类型：int
    - ppId: 项目id 类型：string
    - resultList: 结果列表 类型：list of dict
    - deviceList: 待采设备 类型：list of string
    - ppRegion: 建设地点 类型：dict
    - ppTitle: 项目名称 类型：string
    - ppContent: 项目内容 类型：string
    - ppPublishTime: 发布时间 类型：string
    - ppApprovalTime: 评审时间 类型：string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'pageIndex': pageIndex,
        'pageSize': pageSize,
        'keywordType': keywordType,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66f3d8c064bd2be52d68a134', params)


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
    