import re
import pandas as pd


p = r"E:\TMS\发票_临时转换_20250430.xlsx"
df = pd.read_excel(p)
df["价税合计"] = pd.to_numeric(df["价税合计"], errors="coerce")
sdate = df["单据日期"].astype(str).str.extract(r"(\d{4})年(\d{1,2})月(\d{1,2})日")
df["年度"] = pd.to_numeric(sdate[0], errors="coerce")


def cls(x):
    s = "" if pd.isna(x) else str(x)
    if "包头兵工新世纪宾馆有限公司" in s:
        return "其他"
    nonrail = r"铁路配件|铁路宾馆|火车站.*酒店|火车站.*宾馆|酒店.*火车|宾馆.*火车|机动车|汽车站|检测|配件|物流|货运|运输专线|置业|经贸|如家|锦江之星|维也纳|莫泰|优选酒店|宏丰宾馆"
    rail = r"铁路电子客票|中国铁路.*(车站|车务段|客运段|站$)|铁路.*客运专线|高速铁路(股份|有限)|城际铁路|广深铁路.*车站|大秦铁路.*站|铁路发展控股"
    if re.search(rail, s) and not re.search(nonrail, s):
        return "火车票"
    nonair = r"航空航天大学|航空仪表|航空科技|航空技术|航空器材|航天|大学|学院|研究|仪表|器材|材料|科技|技术|装备|制造|机械|电子|百慕|工业|零部件|发动机|维修|检测"
    if re.search(nonair, s):
        return "其他"
    if re.search(r"机票|机场|空港|航空服务|航空股份有限公司|航空有限公司|航空有限责任公司|航空控股股份有限公司|航空公司", s):
        return "机票"
    if re.search(r"酒店|宾馆|旅馆|住宿|饭店|客栈|民宿|快捷酒店|大酒店|招待所", s):
        return "酒店"
    return "其他"


df["类别"] = df["销方名称"].map(cls)
y2025 = df[df["年度"].eq(2025) & df["价税合计"].notna()].copy()
core = y2025[y2025["类别"].isin(["酒店", "机票", "火车票"])].copy()
summary = core.groupby("类别").agg(次数=("价税合计", "count"), 金额=("价税合计", "sum"))
print("ALL_2025_ROWS", len(y2025))
print("ALL_2025_AMOUNT", float(y2025["价税合计"].sum()))
print(summary.to_string())
print("CORE_ROWS", len(core))
print("CORE_AMOUNT", float(core["价税合计"].sum()))
