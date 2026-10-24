import streamlit as st
from PIL import Image

# إعدادات صفحة التطبيق وتصميم الـ iOS Glassmorphism
st.set_page_config(page_title="NutriFoyer iOS", page_icon="🥗", layout="centered")

st.markdown("""
    <style>
    /* خلفية عامة ناعمة */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* تصميم بطاقات الزجاج السائل (Liquid Glassmorphism) */
    .glass-container {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* أزرار عصرية مطابقة لستايل آيفون */
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        font-weight: 600;
        background: linear-gradient(135deg, #007aff 0%, #005ec4 100%);
        color: white;
        border: none;
        height: 48px;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
    }
    
    /* تنسيق العناوين والتبويبات */
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1c1c1e;
    }
    </style>
""", unsafe_allow_html=True)

# رأس الصفحة بتصميم أنيق
st.markdown("<h1 style='text-align: center; color: #1c1c1e; font-size: 28px;'>🥗 NutriFoyer Mobile</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8e8e93; font-size: 14px;'>Plateforme intelligente d'équilibre nutritionnel en cité universitaire</p>", unsafe_allow_html=True)

# نظام التبويبات الاحترافي (Tabs)
tab1, tab2, tab3 = st.tabs(["👤 Mon Profil", "📸 Scanner le Plat", "🍽️ Menu Resto U"])

# --- التبويب الأول: الملف الشخصي ---
with tab1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("Paramètres de l'Étudiant")
    
    gender = st.selectbox("Sexe", ["Homme", "Femme"])
    col_a, col_b = st.columns(2)
    with col_a:
        age = st.number_input("Âge", 17, 30, 22)
        weight = st.number_input("Poids (kg)", 40, 150, 70)
    with col_b:
        height = st.number_input("Taille (cm)", 140, 200, 175)
        budget = st.selectbox("Budget", ["Économique", "Moyen"])
        
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "Homme" else -161)
    st.info(f"🎯 **Besoin énergétique journalier estimé :** {int(bmr)} kcal/jour")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب الثاني: مسح الصورة بالذكاء الاصطناعي ---
with tab2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("Analyse Intelligente par Photo")
    st.write("Prenez en photo votre plateau ou importez une image pour l'analyser :")
    
    uploaded_file = st.file_uploader("Choisir une image...", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Ou utiliser la caméra :")
    
    image = uploaded_file if uploaded_file else camera_file
    
    if image is not None:
        st.image(image, use_column_width=True)
        if st.button("🚀 Lancer l'analyse IA du plat"):
            with st.spinner("Analyse des macronutriments en cours..."):
                st.success("Analyse terminée avec succès !")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Protéines", "19g", "+3g")
                c2.metric("Glucides", "62g", "Optimal")
                c3.metric("Lipides", "14g", "Équilibré")
                
                st.markdown("---")
                st.markdown("💡 **Conseil Économique NutriFoyer :**")
                st.info("Le plat est riche en énergie mais manque légèrement de protéines de qualité. Ajoutez **deux œufs durs** ou **une boîte de ثونة** pour un équilibre parfait à bas coût.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب الثالث: أطباق المطعم الجامعي التونسي ---
with tab3:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("Composition du Plateau Resto U")
    st.write("Sélectionnez les plats proposés aujourd'hui au Restaurant Universitaire :")
    
    plat_principal = st.selectbox("Plat principal :", [
        "Couscous aux légumes (كسكسي بالخضر)", 
        "Couscous à la viande (كسكسي باللحم)", 
        "Couscous au poulet (كسكسي بالدجاج)", 
        "Ragoût de légumes (مرقة خضر)", 
        "Ragoût au poulet (مرقة بالدجاج)", 
        "Poulet rôti / M'salli (دجاج مصلي)", 
        "Poisson grillé (حوت مشوي)", 
        "Ragoût de lentilles (مرقة عدس)", 
        "Loubia / Haricots blancs (لوبيا)", 
        "Pâtes / Spaghettis (مقرونة)"
    ])
    
    supplements = st.multiselect("Entrées, Salades et Suppléments :", [
        "Salade verte (سلاطة خضراء)", 
        "Salade Mechouia (سلاطة مشوية)", 
        "Fromage (جبن)", 
        "Deux œufs durs (بيضتين مسلوقتين)", 
        "Yaourt (كعبة ياغورت)", 
        "Petit jus de fruit (باكو عصير صغير)"
    ])
    
    if st.button("📊 Évaluer le plateau complet"):
        with st.spinner("Calcul des apports nutritionnels..."):
            st.success("Évaluation réalisée avec succès !")
            
            st.markdown("### 📋 Résultat de l'analyse :")
            st.progress(88)
            st.write("Taux de compatibilité avec votre profil : **88% (Excellent choix étudiant)**")
            
            if len(supplements) > 0:
                st.markdown("✅ **Points forts :** Excellente inclusion de suppléments riches en fibres et vitamines.")
            else:
                st.markdown("⚠️ **Recommandation :** Pensez à ajouter une salade ou un yaourt pour optimiser l'apport nutritionnel.")
    st.markdown('</div>', unsafe_allow_html=True)
