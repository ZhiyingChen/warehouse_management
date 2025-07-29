import streamlit as st
from web import function


# 渲染语言栏
function.render_language_selector()

# 获取语言字典
lang, T = function.get_language_dict("doc")
# 页面内容
st.title(T["title"])
st.header(T["background_header"])
st.markdown(T["background_markdown"])
