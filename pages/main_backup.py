# Set up and run this Streamlit App
import streamlit as st
from logics.customer_query_handler import process_user_message
from utility import check_password

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="HDB resale Intelligent Bot"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit App Configuration --------->

st.title("HDB resale Intelligent Bot")
st.write("Ask me anything about HDB resale transaction")




# form = st.form(key="form")
# form.subheader("Prompt")



# # user_prompt = form.text_area("Enter your prompt here", height=200)

# if form.form_submit_button("Submit"):
#     st.toast("User Input Submitted - {user_prompt}")
#     response = process_user_message(user_prompt) #<--- This calls the `process_user_message` function that we have created 🆕
#     st.write(response[0])
#     response[1]
#     print(f"User Input is {user_prompt}")

import streamlit as st
from streamlit_chat import message


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
img_path = "https://www.groundzeroweb.com/wp-content/uploads/2017/05/Funny-Cat-Memes-11.jpg"
youtube_embed = '''
<iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
'''

st.session_state.setdefault(
    'past', 
    ['plan text with line break',
     'play the song "Dancing Vegetables"', 
     'show me image of cat', 
     'and video of it']
)
st.session_state.setdefault(
    'generated', 
    [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'},
     {'type': 'normal', 'data': f'<audio controls src="{audio_path}"></audio>'}, 
     {'type': 'normal', 'data': f'<img width="100%" height="200" src="{img_path}"/>'}, 
     {'type': 'normal', 'data': f'{youtube_embed}'}]
)

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")