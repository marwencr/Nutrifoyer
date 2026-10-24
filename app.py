import streamlit as st
from PIL import Image
import random
from datetime import datetime

# إعدادات الصفحة مع أيقونة طبق السلطة 🥗
st.set_page_config(page_title="NutriFoyer", page_icon="🥗", layout="centered")

# تهيئة حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Marwan"
if 'gender' not in st.session_state:
    st.session_state.gender = "Homme"
if 'age' not in st.session_state:
    st.session_state.age = 22
if 'weight' not in st.session_state:
    st.session_state.weight = 70
if 'height' not in st.session_state:
    st.session_state.height = 175
if 'edit_profile' not in st.session_state:
    st.session_state.edit_profile = False

# حالات الماسح والصورة
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'nutrients' not in st.session_state:
    st.session_state.nutrients = {}

# حالات نظام التقييم بالنجوم
if 'show_rating_page' not in st.session_state:
    st.session_state.show_rating_page = False
if 'rating_success' not in st.session_state:
    st.session_state.rating_success = False

# تخزين التقييمات للغداء والعشاء
if 'lunch_ratings' not in st.session_state:
    st.session_state.lunch_ratings = [5, 4, 5, 4, 5]
if 'dinner_ratings' not in st.session_state:
    st.session_state.dinner_ratings = [4, 3, 5, 4, 4]

# تصميم الواجهة الاحترافية والمؤشر الملون
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f1f8f5 0%, #e2f0ea 100%);
    }
    .main-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #c8e6c9;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.08);
        margin-bottom: 10px;
    }
    .action-box {
        background: #f4fbf7;
        border: 2px dashed #81c784;
        border-radius: 14px;
        padding: 12px;
        text-align: center;
    }
    .metric-box {
        background: #f8f9fa;
        border: 1px solid #d0d7de;
        border-radius: 10px;
        padding: 8px;
        text-align: center;
    }
    .tip-box-green {
        background: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 13px;
        color: #1b5e20;
    }
    .tip-box-orange {
        background: #fff3e0;
        border-left: 5px solid #ef6c00;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 13px;
        color: #e65100;
    }
    .tip-box-blue {
        background: #e3f2fd;
        border-left: 5px solid #1565c0;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 13px;
        color: #0d47a1;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        background-color: #2e7d32;
        color: white;
        border: none;
        height: 40px;
        box-shadow: 0 3px 10px rgba(46, 125, 50, 0.2);
        transition: all 0.3s;
    }
