import os

import streamlit as st
import streamlit.components.v1 as components

from pathlib import Path

# Set page config
st.set_page_config(page_title="Review Platform", page_icon=":handshake:", layout='wide')

current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"


with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = False

if not _RELEASE:
    _custom_header = components.declare_component(
        "custom_header",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_header = components.declare_component("custom_header", path=build_dir)


def custom_header():
    return _custom_header()

# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_header/__init__.py`
if not _RELEASE:
    custom_header()
