import yaml
import streamlit as st
from pages import Home, Metadata, Turns, Actions, Flags, Bugs
from util import translate, flip_page


if "page" not in st.session_state:
    st.session_state["page"] = "homepage"

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

if "replay_uploaded" not in st.session_state:
    st.session_state["replay_uploaded"] = None
    st.session_state["replay_name"] = None
    st.session_state["replay_data"] = None

if "filter1" not in st.session_state:
    st.session_state["filter1"] = "all"
    st.session_state["filter2"] = "both"
    st.session_state["filter3"] = ["attack","move","recruit","resurrect","level"]
    st.session_state["filter4"] = False




# @st.cache
def load_content():

    with open("content.yml","rb") as f:

        return yaml.load(f,Loader=yaml.FullLoader)

content = load_content()


# st.set_page_config(layout='wide') 


languages = ["English","Italiano","Deutsch"]
lang_index = languages.index(st.session_state["lang"])
st.session_state["lang"] = st.sidebar.selectbox(content["translate"][st.session_state["lang"]], options=languages, on_change=translate, key="new_language", index=lang_index)



if st.session_state["replay_uploaded"]:
    pages = {
            "homepage": Home
             ,"metadata": Metadata
             ,"turns": Turns
             ,"actions": Actions
             ,"flags": Flags
            #  ,"bugs": Bugs
             }
else:
    pages = {"homepage": Home}




def grab_page(selected_page,translation):
    return {"f1":selected_page(translation)}




page_index = list(pages.keys()).index(st.session_state["page"])
selected_page = st.sidebar.selectbox(content["navigator"][st.session_state["lang"]], pages.keys(), format_func=lambda x:content[x][st.session_state["lang"]]["name"], on_change=flip_page, key="new_page", index=page_index)





current_page = grab_page(pages[selected_page], content)["f1"]
current_page.render_frame(st.session_state["lang"])