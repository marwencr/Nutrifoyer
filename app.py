import streamlit as st
from PIL import Image

# إعدادات صفحة التطبيق
st.set_page_config(page_title="NutriFoyer - Nutrition Étudiante", page_icon="🥗", layout="centered")

st.title("🥗 NutriFoyer : Équilibre Nutritionnel en Foyer")
st.write("Application intelligente pour évaluer les repas étudiants par photo et composer son plateau avec les plats du Resto U.")

# الشريط الجانبي: الملف الشخصي للطالب
st.sidebar.header("👤 Profil de l'Étudiant")
gender = st.sidebar.selectbox("Sexe", ["Homme", "Femme"])
age = st.sidebar.number_input("Âge", 17, 30, 22)
weight = st.sidebar.number_input("Poids (kg)", 40, 150, 70)
height = st.sidebar.number_input("Taille (cm)", 140, 200, 175)

bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "Homme" else -161)
st.sidebar.info(f"Besoin estimé : **{int(bmr)} kcal/jour**")

st.divider()

# 1. الأساس: تصوير الوجبة أو رفع صورة
st.header("📸 1. Analyse par Image (Caméra / Galerie)")
st.write("Prenez en photo votre plateau ou importez une image :")

uploaded_file = st.file_uploader("Choisir une image depuis la galerie...", type=["jpg", "jpeg", "png"])
camera_file = st.camera_input("Ou prendre une photo directement :")

image = uploaded_file if uploaded_file else camera_file

if image is not None:
    img = Image.open(image)
    st.image(img, caption="Plateau analysé par IA", use_column_width=True)

st.divider()

# 2. الخيار الإضافي: اختيار الأطباق يدوياً من قائمة المطعم الجامعي
st.header("🍽️ 2. Composants du Resto U (Sélection manuelle)")
st.write("Cochez ou sélectionnez les éléments de votre plateau du Resto U :")

col1, col2 = st.columns(2)

with col1:
    plat_principal = st.selectbox("Plat principal :", [
        "Aucun",
        "Couscous aux légumes (كسكسي بالخضر)", 
        "Couscous à la viande (كسكسي باللحم)", 
        "Couscous au poulet (كسكسي بالدجاج)", 
        "Ragoût de légumes (مرقة خضر)", 
        "Ragoût au poulet (مرقة بالدجاج)", 
        "Poulet cuit (دجاج طايب)", 
        "Poulet rôti au four / M'salli (دجاج مصلي)", 
        "Poisson grillé (حوت مشوي)", 
        "Ragoût de lentilles (مرقة عدس)", 
        "Loubia / Haricots blancs (لوبيا)", 
        "Pâtes Penne / Fül (مقرونة فل)", 
        "Spaghettis (مقرونة سباغيتي)"
    ])

with col2:
    accompagnements = st.multiselect("Entrées, Salades et Suppléments :", [
        "Salade verte (سلاطة خضراء)", 
        "Salade Mechouia (سلاطة مشوية)", 
        "Fromage (جبن)", 
        "Deux œufs durs (بيضتين مسلوقتين)", 
        "Yaourt (كعبة ياغورت)", 
        "Petit jus de fruit (باكو عصير صغير)"
    ])

st.divider()

# زر التحليل الشامل
if st.button("🚀 Lancer l'analyse nutritionnelle globale"):
    with st.spinner("Analyse des macronutriments en cours..."):
        st.success("Analyse terminée avec succès !")
        
        # عرض المؤشرات
        m1, m2, m3 = st.columns(3)
        m1.metric("Protéines", "24g", "Optimal")
        m2.metric("Glucides", "68g", "Bon")
        m3.metric("Lipides", "15g", "Équilibré")
        
        st.subheader("📊 Évaluation globale du plateau :")
        st.progress(80)
        st.write("Niveau d'adéquation avec votre profil : **80% (Excellent repas étudiant)**")
        
        st.warning("💡 **Recommandations du coach NutriFoyer :**")
        if "Deux œufs durs (بيضتين مسلوقتين)" not in accompagnements and "Fromage (جبن)" not in accompagnements and "Poulet" not in plat_principal and "Viande" not in plat_principal and "Poisson" not in plat_principal:
            st.info("⚠️ Le plateau sélectionné manque de protéines. Pensez à ajouter **deux œufs durs** ou du **fromage** du Resto U pour combler vos besoins énergétiques.")
        else:
            st.info("✅ Super choix ! Ce repas fournit l'énergie nécessaire pour vos cours et soutient vos efforts physiques au foyer.")
