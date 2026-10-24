import streamlit as st
from PIL import Image
import random
from datetime import datetime

# إعدادات الصفحة
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
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    </style>
""", unsafe_allow_html=True)

# --- نافذة تعديل البروفايل ---
if st.session_state.edit_profile:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1b5e20; text-align: center;'>⚙️ Mon Profil</h3>", unsafe_allow_html=True)
    
    st.session_state.user_name = st.text_input("Nom", st.session_state.user_name)
    st.session_state.gender = st.selectbox("Sexe", ["Homme", "Femme"], index=0 if st.session_state.gender=="Homme" else 1)
    st.session_state.age = st.number_input("Âge", 17, 40, st.session_state.age)
    st.session_state.weight = st.number_input("Poids (kg)", 40, 150, st.session_state.weight)
    st.session_state.height = st.number_input("Taille (cm)", 140, 200, st.session_state.height)
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        if st.button("💾 Enregistrer"):
            st.session_state.edit_profile = False
            st.success("Mis à jour !")
            st.rerun()
    with col_e2:
        if st.button("❌ Retour"):
            st.session_state.edit_profile = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- التطبيق الرئيسي ---
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("<h3 style='color: #1b5e20; margin: 0;'>🥗 NutriFoyer</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #4caf50; font-size: 11px; margin: 0;'>Équilibre en cité universitaire</p>", unsafe_allow_html=True)
    with top_col2:
        if st.button("⚙️"):
            st.session_state.edit_profile = True
            st.rerun()

    st.markdown("---")

    w = st.session_state.weight
    h = st.session_state.height
    a = st.session_state.age
    g = st.session_state.gender
    bmr = (10 * w) + (6.25 * h) - (5 * a) + (5 if g == "Homme" else -161)

    tab_scanner, tab_feedback = st.tabs(["📸 Scanner & Analyse", "📊 Satisfaction Resto U"])

    # --- 1. قسم الماسح والتحليل ---
    with tab_scanner:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # أ: صفحة التقييم بالنجوم
        if st.session_state.show_rating_page:
            st.markdown("<h4 style='color: #1b5e20; text-align: center;'>⭐ Noter le Repas</h4>", unsafe_allow_html=True)
            current_hour = datetime.now().hour
            meal_type = "lunch" if 10 <= current_hour < 15 else "dinner"
            meal_name_fr = "Déjeuner" if meal_type == "lunch" else "Dîner"
            
            st.info(f"🕒 Repas détecté : **{meal_name_fr}**")
            
            rc1, rc2, rc3, rc4, rc5 = st.columns(5)
            with rc1:
                if st.button("⭐ 1"):
                    if meal_type == "lunch": st.session_state.lunch_ratings.append(1)
                    else: st.session_state.dinner_ratings.append(1)
                    st.session_state.show_rating_page = False
                    st.session_state.rating_success = True
                    st.rerun()
            with rc2:
                if st.button("⭐⭐ 2"):
                    if meal_type == "lunch": st.session_state.lunch_ratings.append(2)
                    else: st.session_state.dinner_ratings.append(2)
                    st.session_state.show_rating_page = False
                    st.session_state.rating_success = True
                    st.rerun()
            with rc3:
                if st.button("⭐⭐⭐ 3"):
                    if meal_type == "lunch": st.session_state.lunch_ratings.append(3)
                    else: st.session_state.dinner_ratings.append(3)
                    st.session_state.show_rating_page = False
                    st.session_state.rating_success = True
                    st.rerun()
            with rc4:
                if st.button("⭐⭐⭐⭐ 4"):
                    if meal_type == "lunch": st.session_state.lunch_ratings.append(4)
                    else: st.session_state.dinner_ratings.append(4)
                    st.session_state.show_rating_page = False
                    st.session_state.rating_success = True
                    st.rerun()
            with rc5:
                if st.button("⭐⭐⭐⭐⭐ 5"):
                    if meal_type == "lunch": st.session_state.lunch_ratings.append(5)
                    else: st.session_state.dinner_ratings.append(5)
                    st.session_state.show_rating_page = False
                    st.session_state.rating_success = True
                    st.rerun()
                    
            if st.button("❌ Retour"):
                st.session_state.show_rating_page = False
                st.rerun()

        # ب: عرض النتائج والمؤشر الملون الجديد والنصائح المبوبة
        elif st.session_state.analysis_done:
            st.markdown("<h4 style='color: #1b5e20;'>📊 Résultats Nutritionnels</h4>", unsafe_allow_html=True)
            if st.session_state.rating_success:
                st.success("🌟 Merci ! Évaluation enregistrée.")
                
            p_val = st.session_state.nutrients['prot']
            c_val = st.session_state.nutrients['carb']
            f_val = st.session_state.nutrients['fat']
            fib_val = st.session_state.nutrients['fib']
            vit_val = st.session_state.nutrients['vit']
            score = st.session_state.nutrients['score']
            tip_type = st.session_state.nutrients['tip_type']
            tip_msg = st.session_state.nutrients['tip_msg']
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="metric-box"><div style="font-size:10px; color:#1565c0; font-weight:bold;">Protéines</div><div style="font-size:15px; color:#0d47a1; font-weight:bold;">{p_val}g</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class="metric-box"><div style="font-size:10px; color:#e65100; font-weight:bold;">Glucides</div><div style="font-size:15px; color:#bf360c; font-weight:bold;">{c_val}g</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-box"><div style="font-size:10px; color:#2e7d32; font-weight:bold;">Lipides</div><div style="font-size:15px; color:#1b5e20; font-weight:bold;">{f_val}g</div></div>""", unsafe_allow_html=True)
                
            m4, m5 = st.columns(2)
            with m4:
                st.markdown(f"""<div class="metric-box"><div style="font-size:10px; color:#6a1b9a; font-weight:bold;">Fibres</div><div style="font-size:15px; color:#4a148c; font-weight:bold;">{fib_val}g</div></div>""", unsafe_allow_html=True)
            with m5:
                st.markdown(f"""<div class="metric-box"><div style="font-size:10px; color:#00695c; font-weight:bold;">Vitamines</div><div style="font-size:15px; color:#004d40; font-weight:bold;">{vit_val}%</div></div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(f"🎯 **Compatibilité profil :** **{score}%**")
            
            # المؤشر الملون المتدرج (أحمر ➔ أصفر ➔ أخضر ➔ أزرق للأكثر ملائمة)
            st.markdown(f"""
                <div style='background: #e0e0e0; border-radius: 10px; padding: 4px; margin-top: 6px;'>
                    <div style='height: 16px; border-radius: 8px; background: linear-gradient(90deg, #e53935 0%, #fbc02d 35%, #43a047 70%, #1e88e5 100%); width: {score}%;'></div>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 10px; color: #555; margin-top: 3px; font-weight: bold;'>
                    <span style='color: #e53935;'>Faible</span>
                    <span style='color: #fbc02d;'>Moyen</span>
                    <span style='color: #43a047;'>Bon</span>
                    <span style='color: #1e88e5;'>Optimal (Bleu)</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("💡 **Conseils & Actions Recommandées :**", unsafe_allow_html=True)
            
            # عرض النصيحة في مربعات ملونة قصيرة ومنظمة
            if tip_type == "green":
                st.markdown(f"<div class='tip-box-green'>🥗 {tip_msg}</div>", unsafe_allow_html=True)
            elif tip_type == "orange":
                st.markdown(f"<div class='tip-box-orange'>⚠️ {tip_msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='tip-box-blue'>⚡ {tip_msg}</div>", unsafe_allow_html=True)
            
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("⭐ Noter"):
                    st.session_state.show_rating_page = True
                    st.session_state.rating_success = False
                    st.rerun()
            with col_act2:
                if st.button("🔄 Nouveau"):
                    st.session_state.captured_image = None
                    st.session_state.analysis_done = False
                    st.session_state.show_camera = False
                    st.session_state.rating_success = False
                    st.rerun()
                
        # ج: معاينة الصورة والتحليل الذكي
        elif st.session_state.captured_image is not None:
            st.image(st.session_state.captured_image, use_column_width=True)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Analyser"):
                    img_bytes = st.session_state.captured_image.getvalue() if hasattr(st.session_state.captured_image, 'getvalue') else str(st.session_state.captured_image).encode()
                    db_index = sum(img_bytes) % 4
                    
                    if db_index == 0:
                        p, c, f, fib, vit, sc = 18, 75, 12, 10, 85, 76
                        tip_type = "orange"
                        tip_msg = "Glucides élevés ! 🚶‍♂️ Marchez 25 min pour l'équilibre énergétique."
                    elif db_index == 1:
                        p, c, f, fib, vit, sc = 38, 45, 13, 6, 90, 98
                        tip_type = "green"
                        tip_msg = "Parfait ! 💧 Pensez juste à boire un grand verre d'eau."
                    elif db_index == 2:
                        p, c, f, fib, vit, sc = 25, 58, 8, 14, 95, 89
                        tip_type = "blue"
                        tip_msg = "Riche en fibres ! 🍏 Ajoutez un yaourt pour compléter les protéines."
                    else:
                        p, c, f, fib, vit, sc = 30, 80, 20, 5, 70, 65
                        tip_type = "orange"
                        tip_msg = "Repas lourd ! 🏃‍♂️ Jogging de 30 min recommandé ce soir."
                        
                    st.session_state.nutrients = {
                        'prot': p, 'carb': c, 'fat': f, 'fib': fib, 
                        'vit': vit, 'score': sc, 'tip_type': tip_type, 'tip_msg': tip_msg
                    }
                    st.session_state.analysis_done = True
                    st.rerun()
            with c_btn2:
                if st.button("❌ Annuler"):
                    st.session_state.captured_image = None
                    st.session_state.show_camera = False
                    st.rerun()
                    
        # د: أزرار الماسح المتجاورة (Zero-Scroll)
        else:
            st.markdown("<h4 style='color: #1b5e20; text-align: center; margin-bottom: 8px;'>📸 Scanner le Repas</h4>", unsafe_allow_html=True)
            
            box_c1, box_c2 = st.columns(2)
            
            with box_c1:
                st.markdown("<div class='action-box'>📁 <b>Importer</b></div>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Fichier", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
                if uploaded_file is not None:
                    st.session_state.captured_image = uploaded_file
                    st.rerun()
                    
            with box_c2:
                st.markdown("<div class='action-box'>📷 <b>Caméra</b></div>", unsafe_allow_html=True)
                if not st.session_state.show_camera:
                    if st.button("Ouvrir"):
                        st.session_state.show_camera = True
                        st.rerun()
                else:
                    if st.button("Fermer"):
                        st.session_state.show_camera = False
                        st.rerun()
            
            if st.session_state.show_camera:
                camera_file = st.camera_input("Photo", label_visibility="collapsed")
                if camera_file is not None:
                    st.session_state.captured_image = camera_file
                    st.session_state.show_camera = False
                    st.rerun()
                    
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. لوحة رضا الطلبة للمطعم الجامعي ---
    with tab_feedback:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1b5e20;'>📊 Satisfaction du Resto U</h4>", unsafe_allow_html=True)
        st.write("Indicateurs en temps réel basés sur les évaluations des étudiants :")
        
        lunch_avg = sum(st.session_state.lunch_ratings) / len(st.session_state.lunch_ratings)
        lunch_pct = int((lunch_avg / 5) * 100)
        
        dinner_avg = sum(st.session_state.dinner_ratings) / len(st.session_state.dinner_ratings)
        dinner_pct = int((dinner_avg / 5) * 100)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"""
                <div style="background: #e8f5e9; border: 1px solid #81c784; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 13px; color: #1b5e20; font-weight: bold;">☀️ Déjeuner (Midi)</div>
                    <div style="font-size: 26px; color: #2e7d32; font-weight: bold; margin: 4px 0;">{lunch_pct}%</div>
                    <div style="font-size: 11px; color: #555;">{round(lunch_avg, 1)} / 5 ⭐ ({len(st.session_state.lunch_ratings)} votes)</div>
                </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
                <div style="background: #e0f2f1; border: 1px solid #4db6ac; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 13px; color: #004d40; font-weight: bold;">🌙 Dîner (Soir)</div>
                    <div style="font-size: 26px; color: #00897b; font-weight: bold; margin: 4px 0;">{dinner_pct}%</div>
                    <div style="font-size: 11px; color: #555;">{round(dinner_avg, 1)} / 5 ⭐ ({len(st.session_state.dinner_ratings)} votes)</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.info("ℹ️ Le système classe et met à jour les scores automatiquement selon l'horaire de soumission.")
        st.markdown("</div>", unsafe_allow_html=True)
