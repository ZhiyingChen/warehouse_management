import streamlit as st
import pandas as pd
from web import function
import requests

function.render_language_selector()
lang, T = function.get_language_dict("algo")

st.title(T["title"])
st.markdown(T["intro"])

# 输入接口文档
st.header(T["input_doc"])

with st.expander(T["global_param_doc"]):
    df_global_params = pd.DataFrame([
        ["名称", "str", "各类参数的名称"],
        ["单位", "str", "参数单位"],
        ["数量", "double", "参数值"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_global_params)

    st.markdown("**" + T["param_enum"] + "**")
    df_param_enum = pd.DataFrame([
        ["运输费率", "元/件·公里", "运输单位成本"],
        ["仓储费率", "元/件·年", "仓储每年的单位成本"],
        ["缺货成本", "元/件", "缺货单位成本"],
        ["资金利率", "百分比", "最终生产成本需要乘以的系数"],
        ["生产成本", "元/件", "生产单位成本"],
        ["仓库数量下限", "个", "最小建仓数"],
        ["仓库数量上限", "个", "最大建仓数"],
        ["仓库库存下限", "件", "最小总库存量"],
        ["仓库库存上限", "件", "最大总库存量"],
        ["运输时间上限", "小时", "仓库与客户城市之间运输时间限制"]
    ], columns=["参数名称", "单位", "解释"])
    st.table(df_param_enum)

with st.expander(T["demand_doc"]):
    df_demand = pd.DataFrame([
        ["城市", "str", "需求城市名称"],
        ["需求量", "str", "城市的需求量"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_demand)

with st.expander(T["supply_doc"]):
    df_supply = pd.DataFrame([
        ["城市", "str", "候选建仓城市名称"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_supply)

with st.expander(T["distance_doc"]):
    df_distance = pd.DataFrame([
        ["城市1", "str", "起始城市"],
        ["城市2", "str", "目标城市"],
        ["距离（公里）", "float", "城市1和城市2之间的距离"],
        ["时间（小时）", "float", "城市1和城市2之间的运输时长"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_distance)

# 输出接口文档
st.header(T["output_doc"])

with st.expander(T["kpi_doc"]):
    df_kpi = pd.DataFrame([
        ["指标名称", "str", "各类 KPI 指标的名称"],
        ["指标值", "double", "KPI 的数值"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_kpi)

    st.markdown("**" + T["kpi_enum"] + "**")
    df_kpi_enum = pd.DataFrame([
        ["总需求量", "件", "所有客户城市的总需求"],
        ["需求覆盖率", "%", "实际满足的需求占总需求的比例"],
        ["总成本", "元", "系统总成本（包括运输、仓储、缺货、资金占用）"],
        ["仓储成本", "元", "所有仓库的总仓储费用"],
        ["运输成本", "元", "所有运输路径的总运输费用"],
        ["缺货成本", "元", "未满足需求部分的惩罚成本"],
        ["资金占用成本", "元", "库存资金占用的成本"]
    ], columns=["指标名称", "单位", "解释"])
    st.table(df_kpi_enum)

with st.expander(T["warehouse_doc"]):
    df_warehouse = pd.DataFrame([
        ["城市", "str", "建仓城市名称"],
        ["库存水平", "double", "仓库的库存数量"],
        ["供给率", "float", "仓库供给出去的比例（出货量 / 库存）"],
        ["城市X", "str", "向需求城市 X 供货的数量（每列代表一个需求城市）"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_warehouse)

with st.expander(T["fulfill_doc"]):
    df_fulfill = pd.DataFrame([
        ["城市", "str", "需求城市名称"],
        ["需求量", "float", "城市的需求值"],
        ["满足率", "float", "实际满足的比例（供货量 / 需求量）"],
        ["城市X", "str", "来自建仓城市 X 的供给数量（每列代表一个建仓城市）"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_fulfill)

# 示例数据展示
st.header(T["sample_data"])


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


global_df = load_csv("data/全局参数.csv")
demand_df = load_csv("data/需求分布.csv")
supply_df = load_csv("data/供应城市.csv")
distance_df = load_csv("data/距离数据.csv")

with st.expander(T["edit_global"]):
    edited_global_df = st.data_editor(global_df, num_rows="dynamic")
    st.download_button(
        label=T["download"].format("全局参数.csv"),
        data=edited_global_df.to_csv(index=False).encode('utf-8'),
        file_name="全局参数.csv",
        mime="text/csv"
    )

with st.expander(T["edit_demand"]):
    edited_demand_df = st.data_editor(demand_df, num_rows="dynamic")
    st.download_button(
        label=T["download"].format("需求分布.csv"),
        data=edited_demand_df.to_csv(index=False).encode('utf-8'),
        file_name="需求分布.csv",
        mime="text/csv"
    )

with st.expander(T["edit_supply"]):
    edited_supply_df = st.data_editor(supply_df, num_rows="dynamic")
    st.download_button(
        label=T["download"].format("供应城市.csv"),
        data=edited_supply_df.to_csv(index=False).encode('utf-8'),
        file_name="供应城市.csv",
        mime="text/csv"
    )

with st.expander(T["edit_distance"]):
    edited_distance_df = st.data_editor(distance_df, num_rows="dynamic")
    st.download_button(
        label=T["download"].format("距离数据.csv"),
        data=edited_distance_df.to_csv(index=False).encode('utf-8'),
        file_name="距离数据.csv",
        mime="text/csv"
    )

if st.button("运行算法"):
    with st.spinner("正在运行优化模型..."):
        payload = {
            "files": {
                "全局参数.csv": edited_global_df.to_dict(orient="records"),
                "需求分布.csv": edited_demand_df.to_dict(orient="records"),
                "供应城市.csv": edited_supply_df.to_dict(orient="records"),
                "距离数据.csv": edited_distance_df.to_dict(orient="records")
            }
        }
        res = requests.post("http://127.0.0.1:8000/api/run", json=payload)
        result = res.json()

        if result["success"]:
            st.success(f"优化完成，用时 {result['runtime']} 秒")
            for name, df_data in result["results"].items():
                df = pd.DataFrame(df_data)
                st.subheader(name)
                st.dataframe(df)
        else:
            st.error(f"出错：{result['error']}")


function.render_footer()
