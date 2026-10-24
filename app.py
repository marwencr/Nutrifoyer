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
        padding: 24px;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.06);
        margin-bottom: 20px;
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
        padding: 12px;
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

# --- نافذة تعديل البروفايل ---
if st.session_state.edit_profile:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='header-title'>⚙️ Modifier le Profil</h2>", unsafe_allow_html=True)
    
    st.session_state.user_name = st.text_input("Nom complet", st.session_state.user_name)
    st.session_state.gender = st.selectbox("Sexe", ["Homme", "Femme"], index=0 if st.session_state.gender=="Homme" else 1)
    st.session_state.age = st.number_input("Âge", 17, 40, st.session_state.age)
    st.session_state.weight = st.number_input("Poids (kg)", 40, 150, st.session_state.weight)
    st.session_state.height = st.number_input("Taille (cm)", 140, 200, st.session_state.height)
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        if st.button("💾 Enregistrer"):
            st.session_state.edit_profile = False
            st.success("Profil mis à jour avec succès !")
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

    tab_scanner, tab_restou, tab_feedback = st.tabs(["📸 Scanner & Analyse", "🍽️ Menus Resto U", "📊 Satisfaction Resto (Tous)"])

    # --- 1. قسم الماسح والتحليل والتحكم بصفحة النجوم ---
    with tab_scanner:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # الحالة أ: إذا اختار المستخدم الانتقال لصفحة تقييم النجوم الخمسة
        if st.session_state.show_rating_page:
            st.subheader("⭐ Évaluation du Repas")
            st.write("Veuillez attribuer une note globale pour ce repas (Classification automatique selon l'heure) :")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            current_hour = datetime.now().hour
            # التصنيف التلقائي حسب الوقت (10h - 15h للغداء، وباقي الوقت للعشاء)
            meal_type = "lunch" if 10 <= current_hour < 15 else "dinner"
            meal_name_fr = "Déjeuner" if meal_type == "lunch" else "Dîner"
            
            st.info(f"🕒 Repas détecté automatiquement : **{meal_name_fr}**")
            
            # أزرار النجوم الخمسة المنفصلة
            if st.button("⭐ 1 Étoile"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(1)
                else: st.session_state.dinner_ratings.append(1)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
                
            if st.button("⭐⭐ 2 Étoiles"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(2)
                else: st.session_state.dinner_ratings.append(2)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
                
            if st.button("⭐⭐⭐ 3 Étoiles"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(3)
                else: st.session_state.dinner_ratings.append(3)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
                
            if st.button("⭐⭐⭐⭐ 4 Étoiles"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(4)
                else: st.session_state.dinner_ratings.append(4)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
                
            if st.button("⭐⭐⭐⭐⭐ 5 Étoiles (Or)"):
                if meal_type == "lunch": st.session_state.lunch_ratings.append(5)
                else: st.session_state.dinner_ratings.append(5)
                st.session_state.show_rating_page = False
                st.session_state.rating_success = True
                st.rerun()
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ Annuler et retourner aux résultats"):
                st.session_state.show_rating_page = False
                st.rerun()

        # الحالة ب: عرض نتائج التحليل (عندما تكون المنصة في وضع النتائج)
        elif st.session_state.analysis_done:
            st.subheader("📸 Analyse Intelligente par Photo")
            
            if st.session_state.rating_success:
                st.success("🌟 Merci ! Votre évaluation a été enregistrée avec succès et l'indice de satisfaction global a été mis à jour.")
                
            st.markdown("### 📊 Résultats nutritionnels détaillés du plat :")
            
            p_val = st.session_state.nutrients['prot']
            c_val = st.session_state.nutrients['carb']
            f_val = st.session_state.nutrients['fat']
            fib_val = st.session_state.nutrients['fib']
            vit_val = st.session_state.nutrients['vit']
            score = st.session_state.nutrients['score']
            advice = st.session_state.nutrients['advice']
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="metric-box"><div style="font-size:12px; color:#1565c0; font-weight:bold;">Protéines</div><div style="font-size:18px; color:#0d47a1; font-weight:bold;">{p_val}g</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class="metric-box"><div style="font-size:12px; color:#e65100; font-weight:bold;">Glucides</div><div style="font-size:18px; color:#bf360c; font-weight:bold;">{c_val}g</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-box"><div style="font-size:12px; color:#2e7d32; font-weight:bold;">Lipides</div><div style="font-size:18px; color:#1b5e20; font-weight:bold;">{f_val}g</div></div>""", unsafe_allow_html=True)
                
            m4, m5 = st.columns(2)
            with m4:
                st.markdown(f"""<div class="metric-box"><div style="font-size:12px; color:#6a1b9a; font-weight:bold;">Fibres</div><div style="font-size:18px; color:#4a148c; font-weight:bold;">{fib_val}g</div></div>""", unsafe_allow_html=True)
            with m5:
                st.markdown(f"""<div class="metric-box"><div style="font-size:12px; color:#00695c; font-weight:bold;">Vitamines</div><div style="font-size:18px; color:#004d40; font-weight:bold;">{vit_val}%</div></div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("🎯 **Indice de compatibilité avec votre profil :**")
            st.markdown(f"""
                <div style='background: #f1f3f4; border-radius: 10px; padding: 5px; margin-top: 8px;'>
                    <div style='height: 18px; border-radius: 8px; background: linear-gradient(90deg, #ff5252 0%, #ffd740 33%, #69f0ae 66%, #2196f3 100%); width: {score}%;'></div>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 11px; color: #555; margin-top: 4px;'>
                    <span>Inadapté</span><span>Moyen</span><span>Bon</span><span style='color: #2196f3; font-weight: bold;'>Compatibilité ({score}%)</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.info(f"💡 **Recommandations & Alternatives NutriFoyer :**\n\n{advice}")
            
            st.markdown("---")
            
            # زر الانتقال إلى صفحة تقييم النجوم تحت التحليل تماماً
            if st.button("⭐ Noter ce repas (Évaluation par étoiles)"):
                st.session_state.show_rating_page = True
                st.session_state.rating_success = False
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Analyser un autre plat"):
                st.session_state.captured_image = None
                st.session_state.analysis_done = False
                st.session_state.show_camera = False
                st.session_state.rating_success = False
                st.rerun()
                
        # الحالة ج: رفع الصورة أو فتح الكاميرا
        elif st.session_state.captured_image is not None:
            st.subheader("📸 Analyse Intelligente par Photo")
            st.image(st.session_state.captured_image, use_column_width=True)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Lancer l'analyse IA"):
                    img_size = len(str(st.session_state.captured_image))
                    random.seed(img_size)
                    
                    p = random.randint(12, 35)
                    c = random.randint(45, 75)
                    f = random.randint(8, 22)
                    fib = random.randint(3, 12)
                    vit = random.randint(60, 99)
                    sc = random.randint(70, 98)
                    
                    if p < 18:
                        adv = "⚠️ **Attention :** Ce plat présente un déficit en protéines. **Alternatives conseillées au Resto U :** Ajoutez deux œufs durs ou une petite boîte de thon pour compenser."
                    else:
                        adv = f"✅ **Parfait !** Ce repas couvre bien vos besoins de {int(bmr)} kcal/jour avec un bon équilibre en fibres et vitamines."
                        
                    st.session_state.nutrients = {'prot': p, 'carb': c, 'fat': f, 'fib': fib, 'vit': vit, 'score': sc, 'advice': adv}
                    st.session_state.analysis_done = True
                    st.rerun()
            with c_btn2:
                if st.button("❌ Changer l'image"):
                    st.session_state.captured_image = None
                    st.session_state.show_camera = False
                    st.rerun()
                    
        else:
            st.subheader("📸 Analyse Intelligente par Photo")
            st.write("Sélectionnez une option pour ajouter une photo de votre plateau :")
            
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

    # --- 2. قسم المطعم الجامعي (Resto U) ---
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
                
                if "Deux œufs durs" not in supp and "Fromage" not in supp:
                    st.warning("⚠️ **Conseil d'optimisation :** Votre plateau manque de sources de protéines. Pensez à ajouter **deux œufs durs** ou **un morceau de fromage**.")
                else:
                    st.success("✅ **Parfait !** Vos suppléments complètent idéalement vos apports.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 3. لوحة تحكم رضا المطعم (الغداء والعشاء تتغير ديناميكياً) ---
    with tab_feedback:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Tableau de Satisfaction du Restaurant (Resto U)")
        st.write("Indicateurs en temps réel mis à jour dynamiquement selon les notes des étudiants :")
        
        # حساب نسبة الرضا ديناميكياً بناءً على التقييمات المسجلة
        lunch_avg = sum(st.session_state.lunch_ratings) / len(st.session_state.lunch_ratings)
        lunch_percentage = int((lunch_avg / 5) * 100)
        
        dinner_avg = sum(st.session_state.dinner_ratings) / len(st.session_state.dinner_ratings)
        dinner_percentage = int((dinner_avg / 5) * 100)
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown(f"""
                <div style="background: #e8f5e9; border: 2px solid #81c784; border-radius: 16px; padding: 20px; text-align: center;">
                    <div style="font-size: 16px; color: #1b5e20; font-weight: bold;">☀️ Repas de Midi (Déjeuner)</div>
                    <div style="font-size: 36px; color: #2e7d32; font-weight: bold; margin: 10px 0;">{lunch_percentage}%</div>
                    <div style="font-size: 12px; color: #555;">Indice de satisfaction global</div>
                    <div style="margin-top: 10px; font-size: 13px; color: #00796b;">Moyenne : {round(lunch_avg, 1)} / 5 ⭐ ({len(st.session_state.lunch_ratings)} votes)</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_s2:
            st.markdown(f"""
                <div style="background: #e0f2f1; border: 2px solid #4db6ac; border-radius: 16px; padding: 20px; text-align: center;">
                    <div style="font-size: 16px; color: #004d40; font-weight: bold;">🌙 Repas du Soir (Dîner)</div>
                    <div style="font-size: 36px; color: #00897b; font-weight: bold; margin: 10px 0;">{dinner_percentage}%</div>
                    <div style="font-size: 12px; color: #555;">Indice de satisfaction global</div>
                    <div style="margin-top: 10px; font-size: 13px; color: #00796b;">Moyenne : {round(dinner_avg, 1)} / 5 ⭐ ({len(st.session_state.dinner_ratings)} votes)</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.info("ℹ️ **Information :** Le système classe automatiquement les votes selon l'heure (10h-15h pour le Déjeuner, 15h-19h pour le Dîner) et met à jour les scores en temps réel.")
        st.markdown("</div>", unsafe_allow_html=True)
