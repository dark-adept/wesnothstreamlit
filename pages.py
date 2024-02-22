import streamlit as st

from io import StringIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



import wesnothanalytics as wa


from util import load_replay,apply_filter1, apply_filter2, apply_filter3, apply_filter4




class Page:

    def __init__(self,content):

        self.content = content
    

    def render_frame(self,lang):

        translation = self.content[lang]

        st.markdown("<h1 style='text-align: center;'>" + translation["title"] + "</h1>", unsafe_allow_html=True)
        st.write("-"*50)

        if "sidebar-title" in translation:
            st.sidebar.markdown(translation["sidebar-title"])


        self.render_content(translation,lang)


    def render_content(self,translation,lang):

        pass





class Home(Page):

    def __init__(self,content):
        super().__init__(content["homepage"]) 


    def render_frame(self,lang):

        translation = self.content[lang]
        st.markdown("<h1 style='text-align: center;'>" + translation["title"] + "</h1>", unsafe_allow_html=True)
        st1,st2,st3 = st.columns(3)
        st1.image("appdata/DarkAdept.png")
        st2.image("appdata/WalkingCorpse.png")
        st3.image("appdata/DragonGuard.png")


        st.write("-"*50)

        if "sidebar-title" in translation:
            st.sidebar.markdown(translation["sidebar-title"])


        replay = st.sidebar.file_uploader(translation["replay"], type=["txt"], accept_multiple_files=False)
        

        if replay is not None:

            try:
                
                replay_name, file_type = replay.name.split(".")

                assert file_type=="txt"

                data = load_replay(replay)

                if replay_name!=st.session_state["replay_name"]:
                    st.session_state["replay_uploaded"] = replay
                    st.session_state["replay_name"] = replay_name
                    st.session_state["replay_data"] = data
                    st.experimental_rerun()


            except Exception as e:
                st.write(f'Error in parsing replay file "{replay.name}"')
                st.session_state["replay_uploaded"] = None
                st.session_state["replay_name"] = None
                st.session_state["replay_data"] = None
                st.write(e)


        if st.session_state["replay_name"]:
            st.markdown("<h1 style='text-align: center;font-size:18px;'>" + f'Replay "{st.session_state["replay_name"]}" parsed correctly' + "</h1>", unsafe_allow_html=True)    












class Metadata(Page):

    def __init__(self,content):
        super().__init__(content["metadata"]) 


    def render_content(self,translation,lang):



        # index1 = list(translation["sidebar-filter1-options"].keys()).index(st.session_state["filter1"])
        # st.session_state["filter1"] = st.sidebar.selectbox(translation["sidebar-filter1-text"], translation["sidebar-filter1-options"].keys(), format_func=lambda x:translation["sidebar-filter1-options"][x],on_change=apply_filter1,key="new_filter1",index=index1) 

        metadata = st.session_state["replay_data"]["meta"]


        st.markdown("<h1 style='text-align: center;font-size:24px;'>" + f'VERSION - {metadata["version"]}' + "</h1>", unsafe_allow_html=True)    

        st.markdown("<h1 style='text-align: center;font-size:18px;'>" + f'MAP - {metadata["map"]}' + "</h1>", unsafe_allow_html=True)    

        st.write("-"*50)

        sts = st.columns(2)

        for i,col in enumerate(sts, start=1):
            cur_player = metadata["players"][i]
            col.markdown("<h1 style='text-align: center;font-size:18px;'>" + f'PLAYER {i}' + "</h1>", unsafe_allow_html=True)
            col.markdown("<h1 style='font-size:12px;'>" + f'Name:    {cur_player["player"]}' + "</h1>", unsafe_allow_html=True) 
            col.markdown("<h1 style='font-size:12px;'>" + f'Faction: {cur_player["faction"]}' + "</h1>", unsafe_allow_html=True) 
            col.markdown("<h1 style='font-size:12px;'>" + f'Leader:  {cur_player["leader"]}' + "</h1>", unsafe_allow_html=True)  





        st.write("-"*50)






