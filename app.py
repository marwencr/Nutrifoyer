import streamlit as st
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="NutriFoyer", page_icon="🥗", layout="centered")

# تهيئة حالة الجلسة (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Marwan"
if 'user_email' not in st.session_state:
    st.session_state.user_email = "marwan@student.tn"
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

# حالات الماسح الضوئي والصورة
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

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
        padding: 24px;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.06);
        margin-bottom: 20px;
    }
    .header-title {
        color: #1b5e20;
        font-weight: 700;
        text-align: center;
    }
    /* مربعات المكونات الغذائية الملونة */
    .metric-box-protein {
        background: #e3f2fd;
        border: 1px solid #90caf9;
        border-radius: 14px;
        padding: 15px;
        text-align: center;
    }
    .metric-box-carbs {
        background: #fff3e0;
        border: 1px solid #ffe0b2;
        border-radius: 14px;
        padding: 15px;
        text-align: center;
    }
    .metric-box-fats {
        background: #e8f5e9;
        border: 1px solid #c8e6c9;
        border-radius: 14px;
        padding: 15px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        background-color: #2e7d32;
        color: white;
        border: none;
        height: 48px;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. شاشة تسجيل الدخول والبروفايل الأولي ---
if not st.session_state.logged_in or st.session_state.edit_profile:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='header-title'>🌿 Bienvenue sur NutriFoyer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Connectez-vous pour configurer votre profil nutritionnel étudiant</p>", unsafe_allow_html=True)
    
    if st.button("🔵 Connexion rapide avec Google (Gmail)"):
        st.session_state.logged_in = True
        st.session_state.edit_profile = False
        st.rerun()
        
    st.markdown("---")
    st.subheader("👤 Informations Personnelles & Profil")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_name = st.text_input("Nom complet", st.session_state.user_name)
        st.session_state.gender = st.selectbox("Sexe", ["Homme", "Femme"], index=0 if st.session_state.gender=="Homme" else 1)
        st.session_state.age = st.number_input("Âge", 17, 40, st.session_state.age)
    with col2:
        st.session_state.user_email = st.text_input("Email universitaire", st.session_state.user_email)
        st.session_state.weight = st.number_input("Poids (kg)", 40, 150, st.session_state.weight)
        st.session_state.height = st.number_input("Taille (cm)", 140, 200, st.session_state.height)
        
    if st.button("💾 Enregistrer et Commencer"):
        st.session_state.logged_in = True
        st.session_state.edit_profile = False
        st.success("Profil configuré avec succès !")
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- التطبيق الرئيسي بعد تسجيل الدخول ---
    
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("<h2 style='color: #1b5e20; margin: 0;'>🥗 NutriFoyer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #4caf50; font-size: 13px; margin: 0;'>Plateforme d'équilibre nutritionnel en cité universitaire</p>", unsafe_allow_html=True)
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

    tab_scanner, tab_restou = st.tabs(["📸 Scanner & Analyse du Plat", "🍽️ Menu Resto U & Plats"])

    # --- قسم التصوير ورفع الصور والتحليل (محدث بالكامل حسب طلبك) ---
    with tab_scanner:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📸 Analyse Intelligente par Photo")
        
        # الحالة 3: إذا ظهر تحليل المعلومات (تختفي الصورة وأزرار الاختيار)
        if st.session_state.analysis_done:
            st.success("Analyse terminée avec succès !")
            st.markdown("### 📊 Résultats nutritionnels du plat :")
            
            # عرض المكونات في مربعات ملونة بجانب بعضها
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown("""
                    <div class="metric-box-protein">
                        <div style="font-size: 13px; color: #1565c0; font-weight: bold;">Protéines</div>
                        <div style="font-size: 22px; color: #0d47a1; font-weight: bold;">24g</div>
                        <div style="font-size: 11px; color: #1976d2;">Optimal</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown("""
                    <div class="metric-box-carbs">
                        <div style="font-size: 13px; color: #e65100; font-weight: bold;">Glucides</div>
                        <div style="font-size: 22px; color: #bf360c; font-weight: bold;">62g</div>
                        <div style="font-size: 11px; color: #f57c00;">Énergie</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_m3:
                st.markdown("""
                    <div class="metric-box-fats">
                        <div style="font-size: 13px; color: #2e7d32; font-weight: bold;">Lipides</div>
                        <div style="font-size: 22px; color: #1b5e20; font-weight: bold;">12g</div>
                        <div style="font-size: 11px; color: #388e3c;">Équilibré</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("🎯 **Indice de compatibilité avec votre profil :**")
            st.markdown("""
                <div style='background: #f1f3f4; border-radius: 10px; padding: 5px; margin-top: 8px;'>
                    <div style='height: 18px; border-radius: 8px; background: linear-gradient(90deg, #ff5252 0%, #ffd740 33%, #69f0ae 66%, #2196f3 100%); width: 95%;'></div>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 11px; color: #555; margin-top: 4px;'>
                    <span>Inadapté</span><span>Moyen</span><span>Bon</span><span style='color: #2196f3; font-weight: bold;'>Parfaitement Adapté (95%)</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.info(f"💡 **Conseil NutriFoyer :** Votre besoin énergétique est de {int(bmr)} kcal/jour. Ce repas correspond parfaitement à votre morphologie et profil !")
            
            if st.button("🔄 Analyser un autre plat"):
                st.session_state.captured_image = None
                st.session_state.analysis_done = False
                st.session_state.show_camera = False
                st.rerun()
                
        # الحالة 2: عندما تصبح الصورة أمامك (تختفي أزرار الكاميرا والتحميل ويظهر زر التحليل)
        elif st.session_state.captured_image is not None:
            st.image(st.session_state.captured_image, use_column_width=True)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Lancer l'analyse IA"):
                    st.session_state.analysis_done = True
                    st.rerun()
            with c_btn2:
                if st.button("❌ Changer l'image"):
                    st.session_state.captured_image = None
                    st.session_state.show_camera = False
                    st.rerun()
                    
        # الحالة 1: البداية (اختيار إما رفع صورة أو فتح الكاميرا بالضغط على الزر)
        else:
            st.write("Sélectionnez une option pour ajouter une photo :")
            
            uploaded_file = st.file_uploader("Importer une image depuis l'appareil", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                st.session_state.captured_image = uploaded_file
                st.rerun()
            
            st.markdown("<div style='text-align: center; margin: 10px 0; color: #666;'>— OU —</div>", unsafe_allow_html=True)
            
            if not st.session_state.show_camera:
                if st.button("📷 Ouvrir la caméra"):
                    st.session_state.show_camera = True
                    st.rerun()
            else:
                st.markdown("### Prenez la photo :")
                camera_file = st.camera_input("Prendre une photo")
                if camera_file is not None:
                    st.session_state.captured_image = camera_file
                    st.session_state.show_camera = False
                    st.rerun()
                if st.button("Fermer la caméra"):
                    st.session_state.show_camera = False
                    st.rerun()
                    
        st.markdown("</div>", unsafe_allow_html=True)

    # --- قسم المطعم الجامعي (Resto U) ---
    with tab_restou:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🍽️ Plats du Restaurant Universitaire (Resto U)")
        st.write("Composez et évaluez votre plateau avec les menus tunisiens officiels :")
        
        plat = st.selectbox("Plat principal :", [
            "Couscous aux légumes", 
            "Couscous à la viande", 
            "Couscous au poulet", 
            "Ragoût de légumes", 
            "Poulet rôti / M'salli", 
            "Poisson grillé", 
            "Ragoût de lentilles", 
            "Loubia / Haricots blancs", 
            "Pâtes / Spaghettis"
        ])
        
        supp = st.multiselect("Entrées et Suppléments :", [
            "Salade verte", 
            "Salade Mechouia", 
            "Fromage", 
            "Deux œufs durs", 
            "Yaourt", 
            "Jus de fruit"
        ])
        
        if st.button("📊 Évaluer ce plateau Resto U"):
            with st.spinner("Évaluation en cours..."):
                st.success("Plateau évalué avec succès !")
                st.markdown("### 📋 Résultat de l'analyse Resto U :")
                st.progress(92)
                st.write("Score nutritionnel : **92% - Excellent choix pour votre santé !**")
                st.success("Ce menu fournit l'apport nécessaire en vitamines et protéines pour vos cours.")
        st.markdown("</div>", unsafe_allow_html=True)
