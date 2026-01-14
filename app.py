import streamlit as st
import os
import shutil
from resume_matcher.resume_parser import load_resumes
from resume_matcher.matcher import rank_resumes
from resume_matcher.explainer import generate_explanation

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Smart Resume Matcher",
    page_icon="🎯",
    layout="wide"
)

# Petit CSS uniquement pour nettoyer les marges (le reste est natif)
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- 2. GESTION DE L'ÉTAT (SESSION STATE) ---
# Cela permet de garder les résultats en mémoire même si on clique sur un bouton
if 'results' not in st.session_state:
    st.session_state.results = None
if 'ai_analyses' not in st.session_state:
    st.session_state.ai_analyses = {}

# Fonction pour nettoyer le dossier uploads
def clear_upload_folder():
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")
    os.makedirs("uploads")

# --- 3. SIDEBAR (UPLOAD) ---
with st.sidebar:
    st.title("📂 Control Panel")
    uploaded_files = st.file_uploader(
        "Upload PDF Resumes", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    st.divider()
    
    # Indicateur visuel simple
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} resumes loaded")
    else:
        st.info("Waiting for files...")

# --- 4. ZONE PRINCIPALE (INPUT) ---
st.title("🎯 Smart Resume Matcher")
st.markdown("### Find the perfect candidate using AI Vectors")

# Zone de description du poste
job_description = st.text_area(
    "Paste the Job Description here:",
    height=150,
    placeholder="Example: We are looking for a Python Data Scientist with 3 years of experience..."
)

# Bouton d'action principal
# On utilise use_container_width pour qu'il prenne toute la largeur
if st.button("🚀 Analyze Candidates", type="primary", use_container_width=True):
    
    if not uploaded_files or not job_description:
        st.warning("⚠️ Please upload resumes AND provide a job description.")
    else:
        with st.spinner("Reading PDFs and calculating scores..."):
            # 1. Préparation des fichiers
            clear_upload_folder()
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join("uploads", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(file_path)

            # 2. Parsing et Matching (Backend)
            resumes = load_resumes(file_paths)
            results = rank_resumes(job_description, resumes)
            
            # 3. Sauvegarde dans la session
            st.session_state.results = results
            st.session_state.ai_analyses = {} # Reset l'IA précédente

# --- 5. AFFICHAGE DES RÉSULTATS (GRILLE NATIVE) ---
if st.session_state.results:
    st.divider()
    
    # Layout: Header on left, Filter on right (small)
    col_header, col_filter = st.columns([3, 1])
    
    with col_header:
        st.subheader("📊 Analysis Results")
        
    with col_filter:
        selected_limit = st.selectbox("Show top:", [5, 10, 25, 50, "Tous"], index=1)
    
    # Logique de découpage (Slicing Logic)
    if selected_limit == "Tous":
        results_to_display = st.session_state.results
    else:
        results_to_display = st.session_state.results[:selected_limit]
        
    st.caption(f"Affichage de {len(results_to_display)} résultats sur {len(st.session_state.results)} candidats au total.")
    
    # Configuration de la grille : 3 colonnes
    cols = st.columns(3)
    
    for index, candidate in enumerate(results_to_display):
        # Logique pour placer la carte dans la bonne colonne (0, 1, 2, 0, 1...)
        col_index = index % 3
        
        with cols[col_index]:
            # LE COMPOSANT CARTE : st.container(border=True)
            with st.container(border=True):
                
                # En-tête : Nom du fichier et Badge
                # On utilise des colonnes pour aligner le texte et un badge
                c_head1, c_head2 = st.columns([3, 1])
                with c_head1:
                    st.markdown(f"**{os.path.basename(candidate['filename'])}**")
                with c_head2:
                    if index == 0:
                        st.markdown(":star: **Top 1**")
                
                # Score et Barre
                score_val = candidate['score']
                score_pct = int(score_val * 100)
                
                # Utilisation de st.metric natif pour un affichage propre
                # Delta_color="off" pour garder le style neutre, ou "normal" pour vert/rouge auto
                st.metric(label="Relevance Score", value=f"{score_pct}%")
                
                # Determine color based on score
                if score_pct < 25:
                    bar_color = "#ff4b4b" # Red
                elif score_pct < 60:
                    bar_color = "#ffa421" # Yellow
                else:
                    bar_color = "#21c354" # Green
                
                # Custom HTML Progress Bar
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-radius: 5px; height: 10px; width: 100%;">
                    <div style="background-color: {bar_color}; width: {score_pct}%; height: 100%; border-radius: 5px;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                # --- LOGIQUE IA (Pour le Top 3) ---
                if index < 3:
                    st.divider()
                    
                    analysis_key = f"cand_{index}"
                    
                    # Si l'analyse n'est pas encore faite, afficher le bouton
                    if analysis_key not in st.session_state.ai_analyses:
                        if st.button("✨ Ask AI Why", key=f"btn_ai_{index}", type="secondary", use_container_width=True):
                            with st.spinner(f"Llama 3 is analyzing candidate #{index+1}..."):
                                explanation = generate_explanation(candidate['content'], job_description)
                                st.session_state.ai_analyses[analysis_key] = explanation
                                st.rerun() # Recharge la page pour afficher le texte
                    
                    # Si l'analyse est faite, l'afficher + bouton fermer
                    else:
                        st.info("🤖 **AI Recruiter Analysis:**")
                        st.markdown(st.session_state.ai_analyses[analysis_key])
                        
                        if st.button("Close Analysis", key=f"btn_close_{index}", use_container_width=True):
                            del st.session_state.ai_analyses[analysis_key]
                            st.rerun()

    # Bouton Reset global en bas
    st.markdown("---")
    if st.button("🔄 Start New Search"):
        st.session_state.results = None
        st.session_state.ai_analyses = {}
        st.rerun()