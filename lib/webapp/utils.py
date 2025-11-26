from lib.common import Model
from lib.settings import OUTFILE
import streamlit as st

@st.cache_resource()
def load_model():
    return Model.from_file(OUTFILE)