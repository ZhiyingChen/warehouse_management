import streamlit as st
import pandas as pd
import time
from web import function
from source.context import Context
from source.info import InputData, Config
from source.info.data_loader import DataLoader
from source.model import ModelManager
from source.result.processor import ResultProcessor
from source.result.dumper import ResultDumper
from source.utils import log

st.title("⚙️ 仓储选址算法")

st.markdown(
    """
    请在“执行算法”页面将示例输入文件改成你需要的数据。
    """
)

# 输入接口文档
st.header("📥 输入接口文档")

with st.expander("📥 输入文件说明：全局参数.csv"):
    df_global_params = pd.DataFrame([
        ["名称", "str", "各类参数的名称"],
        ["单位", "str", "参数单位"],
        ["数量", "double", "参数值"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_global_params)

    st.markdown("**参数枚举说明：**")
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

with st.expander("📥 输入文件说明：需求分布.csv"):
    df_demand = pd.DataFrame([
        ["城市", "str", "需求城市名称"],
        ["需求量", "str", "城市的需求量"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_demand)

with st.expander("📥 输入文件说明：供应城市.csv"):
    df_supply = pd.DataFrame([
        ["城市", "str", "候选建仓城市名称"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_supply)

with st.expander("📥 输入文件说明：距离数据.csv"):
    df_distance = pd.DataFrame([
        ["城市1", "str", "起始城市"],
        ["城市2", "str", "目标城市"],
        ["距离（公里）", "float", "城市1和城市2之间的距离"],
        ["时间（小时）", "float", "城市1和城市2之间的运输时长"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_distance)

# 输出接口文档
st.header("📤 输出接口文档")

with st.expander("📊 输出文件说明：指标输出.csv"):
    df_kpi = pd.DataFrame([
        ["指标名称", "str", "各类 KPI 指标的名称"],
        ["指标值", "double", "KPI 的数值"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_kpi)

    st.markdown("**常见指标说明：**")
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

with st.expander("📊 输出文件说明：构建仓库的城市输出.csv"):
    df_warehouse = pd.DataFrame([
        ["城市", "str", "建仓城市名称"],
        ["库存水平", "double", "仓库的库存数量"],
        ["供给率", "float", "仓库供给出去的比例（出货量 / 库存）"],
        ["城市X", "str", "向需求城市 X 供货的数量（每列代表一个需求城市）"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_warehouse)

with st.expander("📊 输出文件说明：需求城市满足情况输出.csv"):
    df_fulfill = pd.DataFrame([
        ["城市", "str", "需求城市名称"],
        ["需求量", "float", "城市的需求值"],
        ["满足率", "float", "实际满足的比例（供货量 / 需求量）"],
        ["城市X", "str", "来自建仓城市 X 的供给数量（每列代表一个建仓城市）"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_fulfill)

# 示例数据展示
st.header("📄 示例输入数据（可编辑）")


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


# 加载示例数据
global_df = load_csv("data/全局参数.csv")
demand_df = load_csv("data/需求分布.csv")
supply_df = load_csv("data/供应城市.csv")
distance_df = load_csv("data/距离数据.csv")

# 可编辑的 DataFrame
with st.expander("📝 编辑全局参数"):
    edited_global_df = st.data_editor(global_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label="📥 下载编辑后的 全局参数.csv",
        data=edited_global_df.to_csv(index=False).encode('utf-8'),
        file_name="全局参数.csv",
        mime="text/csv"
    )

with st.expander("📝 编辑需求数据"):
    edited_demand_df = st.data_editor(demand_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label="📥 下载编辑后的 需求分布.csv",
        data=edited_demand_df.to_csv(index=False).encode('utf-8'),
        file_name="需求分布.csv",
        mime="text/csv"
    )

with st.expander("📝 编辑供应城市"):
    edited_supply_df = st.data_editor(supply_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label="📥 下载编辑后的 供应城市.csv",
        data=edited_supply_df.to_csv(index=False).encode('utf-8'),
        file_name="供应城市.csv",
        mime="text/csv"
    )

with st.expander("📝 编辑距离数据"):
    edited_distance_df = st.data_editor(distance_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label="📥 下载编辑后的 距离数据.csv",
        data=edited_distance_df.to_csv(index=False).encode('utf-8'),
        file_name="距离数据.csv",
        mime="text/csv"
    )

# 显示运行按钮
if st.button("🚀 运行算法"):
    with st.spinner("算法运行中，请稍候..."):
        config = Config(
            load_from_file=False
        )
        context = Context()
        context.config = config
        # logger = log.setup_log(config.output_folder)
        st_time = time.time()
        try:

            data_loader = DataLoader(
                param_file_dict={
                    "全局参数.csv": edited_global_df,
                    "需求分布.csv": edited_demand_df,
                    "供应城市.csv": edited_supply_df,
                    "距离数据.csv": edited_distance_df
                }
            )
            data_loader.generate_data(context=context)

            model_manager = ModelManager()
            model_manager.create_constraints(context=context)
            model_manager.solve_all_objectives(context=context)
            sol_dict = model_manager.get_solution()

            result_processor = ResultProcessor(sol_dict=sol_dict)
            result_processor.generate_results(context=context)

            result_dumper = ResultDumper()
            result_file_dict = result_dumper.generate_all_files(context=context)

            st.success(
                "✅ 算法运行完成！共{}秒。".format(round(time.time() - st_time))
            )

        except Exception as e:
            st.error(f"❌ 算法运行出错：{e}")

    st.markdown("---")
    st.header("📊 输出结果")

    # 展示输出文件
    for filename, df in result_file_dict.items():
        with st.expander("📄 {}".format(filename)):
            st.dataframe(df)

# 页脚

function.render_footer()
