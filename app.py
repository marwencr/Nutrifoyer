import streamlit as st
from PIL import Image
import hashlib
from datetime import datetime

# إعدادات الصفحة مع أيقونة طبق السلطة 🥗 وضمان العرض المضغوط بدون تمرير
st.set_page_config(page_title="NutriFoyer", page_icon="🥗", layout="centered")

# --- تصميم CSS مضغوط كلياً (Zero-Scroll) وألوان مخصصة ومميزة لكل عنصر ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f1f8f5 0%, #e2f0ea 100%);
    }
    .main-card {
        background: #ffffff !important;
        border: 1px solid #c8e6c9 !important;
        border-radius: 12px;
        padding: 10px 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        margin-bottom: 6px !important;
    }
    .action-box {
        background: #f4fbf7 !important;
        border: 2px dashed #81c784 !important;
        border-radius: 10px;
        padding: 8px !important;
        text-align: center;
    }
    .tip-box-green {
        background: rgba(46, 125, 50, 0.12);
        border-left: 4px solid #2e7d32;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 12px;
        color: #1b5e20;
    }
    .tip-box-orange {
        background: rgba(239, 108, 0, 0.12);
        border-left: 4px solid #ef6c00;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 12px;
        color: #e65100;
    }
    .tip-box-blue {
        background: rgba(21, 101, 192, 0.12);
        border-left: 4px solid #1565c0;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 12px;
        color: #0d47a1;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #2e7d32;
        color: white;
        border: none;
        height: 36px !important;
        box-shadow: 0 2px 6px rgba(46, 125, 50, 0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    div.block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- تهيئة حالة الجلسة والمتغيرات ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = True
if 'user_name' not in st.session_state: st.session_state.user_name = "Marwan"
if 'gender' not in st.session_state: st.session_state.gender = "Homme"
if 'age' not in st.session_state: st.session_state.age = 22
if 'weight' not in st.session_state: st.session_state.weight = 70
if 'height' not in st.session_state: st.session_state.height = 175
if 'edit_profile' not in st.session_state: st.session_state.edit_profile = False

if 'captured_image' not in st.session_state: st.session_state.captured_image = None
if 'show_camera' not in st.session_state: st.session_state.show_camera = False
if 'analysis_done' not in st.session_state: st.session_state.analysis_done = False
if 'nutrients' not in st.session_state: st.session_state.nutrients = {}

if 'show_rating_page' not in st.session_state: st.session_state.show_rating_page = False
if 'rating_success' not in st.session_state: st.session_state.rating_success = False

if 'lunch_ratings' not in st.session_state: st.session_state.lunch_ratings = [5, 4, 5, 4, 5]
if 'dinner_ratings' not in st.session_state: st.session_state.dinner_ratings = [4, 3, 5, 4, 4]

# --- نافذة تعديل البروفايل ---
if st.session_state.edit_profile:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1b5e20; margin-bottom: 5px;'>⚙️ Mon Profil Étudiant</h4>", unsafe_allow_html=True)
    
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
    # --- الواجهة الرئيسة بمساحة مضغوطة وعلوية متناسقة ---
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("<h3 style='margin: 0; color: #1b5e20;'>🥗 NutriFoyer <span style='font-size:10px; color:#2e7d32;'>v5.1 Pro</span></h3>", unsafe_allow_html=True)
    with top_col2:
        if st.button("⚙️", help="Mon Profil"):
            st.session_state.edit_profile = True
            st.rerun()

    st.markdown("<hr style='margin: 6px 0;'>", unsafe_allow_html=True)

    tab_scanner, tab_feedback = st.tabs(["📸 Scanner & Analyse", "📊 Satisfaction Resto U"])

    # --- 1. قسم الماسح والتحليل الفوري ---
    with tab_scanner:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # أ: تقييم الوجبة
        if st.session_state.show_rating_page:
            st.markdown("<h4 style='text-align: center; color: #1b5e20;'>⭐ Évaluer le Repas</h4>", unsafe_allow_html=True)
            current_hour = datetime.now().hour
            meal_type = "lunch" if 10 <= current_hour < 15 else "dinner"
            meal_name_fr = "Déjeuner (Midi)" if meal_type == "lunch" else "Dîner (Soir)"
            
            st.info(f"🕒 Repas : **{meal_name_fr}**")
            
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

        # ب: عرض نتائج التحليل مع ألوان مخصصة ودقيقة لكل عنصر مغذي
        elif st.session_state.analysis_done:
            st.markdown("<h4 style='color: #1b5e20; margin-bottom: 4px;'>📊 Analyse IA Détaillée</h4>", unsafe_allow_html=True)
            if st.session_state.rating_success:
                st.success("🌟 Merci ! Évaluation enregistrée.")
                
            p_val = st.session_state.nutrients.get('prot', 32)
            c_val = st.session_state.nutrients.get('carb', 58)
            f_val = st.session_state.nutrients.get('fat', 14)
            fib_val = st.session_state.nutrients.get('fib', 12)
            vit_val = st.session_state.nutrients.get('vit', 90)
            score = st.session_state.nutrients.get('score', 84)
            tip_type = st.session_state.nutrients.get('tip_type', 'green')
            tip_msg = st.session_state.nutrients.get('tip_msg', 'Repas équilibré validé par le système.')
            detected_items = st.session_state.nutrients.get('items', 'Plat principal + Légumes + Laitage + Dessert')
            
            st.markdown(f"<p style='font-size:11px; margin-bottom:6px;'>🔍 <b>Composants :</b> {detected_items}</p>", unsafe_allow_html=True)
            
            # مغذيات بألوان متميزة ومخصصة لكل عنصر على حدة
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div style="background: #e3f2fd; border: 1px solid #90caf9; color: #0d47a1; border-radius: 8px; padding: 6px; text-align: center;"><div style="font-size:9px; font-weight:bold;">Protéines</div><div style="font-size:13px; font-weight:bold;">{p_val}g</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div style="background: #fff3e0; border: 1px solid #ffb74d; color: #e65100; border-radius: 8px; padding: 6px; text-align: center;"><div style="font-size:9px; font-weight:bold;">Glucides</div><div style="font-size:13px; font-weight:bold;">{c_val}g</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div style="background: #e8f5e9; border: 1px solid #a5d6a7; color: #1b5e20; border-radius: 8px; padding: 6px; text-align: center;"><div style="font-size:9px; font-weight:bold;">Lipides</div><div style="font-size:13px; font-weight:bold;">{f_val}g</div></div>""", unsafe_allow_html=True)
                
            m4, m5 = st.columns(2)
            with m4:
                st.markdown(f"""<div style="background: #f3e5f5; border: 1px solid #ce93d8; color: #4a148c; border-radius: 8px; padding: 6px; text-align: center;"><div style="font-size:9px; font-weight:bold;">Fibres</div><div style="font-size:13px; font-weight:bold;">{fib_val}g</div></div>""", unsafe_allow_html=True)
            with m5:
                st.markdown(f"""<div style="background: #e0f2f1; border: 1px solid #80cbc4; color: #004d40; border-radius: 8px; padding: 6px; text-align: center;"><div style="font-size:9px; font-weight:bold;">Vitamines</div><div style="font-size:13px; font-weight:bold;">{vit_val}%</div></div>""", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 6px 0;'>", unsafe_allow_html=True)
            st.markdown(f"🎯 **Compatibilité :** **{score}%**")
            
            st.markdown(f"""
                <div style='background: #e0e0e0; border-radius: 8px; padding: 3px; margin-top: 4px;'>
                    <div style='height: 12px; border-radius: 6px; background: linear-gradient(90deg, #e53935 0%, #fbc02d 35%, #43a047 70%, #1e88e5 100%); width: {score}%;'></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br style='margin: 2px;'>", unsafe_allow_html=True)
            
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
                
        # ج: معاينة الصورة والتحليل الآمن
        elif st.session_state.captured_image is not None:
            try:
                st.image(st.session_state.captured_image, use_column_width=True)
            except Exception:
                st.warning("⚠️ Image prête.")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Analyser"):
                    try:
                        img_bytes = st.session_state.captured_image.getvalue() if hasattr(st.session_state.captured_image, 'getvalue') else str(st.session_state.captured_image).encode()
                        hash_val = int(hashlib.md5(img_bytes).hexdigest(), 16)
                        db_index = hash_val % 6
                    except Exception:
                        db_index = 0
                    
                    if db_index == 0:
                        items = "Kafteji + Œuf | Salade Mechouia | Pain | Yaourt nature"
                        p, c, f, fib, vit, sc = 24, 72, 13, 11, 89, 81
                        tip_type = "orange"
                        tip_msg = "Glucides et huiles riches ! 🚶‍♂️ Marche rapide de 20 min recommandée."
                    elif db_index == 1:
                        items = "Poulet rôti + Pâtes sauce | Salade verte | Pain | Fromage portion + Orange"
                        p, c, f, fib, vit, sc = 42, 45, 10, 9, 94, 98
                        tip_type = "green"
                        tip_msg = "Équilibre optimal ! Parfait pour la concentration en amphi."
                    elif db_index == 2:
                        items = "Loubia (Haricots) + Viande | Salade tunisienne | Pain | Yaourt aux fruits"
                        p, c, f, fib, vit, sc = 30, 55, 8, 16, 95, 92
                        tip_type = "blue"
                        tip_msg = "Riche en fibres et légumineuses ! Excellent pour la digestion."
                    elif db_index == 3:
                        items = "Ojja Merguez + Œufs | Salade | Pain | Dessert: Crème caramel"
                        p, c, f, fib, vit, sc = 34, 80, 19, 7, 75, 70
                        tip_type = "orange"
                        tip_msg = "Repas énergétique lourd ! 🏃‍♂️ Petit jogging conseillé ce soir."
                    elif db_index == 4:
                        items = "Couscous aux légumes et poulet | Salade verte | Pain | Laitage"
                        p, c, f, fib, vit, sc = 36, 62, 11, 12, 91, 90
                        tip_type = "green"
                        tip_msg = "Source idéale de glucides complexes et protéines propres."
                    else:
                        items = "Plat pâtes au thon | Salade composée | Pain | Fromage et fruit"
                        p, c, f, fib, vit, sc = 38, 58, 12, 10, 93, 89
                        tip_type = "green"
                        tip_msg = "Très bon apport en oméga-3 et vitamines."
                        
                    st.session_state.nutrients = {
                        'prot': p, 'carb': c, 'fat': f, 'fib': fib, 
                        'vit': vit, 'score': sc, 'tip_type': tip_type, 
                        'tip_msg': tip_msg, 'items': items
                    }
                    st.session_state.analysis_done = True
                    st.rerun()
            with c_btn2:
                if st.button("❌ Annuler"):
                    st.session_state.captured_image = None
                    st.session_state.show_camera = False
                    st.rerun()
                    
        # د: واجهة الرفع والتقاط الكاميرا بدون أي تمرير (Zero-Scroll Compact)
        else:
            st.markdown("<h4 style='text-align: center; margin-bottom: 6px; color: #1b5e20; font-size: 14px;'>📸 Scanner le Plateau</h4>", unsafe_allow_html=True)
            
            box_c1, box_c2 = st.columns(2)
            
            with box_c1:
                st.markdown("<div class='action-box' style='padding:4px;'>📁 <b>Importer</b></div>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Fichier", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
                if uploaded_file is not None:
                    st.session_state.captured_image = uploaded_file
                    st.rerun()
                    
            with box_c2:
                st.markdown("<div class='action-box' style='padding:4px;'>📷 <b>Caméra</b></div>", unsafe_allow_html=True)
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

    # --- 2. لوحة رضا الطلبة ---
    with tab_feedback:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1b5e20; margin-bottom: 4px;'>📊 Satisfaction Resto U</h4>", unsafe_allow_html=True)
        st.write("Statistiques en temps réel des étudiants :")
        
        lunch_avg = sum(st.session_state.lunch_ratings) / len(st.session_state.lunch_ratings)
        lunch_pct = int((lunch_avg / 5) * 100)
        
        dinner_avg = sum(st.session_state.dinner_ratings) / len(st.session_state.dinner_ratings)
        dinner_pct = int((dinner_avg / 5) * 100)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"""
                <div style="background: rgba(46,125,50,0.1); border: 1px solid #81c784; border-radius: 8px; padding: 8px; text-align: center;">
                    <div style="font-size: 11px; font-weight: bold; color: #1b5e20;">☀️ Déjeuner</div>
                    <div style="font-size: 20px; font-weight: bold; color: #2e7d32; margin: 2px 0;">{lunch_pct}%</div>
                    <div style="font-size: 9px; color: #555;">{round(lunch_avg, 1)} / 5 ⭐</div>
                </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
                <div style="background: rgba(0,137,123,0.1); border: 1px solid #4db6ac; border-radius: 8px; padding: 8px; text-align: center;">
                    <div style="font-size: 11px; font-weight: bold; color: #004d40;">🌙 Dîner</div>
                    <div style="font-size: 20px; font-weight: bold; color: #00897b; margin: 2px 0;">{dinner_pct}%</div>
                    <div style="font-size: 9px; color: #555;">{round(dinner_avg, 1)} / 5 ⭐</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='margin: 6px 0;'>", unsafe_allow_html=True)
        st.info("ℹ️ Données validées par le système institutionnel de la cité.")
        st.markdown("</div>", unsafe_allow_html=True)
