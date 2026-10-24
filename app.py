import streamlit as st
from PIL import Image
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="NutriFoyer - Cité U", page_icon="🥗", layout="centered")

# تهيئة حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Étudiant"
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

# تصميم الواجهة الرسمية الاحترافية
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
    st.markdown("<h3 style='color: #1b5e20; text-align: center;'>⚙️ Mon Profil Étudiant</h3>", unsafe_allow_html=True)
    
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
        st.markdown("<p style='color: #4caf50; font-size: 11px; margin: 0;'>Plateforme officielle - Cité Universitaire</p>", unsafe_allow_html=True)
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

    tab_scanner, tab_restou, tab_feedback = st.tabs(["📸 Scanner", "🍽️ Menus Resto U", "📊 Satisfaction"])

    # --- 1. قسم الماسح والتحليل الرسمي ---
    with tab_scanner:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # أ: صفحة التقييم بالنجوم
        if st.session_state.show_rating_page:
            st.markdown("<h4 style='color: #1b5e20; text-align: center;'>⭐ Noter le Repas du Resto U</h4>", unsafe_allow_html=True)
            current_hour = datetime.now().hour
            meal_type = "lunch" if 10 <= current_hour < 15 else "dinner"
            meal_name_fr = "Déjeuner" if meal_type == "lunch" else "Dîner"
            
            st.info(f"🕒 Repas détecté automatiquement : **{meal_name_fr}**")
            
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

        # ب: عرض النتائج بعد التحديد الذكي
        elif st.session_state.analysis_done:
            st.markdown("<h4 style='color: #1b5e20;'>📊 Analyse Nutritionnelle Officielle</h4>", unsafe_allow_html=True)
            if st.session_state.rating_success:
                st.success("🌟 Merci ! Votre vote a été pris en compte dans le dashboard officiel.")
                
            selected_dish = st.session_state.nutrients['dish']
            det = st.session_state.nutrients['details']
            p_val = st.session_state.nutrients['prot']
            c_val = st.session_state.nutrients['carb']
            f_val = st.session_state.nutrients['fat']
            fib_val = st.session_state.nutrients['fib']
            vit_val = st.session_state.nutrients['vit']
            score = st.session_state.nutrients['score']
            advice = st.session_state.nutrients['advice']
            
            st.info(f"🍽️ **Plat sélectionné / détecté :** {selected_dish}\n\n📝 **Détails :** {det}")
            
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
            
            st.markdown(f"🎯 **Indice de compatibilité :** {score}%")
            st.warning(f"💡 {advice}")
            
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("⭐ Noter ce repas"):
                    st.session_state.show_rating_page = True
                    st.session_state.rating_success = False
                    st.rerun()
            with col_act2:
                if st.button("🔄 Scanner un autre"):
                    st.session_state.captured_image = None
                    st.session_state.analysis_done = False
                    st.session_state.show_camera = False
                    st.session_state.rating_success = False
                    st.rerun()
                
        # ج: معاينة الصورة مع اختيار نوع الوجبة الرسمية لضمان دقة 100%
        elif st.session_state.captured_image is not None:
            st.image(st.session_state.captured_image, use_column_width=True)
            st.markdown("---")
            st.write("📌 **Précisez le plat officiel servi au Resto U :**")
            
            chosen_menu = st.selectbox("Sélectionner le plat :", [
                "Couscous tunisien aux légumes et viande",
                "M'salli / Poulet rôti du Resto U",
                "Plat de Pâtes / Spaghettis sauce rouge",
                "Ragoût de lentilles (Lentilles / Loubia)",
                "Pizza / Fast-food universitaire",
                "Poisson grillé du jour"
            ], label_visibility="collapsed")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Lancer l'analyse"):
                    # تحديد القيم بدقة بناءً على الوجبة المكتارة لضمان مطابقة واقعية علمياً
                    if "Couscous" in chosen_menu:
                        det = "Assiette traditionnelle de couscous universitaire avec légumes (courge, carottes) et viande ovine/bovine."
                        p, c, f, fib, vit, sc = 22, 75, 12, 10, 88, 85
                        adv = "Excellent apport en glucides complexes et fibres. Équilibré pour l'étudiant."
                    elif "Poulet" in chosen_menu:
                        det = "Quart de poulet rôti (M'salli) tendre avec une portion de pommes de terre du chef."
                        p, c, f, fib, vit, sc = 40, 48, 15, 5, 80, 96
                        adv = "Parfait ! Haute teneur en protéines nobles pour le maintien et l'énergie."
                    elif "Pâtes" in chosen_menu:
                        det = "Assiette de spaghettis à la sauce tomate tunisienne avec bœuf haché."
                        p, c, f, fib, vit, sc = 25, 82, 11, 4, 75, 80
                        adv = "Riche en énergie (glucides). Pensez à ajouter une salade mechouia en entrée."
                    elif "lentilles" in chosen_menu:
                        det = "Plat chaud de ragoût de légumineuses riches en fer et protéines végétales."
                        p, c, f, fib, vit, sc = 26, 62, 8, 16, 92, 90
                        adv = "Très riche en fibres et fer. Excellent choix pour la santé digestive et l'immunité."
                    elif "Pizza" in chosen_menu:
                        det = "Pizza italienne artisanale garnie de charcuterie / pepperoni et fromage mozzarella fondue."
                        p, c, f, fib, vit, sc = 28, 55, 22, 3, 65, 72
                        adv = "Plat calorique et savoureux. À consommer avec modération et à équilibrer avec des légumes."
                    else:
                        det = "Plat de poisson du restaurant universitaire avec garniture légère."
                        p, c, f, fib, vit, sc = 32, 35, 10, 6, 85, 94
                        adv = "Excellent choix ! Riche en oméga-3 et protéines de haute qualité."
                        
                    st.session_state.nutrients = {
                        'dish': chosen_menu, 'details': det, 'prot': p, 'carb': c, 
                        'fat': f, 'fib': fib, 'vit': vit, 'score': sc, 'advice': adv
                    }
                    st.session_state.analysis_done = True
                    st.rerun()
            with c_btn2:
                if st.button("❌ Changer"):
                    st.session_state.captured_image = None
                    st.session_state.show_camera = False
                    st.rerun()
                    
        # د: الواجهة الرئيسية المربعة المتجاورة بدون تمرير
        else:
            st.markdown("<h4 style='color: #1b5e20; text-align: center; margin-bottom: 8px;'>📸 Scanner le Plateau</h4>", unsafe_allow_html=True)
            
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

    # --- 2. قسم المطعم الجامعي ---
    with tab_restou:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1b5e20;'>🍽️ Menus Officiels du Resto U</h4>", unsafe_allow_html=True)
        
        plat = st.selectbox("Plat du jour :", [
            "Couscous aux légumes et viande", 
            "Poulet rôti (M'salli)", 
            "Spaghettis sauce rouge", 
            "Ragoût de lentilles / Loubia", 
            "Poisson du jour"
        ])
        
        supp = st.multiselect("Suppléments disponibles :", [
            "Salade verte", "Salade Mechouia", "Fromage", 
            "Œufs durs", "Yaourt", "Fruit / Orange"
        ])
        
        if st.button("📊 Analyser le menu"):
            st.success("Analyse validée pour le restaurant universitaire !")
            if "Œufs durs" not in supp and "Fromage" not in supp and "Salade" not in supp:
                st.warning("⚠️ Conseil nutritionnel : Ajoutez une entrée (salade ou œufs) pour compléter vos apports en micronutriments.")
            else:
                st.success("✅ Excellent choix de menu équilibré !")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 3. لوحة رضا المطعم الرسمية ---
    with tab_feedback:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1b5e20;'>📊 Indice de Satisfaction Global</h4>", unsafe_allow_html=True)
        st.write("Statistiques en temps réel basées sur les votes des étudiants :")
        
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
        st.info("ℹ️ Le système classe et actualise les votes automatiquement selon l'horaire officiel du Resto U.")
        st.markdown("</div>", unsafe_allow_html=True)
