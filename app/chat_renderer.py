import streamlit as st
import os
import base64

def get_base64_avatar(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def render_custom_chat_message(role, content, footer_html=""):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bot_logo_path = os.path.join(base_dir, "assets", "bot_logo.png")
    user_icon_path = os.path.join(base_dir, "assets", "user_icon.png")
    
    bot_b64 = get_base64_avatar(bot_logo_path)
    user_b64 = get_base64_avatar(user_icon_path)
    
    if role == "assistant":
        avatar_html = f'<img src="data:image/png;base64,{bot_b64}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;margin-right:12px;flex-shrink:0;">' if bot_b64 else '<span style="font-size:28px;margin-right:12px;">🧬</span>'
        bg_color = "rgba(30, 41, 59, 0.4)"
    else:
        avatar_html = f'<img src="data:image/png;base64,{user_b64}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;margin-right:12px;flex-shrink:0;">' if user_b64 else '<span style="font-size:28px;margin-right:12px;">🧪</span>'
        bg_color = "rgba(15, 23, 42, 0.4)"
        
    # Render the container shell first without raw unescaped markdown nesting issues
    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 14px; background: {bg_color}; padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);">
        {avatar_html}
        <div style="flex-grow: 1; color: #f8fafc; font-size: 15px; line-height: 1.5; word-break: break-word;">
    """, unsafe_allow_html=True)
    
    # Safely render the text payload as true markdown inside the container
    st.markdown(content)
    
    # Render any footer/guardrail badges if present
    if footer_html:
        st.markdown(footer_html, unsafe_allow_html=True)
        
    # Safely close the outer wrapper divs
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)