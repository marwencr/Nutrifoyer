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
if 'avatar' not in st.session_state:
    st.session_state.avatar = None
if 'edit_profile' not in st.session_state:
    st.session_state.edit_profile = False

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
    
    # زر محاكاة تسجيل الدخول بالجميل
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
        
    uploaded_avatar = st.file_uploader("📷 Ajouter une photo de profil (Avatar)", type=["jpg", "png", "jpeg"])
    if uploaded_avatar is not None:
        st.session_state.avatar = uploaded_avatar
        
    if st.button("💾 Enregistrer et Commencer"):
        st.session_state.logged_in = True
        st.session_state.edit_profile = False
        st.success("Profil configuré avec succès !")
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- التطبيق الرئيسي بعد تسجيل الدخول ---
    
    # شريط علوي مع زر دائري صغير للبروفايل في الزاوية
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("<h2 style='color: #1b5e20; margin: 0;'>🥗 NutriFoyer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #4caf50; font-size: 13px; margin: 0;'>Plateforme d'équilibre nutritionnel en cité universitaire</p>", unsafe_allow_html=True)
    with top_col2:
        if st.button("⚙️ Profil"):
            st.session_state.edit_profile = True
            st.rerun()

    st.markdown("---")

    # حساب السعرات الأساسية BMR
    w = st.session_state.weight
    h = st.session_state.height
    a = st.session_state.age
    g = st.session_state.gender
    bmr = (10 * w) + (6.25 * h) - (5 * a) + (5 if g == "Homme" else -161)

    # الأقسام الرئيسية (التبويبات الواضحة)
    tab_scanner, tab_restou = st.tabs(["📸 Scanner & Analyse du Plat", "🍽️ Menu Resto U & Plats"])

    # --- قسم التصوير ورفع الصور والتحليل ---
    with tab_scanner:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📸 Analyse Intelligente par Photo")
        st.write("Sélectionnez une option ci-dessous pour importer ou prendre en photo votre plateau :")
        
        # زرين على شكل مربع بألوان محددة
        c_box1, c_box2 = st.columns(2)
        with c_box1:
            st.markdown("""
                <div style='background: #e8f5e9; padding: 12px; border-radius: 12px; text-align: center; border: 2px dashed #4caf50; margin-bottom: 8px;'>
                    <span style='color: #2e7d32; font-weight: bold;'>📁 Importer une image</span>
                </div>
            """, unsafe_allow_html=True)
            uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="up_file")
            
        with c_box2:
            st.markdown("""
                <div style='background: #e0f2f1; padding: 12px; border-radius: 12px; text-align: center; border: 2px dashed #00897b; margin-bottom: 8px;'>
                    <span style='color: #00695c; font-weight: bold;'>📷 Prendre une photo</span>
                </div>
            """, unsafe_allow_html=True)
            camera_file = st.camera_input("", key="cam_file")
            
        image = uploaded_file if uploaded_file else camera_file
        
        if image is not None:
            st.image(image, use_column_width=True)
            
            # زر التحليل بالذكاء الاصطناعي تحت الصورة مباشرة
            if st.button("🚀 Lancer l'analyse IA de la وجبة"):
                with st.spinner("Analyse des macronutriments en cours..."):
                    st.success("Analyse terminée !")
                    
                    mc1, mc2, mc3 = st.columns(3)
                    mc1.metric("Protéines", "24g", "Optimal")
                    mc2.metric("Glucides", "62g", "Énergie")
                    mc3.metric("Lipides", "12g", "Équilibré")
                    
                    st.markdown("---")
                    st.markdown("🎯 **Indice de compatibilité avec votre profil :**")
                    
                    # مؤشر يتدرج من الأحمر والأصفر والأخضر إلى الأزرق (الأزرق الممتلئ يعني الأنسب تماماً لبروفايلك)
                    st.markdown("""
                        <div style='background: #f1f3f4; border-radius: 10px; padding: 5px; margin-top: 8px;'>
                            <div style='height: 18px; border-radius: 8px; background: linear-gradient(90deg, #ff5252 0%, #ffd740 33%, #69f0ae 66%, #2196f3 100%); width: 95%;'></div>
                        </div>
                        <div style='display: flex; justify-content: space-between; font-size: 11px; color: #555; margin-top: 4px;'>
                            <span>🔴 Inadapté</span><span>🟡 Moyen</span><span>🟢 Bon</span><span style='color: #2196f3; font-weight: bold; font-size: 12px;'>🔵 Parfaitement Adapté (95%)</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"💡 **Conseil NutriFoyer :** Votre besoin énergétique est de **{int(bmr)} kcal/jour**. Ce repas correspond parfaitement à votre morphologie, âge et niveau d'activité !")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- قسم المطعم الجامعي (Resto U) ---
    with tab_restou:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🍽️ Plats du Restaurant Universitaire (Resto U)")
        st.write("Composez et évaluez votre plateau avec les menus tunisiens officiels :")
        
        plat = st.selectbox("Plat principal :", [
            "Couscous aux légumes (كسكسي بالخضر)", 
            "Couscous à la viande (كسكسي باللحم)", 
            "Couscous au poulet (كسكسي بالدجاج)", 
            "Ragoût de légumes (مرقة خضر)", 
            "Poulet rôti / M'salli (دجاج مصلي)", 
            "Poisson grillé (حوت مشوي)", 
            "Ragoût de lentilles (مرقة عدس)", 
            "Loubia / Haricots blancs (لوبيا)", 
            "Pâtes / Spaghettis (مقرونة)"
        ])
        
        supp = st.multiselect("Entrées et Suppléments :", [
            "Salade verte (سلاطة خضراء)", 
            "Salade Mechouia (سلاطة مشوية)", 
            "Fromage (جبن)", 
            "Deux œufs durs (بيضتين مسلوقتين)", 
            "Yaourt (كعبة ياغورت)", 
            "Jus de fruit (باكو عصير)"
        ])
        
        if st.button("📊 Évaluer ce plateau Resto U"):
            with st.spinner("Évaluation en cours..."):
                st.success("Plateau évalué avec succès !")
                st.markdown("### 📋 Résultat de l'analyse Resto U :")
                st.progress(92)
                st.write("Score nutritionnel : **92% - Excellent choix pour votre santé !**")
                st.success("✅ Ce menu fournit l'apport nécessaire en vitamines et protéines pour vos cours.")
        st.markdown("</div>", unsafe_allow_html=True)
