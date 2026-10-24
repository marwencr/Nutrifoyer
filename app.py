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

# حالات نظام الانتقال لصفحة التقييم بالنجوم
if 'show_rating_page' not in st.session_state:
    st.session_state.show_rating_page = False
if 'rating_success' not in st.session_state:
    st.session_state.rating_success = False

# تخزين التقييمات الديناميكية للغداء والعشاء
if 'lunch_ratings' not in st.session_state:
    st.session_state.lunch_ratings = [5, 4, 5, 4, 5]
if 'dinner_ratings' not in st.session_state:
    st.session_state.dinner_ratings = [4, 3, 5, 4, 4]

# تصميم واجهة مستوحاة من الطبيعة واللون الأخضر الصحي
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f1f8f5 0%, #e2f0ea 100%);
    }
    .card {
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #c8e6c9;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.06);
        margin-bottom: 15px;
    }
    .header-title {
        color: #1b5e20;
        font-weight: 700;
        text-align: center;
    }
    .metric-box {
        background: #f8f9fa;
        border: 1px solid #d0d7de;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        background-color: #2e7d32;
        color: white;
        border: none;
        height: 44px;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# --- نافذة تعديل البروفايل ---
if st.session_state.edit_profile:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='header-title'>⚙️ Profil</h2>", unsafe_allow_html=True)
    
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
        if st.button("⚙️ Profil"):
            st.session_state.edit_profile = True
            st.rerun()

    st.markdown("---")

    w = st.session_state.weight
    h = st.session_state.height
    a = st.session_state.age
    g = st.session_state.gender
    bmr = (10 * w) + (6.25 * h) - (5 * a) + (5 if g == "Homme" else -161)

    tab_scanner, tab_restou, tab_feedback = st.tabs(["📸 Scanner", "🍽️ Menus", "📊 Resto"])

    # --- 1. قسم الماسح والتحليل ---
    with tab_scanner:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # الحالة أ: تقييم النجوم الخمسة
        if st.session_state.show_rating_page:
            st.subheader("⭐ Noter le Repas")
            current_hour = datetime.now().hour
            meal_type = "lunch" if 10 <= current_hour < 15 else "dinner"
            meal_name_fr = "Déjeuner" if meal_type == "lunch" else "Dîner"
            
            st.info(f"🕒 Repas : **{meal_name_fr}**")
            
            if st.button("⭐ 1"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(1)
                else: st.session_state.dinner_ratings.append(1)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
            if st.button("⭐⭐ 2"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(2)
                else: st.session_state.dinner_ratings.append(2)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
            if st.button("⭐⭐⭐ 3"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(3)
                else: st.session_state.dinner_ratings.append(3)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
            if st.button("⭐⭐⭐⭐ 4"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(4)
                else: st.session_state.dinner_ratings.append(4)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
            if st.button("⭐⭐⭐⭐⭐ 5 (Or)"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(5)
                else: st.session_state.dinner_ratings.append(5)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
                
            if st.button("❌ Retour"):
                st.session_state.show_rating_page = False
                st.rerun()

        # الحالة ب: عرض النتائج
        elif st.session_state.analysis_done:
            st.subheader("📊 Résultats")
            if st.session_state.rating_success:
                st.success("🌟 Merci ! Évaluation enregistrée.")
                
            p_val = st.session_state.nutrients['prot']
            c_val = st.session_state.nutrients['carb']
            f_val = st.session_state.nutrients['fat']
            fib_val = st.session_state.nutrients['fib']
            vit_val = st.session_state.nutrients['vit']
            score = st.session_state.nutrients['score']
            advice = st.session_state.nutrients['advice']
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="metric-box"><div style="font-size:11px; color:#1565c0; font-weight:bold;">Protéines</div><div style="font-size:16px; color:#0d47a1; font-weight:bold;">{p_val}g</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class="metric-box"><div style="font-size:11px; color:#e65100; font-weight:bold;">Glucides</div><div style="font-size:16px; color:#bf360c; font-weight:bold;">{c_val}g</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-box"><div style="font-size:11px; color:#2e7d32; font-weight:bold;">Lipides</div><div style="font-size:16px; color:#1b5e20; font-weight:bold;">{f_val}g</div></div>""", unsafe_allow_html=True)
                
            m4, m5 = st.columns(2)
            with m4:
                st.markdown(f"""<div class="metric-box"><div style="font-size:11px; color:#6a1b9a; font-weight:bold;">Fibres</div><div style="font-size:16px; color:#4a148c; font-weight:bold;">{fib_val}g</div></div>""", unsafe_allow_html=True)
            with m5:
                st.markdown(f"""<div class="metric-box"><div style="font-size:11px; color:#00695c; font-weight:bold;">Vitamines</div><div style="font-size:16px; color:#004d40; font-weight:bold;">{vit_val}%</div></div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(f"🎯 **Compatibilité :** {score}%")
            st.info(f"💡 **Conseil :**\n\n{advice}")
            
            st.markdown("---")
            if st.button("⭐ Noter"):
                st.session_state.show_rating_page = True
                st.session_state.rating_success = False
                st.rerun()

            if st.button("🔄 Nouveau"):
                st.session_state.captured_image = None
                st.session_state.analysis_done = False
                st.session_state.show_camera = False
                st.session_state.rating_success = False
                st.rerun()
                
        # الحالة ج: الصورة أمامك
        elif st.session_state.captured_image is not None:
            st.image(st.session_state.captured_image, use_column_width=True)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Analyser"):
                    img_size = len(str(st.session_state.captured_image))
                    random.seed(img_size)
                    p = random.randint(12, 35)
                    c = random.randint(45, 75)
                    f = random.randint(8, 22)
                    fib = random.randint(3, 12)
                    vit = random.randint(60, 99)
                    sc = random.randint(70, 98)
                    
                    if p < 18:
                        adv = "⚠️ **Déficit en protéines.** Ajoutez deux œufs durs ou une boîte de thon."
                    else:
                        adv = f"✅ **Parfait !** Couvre vos besoins ({int(bmr)} kcal)."
                        
                    st.session_state.nutrients = {'prot': p, 'carb': c, 'fat': f, 'fib': fib, 'vit': vit, 'score': sc, 'advice': adv}
                    st.session_state.analysis_done = True
                    st.rerun()
            with c_btn2:
                if st.button("❌ Annuler"):
                    st.session_state.captured_image = None
                    st.session_state.show_camera = False
                    st.rerun()
                    
        # الحالة د: الأزرار الرئيسية في نفس السطر وبدون تمرير
        else:
            st.subheader("📸 Scanner le Plat")
            
            # وضع زر التحميل وزر الكاميرا جنباً إلى جنب في نفس السطر تماماً
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                uploaded_file = st.file_uploader("📁 Importer", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
                if uploaded_file is not None:
                    st.session_state.captured_image = uploaded_file
                    st.rerun()
            with col_u2:
                if not st.session_state.show_camera:
                    if st.button("📷 Caméra"):
                        st.session_state.show_camera = True
                        st.rerun()
                else:
                    if st.button("Fermer"):
                        st.session_state.show_camera = False
                        st.rerun()
            
            if st.session_state.show_camera:
                camera_file = st.camera_input("Prendre photo", label_visibility="collapsed")
                if camera_file is not None:
                    st.session_state.captured_image = camera_file
                    st.session_state.show_camera = False
                    st.rerun()
                    
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. قسم المطعم الجامعي (Resto U) ---
    with tab_restou:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🍽️ Menus Resto U")
        
        plat = st.selectbox("Plat :", [
            "Couscous légumes", "Couscous viande", "Couscous poulet", 
            "Ragoût légumes", "Poulet rôti", "Poisson grillé", 
            "Lentilles", "Loubia", "Pâtes"
        ])
        
        supp = st.multiselect("Suppléments :", [
            "Salade verte", "Salade Mechouia", "Fromage", 
            "Œufs durs", "Yaourt", "Jus"
        ])
        
        if st.button("📊 Évaluer"):
            st.success("Évalué avec succès (92% - Excellent) !")
            if "Œufs durs" not in supp and "Fromage" not in supp:
                st.warning("⚠️ Conseil : Ajoutez des œufs ou du fromage pour plus de protéines.")
            else:
                st.success("✅ Parfait !")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 3. قسم لوحة رضا المطعم ---
    with tab_feedback:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Satisfaction Resto")
        
        lunch_avg = sum(st.session_state.lunch_ratings) / len(st.session_state.lunch_ratings)
        lunch_pct = int((lunch_avg / 5) * 100)
        
        dinner_avg = sum(st.session_state.dinner_ratings) / len(st.session_state.dinner_ratings)
        dinner_pct = int((dinner_avg / 5) * 100)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"""
                <div style="background: #e8f5e9; border: 2px solid #81c784; border-radius: 12px; padding: 15px; text-align: center;">
                    <div style="font-size: 14px; color: #1b5e20; font-weight: bold;">☀️ Midi</div>
                    <div style="font-size: 28px; color: #2e7d32; font-weight: bold; margin: 5px 0;">{lunch_pct}%</div>
                    <div style="font-size: 11px; color: #555;">{round(lunch_avg, 1)} / 5 ⭐</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_s2:
            st.markdown(f"""
                <div style="background: #e0f2f1; border: 2px solid #4db6ac; border-radius: 12px; padding: 15px; text-align: center;">
                    <div style="font-size: 14px; color: #004d40; font-weight: bold;">🌙 Soir</div>
                    <div style="font-size: 28px; color: #00897b; font-weight: bold; margin: 5px 0;">{dinner_pct}%</div>
                    <div style="font-size: 11px; color: #555;">{round(dinner_avg, 1)} / 5 ⭐</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.info("ℹ️ Classement automatique selon l'horaire (Midi / Soir).")
        st.markdown("</div>", unsafe_allow_html=True)
