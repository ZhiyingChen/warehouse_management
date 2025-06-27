import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import patches
import pandas as pd
from web import function

# 设置页面标题和图标
st.set_page_config(page_title="纸卷切割优化问题背景", page_icon="📘")

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        max-width: 1000px;
        padding: 2rem;
    }
    .stMarkdown h2 {
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.3rem;
    }
    .stMarkdown h3 {
        color: #3d5a80;
    }
    .stDataFrame {
        font-size: 0.9rem;
    }
    .stImage {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 标题部分
st.title("📘 仓储管理问题背景")
st.markdown("---")

# 页面布局
st.subheader("📋 问题描述")
st.markdown("""
    给定：
    - 一组客户城市及其需求；
    - 一组候选仓储城市（即潜在的建仓选址）；
    - 城市对之间的距离及运输时间；
    - 各类相关成本（运输、库存、资金占用、缺货惩罚）；
    
    目标是在满足客户需求、满足运输时效前提下，决定：
    - 在哪些候选仓储城市设立仓库；
    - 每个仓库配置多少库存；
    - 每个客户的需求由哪个仓库供应，以及供应量是多少；
    并使得系统的总成本最小。
    
    约束包括：
    - 未建仓库城市不能存货；
    - 总库存需控制在上下限之间；
    - 每个仓库出货量不能超过库存；
    - 每个客户的收货量不能超过其需求；
    - 仓库总数需满足数量约束（最小/最大建仓数）；
    - 仓库间运输需满足时效上限。
""")

# 页脚

function.render_footer()