class Turns(Page):

    def __init__(self,content):
        super().__init__(content["turns"]) 


    def render_content(self,translation,lang):


        df = pd.DataFrame(st.session_state["replay_data"]["turns"])


        if st.session_state["filter1"]=="all":
            st.session_state["filter1"] = (1,df.turn.max())

        st.session_state["filter1"] = st.sidebar.slider(translation["sidebar-filter1-text"],1,df.turn.max(),st.session_state["filter1"])


        index2 = list(translation["sidebar-filter2-options"].keys()).index(st.session_state["filter2"])
        st.session_state["filter2"] = st.sidebar.selectbox(translation["sidebar-filter2-text"], translation["sidebar-filter2-options"].keys(), format_func=lambda x:translation["sidebar-filter2-options"][x],on_change=apply_filter2,key="new_filter2",index=index2) 

        visible_df = df[(df.turn.between(*st.session_state["filter1"]))&((df.side.astype(str)==st.session_state["filter2"])|(st.session_state["filter2"]=="both"))]
        st.table(visible_df)

        st.download_button(
        "Press to Download",
        df.to_csv(index=False).encode('utf-8'),
        f'{st.session_state["replay_name"]}_turns.csv',
        "text/csv",
        key='download-csv'
        )











class Actions(Page):

    def __init__(self,content):
        super().__init__(content["actions"]) 


    def render_content(self,translation,lang):






        df = pd.DataFrame(st.session_state["replay_data"]["actions"])
        df[["combat_string","combat_ids"]].fillna("", inplace=True)


        if st.session_state["filter1"]=="all":
            st.session_state["filter1"] = (1,df.turn.max())

        st.session_state["filter1"] = st.sidebar.slider(translation["sidebar-filter1-text"],1,df.turn.max(),st.session_state["filter1"])


        index2 = list(translation["sidebar-filter2-options"].keys()).index(st.session_state["filter2"])
        st.session_state["filter2"] = st.sidebar.selectbox(translation["sidebar-filter2-text"], translation["sidebar-filter2-options"].keys(), format_func=lambda x:translation["sidebar-filter2-options"][x],on_change=apply_filter2,key="new_filter2",index=index2) 



        st.sidebar.multiselect(label="Actions", options=["attack","move","recruit","resurrect","level"], default=st.session_state["filter3"], on_change=apply_filter3, key="new_filter3")

        new_filter4 = st.sidebar.checkbox(translation["sidebar-filter4-text"], on_change=apply_filter4, key="new_filter4")

        visible_df = df[(df.turn.between(*st.session_state["filter1"]))&((df.side.astype(str)==st.session_state["filter2"])|(st.session_state["filter2"]=="both"))&(df.action.isin(st.session_state["filter3"]))&(((df.unit=="PHANTOM")|(df.combat_string=="PHANTOM"))|(not st.session_state["filter4"]))]

        st.table(visible_df)



        st.download_button(
        "Press to Download",
        df.to_csv(index=False).encode('utf-8'),
        f'{st.session_state["replay_name"]}_actions.csv',
        "text/csv",
        key='download-csv'
        )




class Flags(Page):

    def __init__(self,content):
        super().__init__(content["flags"]) 



    def render_content(self,translation,lang):


        flags = st.session_state["replay_data"]["flags"]


        for flag,b in flags.items():
            st.markdown(f'<p style="color:{"#13a113" if b else "#cc2118"};text-align: center;font-size:24px;">{flag.replace("_"," ").title()}</p>', unsafe_allow_html=True)
            st.write(translation["correct" if b else "incorrect"][flag])


            st.write("-"*50)        






class Bugs(Page):

    def __init__(self,content):
        super().__init__(content["bugs"]) 



    def render_content(self,translation,lang):


        st.sidebar.button("Submit issue")

        comments = st.text_input("Enter comments here: ")

        st.write(f'Comments: {comments}')
