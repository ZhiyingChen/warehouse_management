import streamlit as st
from web import function
from web.language_dict import APP_LANG as LANG


if __name__ == '__main__':
    st.set_page_config(
        page_title="仓储选址算法平台",
        page_icon="📦",
        layout="wide"
    )

    function.render_language_selector()
    lang, T = function.get_language_dict("app")

    st.title(T["title"])
    st.markdown(T["welcome"])
    st.markdown(T["navigation"])


    function.render_footer()
