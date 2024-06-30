import streamlit as st
import streamlit_shadcn_ui as ui
st.set_page_config(layout="wide")

from backend.database import in_memory as db
st.title('Visite virtuelle avec Casami')



with st.sidebar as sidebar:
    props = db.get_properties()
    property_select = st.selectbox('Select a property to visit', 
                    [property['id'] for property in props],
                    format_func=lambda x: props[x]['name'])
    selected_property = props[property_select]


# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant",
#          "content": "Bonjour, je suis un assistant IA pour vous accompagner pour cette visite virtuel. Nous visitons virtuellement cet appartement ensemble, pièces par pièces à travers des vidéos et des images. A tout moment vous pouvez me poser des questions sur ce bien. Êtes-vous prêts?"},
#         {"role": "user",
#          "content": "Oui, je suis prêt"},
#         {"role": "assistant",
#         "content": "Parfait, commençons à l'entrée..."},
#     ]
if "view_idx" not in st.session_state:
    st.session_state.view_idx = 0

media, chat = st.columns([2, 1])
with media:
    views = db.get_views_by_property_id(selected_property['id'])

    def update_view_idx():
        st.session_state.view_idx = st.session_state.view_idx_select

    view_idx = st.selectbox('Select a room to visit', 
                    range(len(views)),
                    key='view_idx_select',
                    index=st.session_state.view_idx,
                    format_func=lambda x: views[x]['name'], 
                    on_change=update_view_idx)
    
    left, right = st.columns([1, 1])
    with left:
        if st.session_state.view_idx > 0:
            if st.button('Previous'):
                st.session_state.view_idx -= 1
                st.rerun()
    with right:
        if st.session_state.view_idx < len(views)-1:
            if st.button('Next'):
                st.session_state.view_idx += 1
                st.rerun()
        
    current_view = views[st.session_state.view_idx]
    st.video(data=current_view['video'], 
            subtitles=current_view.get('subtitles', None),)

# with chat:
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     prompt = st.chat_input('Poszer votre question ici...')

#     if prompt:
#         with st.chat_message(name='user'):
#             st.write('Quelle est la surface de la cuisine ?')


