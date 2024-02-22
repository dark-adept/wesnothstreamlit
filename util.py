import streamlit as st

from io import StringIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import wesnothanalytics as wa


def translate():

    if st.session_state.new_language:
        st.session_state["lang"] = st.session_state.new_language


def flip_page():

    if st.session_state.new_page:
        st.session_state["page"] = st.session_state.new_page


@st.cache
def load_replay(replay):

    return wa.parse_data(StringIO(replay.getvalue().decode("utf-8")).read())


def apply_filter1():

    st.session_state["filter1"] = st.session_state.new_filter1



def apply_filter2():

    st.session_state["filter2"] = st.session_state.new_filter2

def apply_filter3():

    st.session_state["filter3"] = st.session_state.new_filter3

def apply_filter4():

    st.session_state["filter4"] = st.session_state.new_filter4




