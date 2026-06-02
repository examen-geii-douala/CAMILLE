import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime

# ================================================================
#                    CONFIGURATION
# ================================================================
DUREE = 10 * 60
FICHIER = "resultats_geii.csv"
CODE_ADMIN = "IUT2024"

st.set_page_config(
    page_title="Examen DUT2 GEII - IUT Douala",
    layout="centered"
)

# ================================================================
#                    STYLE
# ================================================================
st.markdown("""
<style>
    .big-title {
        text-align: center;
        color: #1e3a8a;
        font-size: 28px;
        font-weight: bold;
        padding: 10px;
    }
    .sub-title {
        text-align: center;
        color: #dc2626;
        font-size: 20px;
        padding: 5px;
    }
    .timer-box {
        text-align: center;
        font-size: 50px;
        color: #dc2626;
        font-weight: bold;
        padding: 15px;
        border: 4px solid #dc2626;
        border-radius: 15px;
        margin: 10px auto;
        background-color: #fff1f2;
    }
    .info-box {
        background-color: #eff6ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1e40af;
        margin: 10px 0;
    }
    .section-title {
        color: #1e40af;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 0;
    }
    .stRadio > div {
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .success-box {
        text-align: center;
        background-color: #f0fdf4;
        border: 3px solid #16a34a;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
#                    BONNES REPONSES
# ================================================================
bonnes_reponses = {
    "Q1":  "La somme des courants entrants est égale à la somme des courants sortants",
    "Q2":  "La somme algébrique des tensions est nulle dans une maille fermée",
    "Q3":  "Ohm",
    "Q4":  "De simplifier un réseau électrique complexe",
    "Q5":  "RC",
    "Q6":  "Les grandeurs ne varient plus avec le temps",
    "Q7":  "Courant alternatif",
    "Q8":  "Modifier le niveau de tension",
    "Q9":  "Au moteur asynchrone",
    "Q10": "Du courant d'induit",
    "Q11": "De la fréquence d'alimentation",
    "Q12": "Puissance utile / puissance absorbée",
    "Q13": "AC vers DC",
    "Q14": "DC vers AC",
    "Q15": "D'obtenir une tension continue variable",
    "Q16": "IGBT",
    "Q17": "La fréquence appliquée au moteur",
    "Q18": "Réduire l'ondulation de la tension redressée",
    "Q19": "Protéger contre les surcharges et courts-circuits",
    "Q20": "Détecter les défauts électriques",
    "Q21": "Basse Tension",
    "Q22": "Haute Tension Alternative",
    "Q23": "La protection des personnes",
    "Q24": "Une très forte intensité de courant",
    "Q25": "Du courant transporté",
    "Q26": "Les installations électriques basse tension",
    "Q27": "Un mauvais fonctionnement des équipements",
    "Q28": "Des normes internationales en électrotechnique",
    "Q29": "Le courant maximal qu'il peut interrompre en sécurité",
    "Q30": "Garantir sécurité, conformité et continuité de service"
}

# ================================================================
#                    VARIABLES DE SESSION
# ================================================================
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'nom' not in st.session_state:
    st.session_state.nom = ""
if 'matricule' not in st.session_state:
    st.session_state.matricule = ""
if 'etablissement' not in st.session_state:
    st.session_state.etablissement = ""

# ================================================================
#                    EN-TETE
# ================================================================
st.markdown("""
<div class='big-title'>
    🎓 Évaluation des Compétences en Électrotechnique et Génie Électrique
</div>
<div class='sub-title'>
    DUT2 GEII — IUT DE DOUALA
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ================================================================
#                    PAGE IDENTIFICATION
# ================================================================
if st.session_state.start_time is None and not st.session_state.submitted:

    st.markdown("""
    <div class='info-box'>
    <b>Bonjour,</b><br><br>
    Ce questionnaire vise à évaluer vos connaissances en
    <b>électrotechnique et génie électrique</b>.<br>
    Veuillez répondre à toutes les questions en choisissant
    <b>une seule réponse</b>.<br><br>
    ⏱️ Vous disposez de <b>10 minutes</b>.<br>
    À la fin du temps, le formulaire sera soumis automatiquement.<br><br>
    📌 <b>Remplissez d'abord votre identification avant de commencer.</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Identification de l'étudiant")

    with st.form("identification"):
        nom = st.text_input(
            "Nom et Prénom *",
            placeholder="Ex: DUPONT Jean"
        )
        matricule = st.text_input(
            "Matricule *",
            placeholder="Ex: 2024GEII0012"
        )
        etablissement = st.text_input(
            "Établissement *",
            placeholder="IUT de Douala",
            value="IUT de Douala"
        )

        st.markdown("---")
        st.warning(
            "⚠️ Dès que vous cliquez sur le bouton ci-dessous, "
            "le chronomètre de 10 minutes démarre immédiatement !"
        )

        bouton_start = st.form_submit_button(
            "🚀 COMMENCER L'EXAMEN — 10 MINUTES CHRONO",
            use_container_width=True
        )

        if bouton_start:
            if nom.strip() and matricule.strip() and etablissement.strip():
                st.session_state.start_time = time.time()
                st.session_state.nom = nom.strip()
                st.session_state.matricule = matricule.strip()
                st.session_state.etablissement = etablissement.strip()
                st.rerun()
            else:
                st.error("❌ Tous les champs sont obligatoires !")

# ================================================================
#                    PAGE FIN D'EXAMEN
# ================================================================
elif st.session_state.submitted:
    st.markdown("""
    <div class='success-box'>
        <h2>✅ Examen soumis avec succès !</h2>
        <p>Merci d'avoir participé à cet examen.</p>
        <p>Vous pouvez maintenant fermer cette page.</p>
        <p>Bonne chance pour la suite ! 🍀</p>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
#                    PAGE EXAMEN
# ================================================================
else:
    temps_ecoule = time.time() - st.session_state.start_time
    temps_restant = DUREE - temps_ecoule

    if temps_restant <= 0:
        temps_restant = 0

    m, s = divmod(int(temps_restant), 60)

    # Timer
    couleur_timer = "#dc2626"
    if temps_restant <= 60:
        couleur_timer = "#7f1d1d"
    elif temps_restant <= 300:
        couleur_timer = "#ea580c"

    st.markdown(f"""
    <div class='timer-box' style='border-color:{couleur_timer};
    color:{couleur_timer};'>
        ⏱️ TEMPS RESTANT : {m:02d}:{s:02d}
    </div>
    """, unsafe_allow_html=True)

    if temps_restant <= 300 and temps_restant > 60:
        st.warning("⚠️ Attention ! Il vous reste moins de 5 minutes !")
    if temps_restant <= 60 and temps_restant > 0:
        st.error("🚨 URGENT ! Il vous reste moins d'1 minute !")
    if temps_restant == 0:
        st.error("⏰ TEMPS ÉCOULÉ ! Soumission automatique en cours...")

    st.markdown("---")
    st.markdown(f"""
    <div class='info-box'>
        👤 <b>Étudiant :</b> {st.session_state.nom}<br>
        🆔 <b>Matricule :</b> {st.session_state.matricule}<br>
        🏫 <b>Établissement :</b> {st.session_state.etablissement}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    with st.form("examen_complet"):

        # ============================================================
        #              SECTION 1 : CIRCUITS ELECTRIQUES
        # ============================================================
        st.markdown("""
        <div class='section-title'>
            📘 SECTION 1 : CIRCUITS ÉLECTRIQUES
        </div>
        """, unsafe_allow_html=True)

        r1 = st.radio(
            "Q1. La loi des nœuds de Kirchhoff stipule que :",
            [
                "La somme des tensions est constante",
                "La somme des courants entrants est égale à la somme des courants sortants",
                "Le courant est nul",
                "La résistance est constante"
            ],
            index=None,
            key="r1"
        )

        r2 = st.radio(
            "Q2. La loi des mailles de Kirchhoff indique que :",
            [
                "La somme algébrique des tensions est nulle dans une maille fermée",
                "La somme des courants est nulle",
                "La puissance est nulle",
                "La fréquence est constante"
            ],
            index=None,
            key="r2"
        )

        r3 = st.radio(
            "Q3. L'unité de la résistance électrique est :",
            [
                "Volt",
                "Ampère",
                "Ohm",
                "Watt"
            ],
            index=None,
            key="r3"
        )

        r4 = st.radio(
            "Q4. Le théorème de Thévenin permet :",
            [
                "De simplifier un réseau électrique complexe",
                "De mesurer la fréquence",
                "D'augmenter la tension",
                "De calculer la puissance réactive"
            ],
            index=None,
            key="r4"
        )

        r5 = st.radio(
            "Q5. La constante de temps d'un circuit RC vaut :",
            [
                "R/C",
                "RC",
                "C/R",
                "1/RC"
            ],
            index=None,
            key="r5"
        )

        r6 = st.radio(
            "Q6. Le régime permanent est atteint lorsque :",
            [
                "Les grandeurs ne varient plus avec le temps",
                "Le courant est nul",
                "La tension est nulle",
                "Le circuit est ouvert"
            ],
            index=None,
            key="r6"
        )

        st.markdown("---")

        # ============================================================
        #              SECTION 2 : MACHINES ELECTRIQUES
        # ============================================================
        st.markdown("""
        <div class='section-title'>
            📗 SECTION 2 : MACHINES ÉLECTRIQUES
        </div>
        """, unsafe_allow_html=True)

        r7 = st.radio(
            "Q7. Un transformateur fonctionne avec :",
            [
                "Courant continu",
                "Courant alternatif",
                "Courant pulsé",
                "Courant mixte"
            ],
            index=None,
            key="r7"
        )

        r8 = st.radio(
            "Q8. La fonction principale d'un transformateur est :",
            [
                "Modifier le niveau de tension",
                "Modifier la fréquence",
                "Produire de l'énergie",
                "Stocker l'énergie"
            ],
            index=None,
            key="r8"
        )

        r9 = st.radio(
            "Q9. Le glissement est associé :",
            [
                "Au moteur asynchrone",
                "Au moteur synchrone",
                "Au transformateur",
                "Au générateur CC"
            ],
            index=None,
            key="r9"
        )

        r10 = st.radio(
            "Q10. Dans un moteur CC, le couple dépend principalement :",
            [
                "Du courant d'induit",
                "De la couleur des balais",
                "De la fréquence",
                "De la température"
            ],
            index=None,
            key="r10"
        )

        r11 = st.radio(
            "Q11. La vitesse synchrone dépend :",
            [
                "De la fréquence d'alimentation",
                "Du courant nominal",
                "Du facteur de puissance",
                "De la puissance mécanique"
            ],
            index=None,
            key="r11"
        )

        r12 = st.radio(
            "Q12. Le rendement d'une machine électrique est :",
            [
                "Puissance utile / puissance absorbée",
                "Puissance absorbée / puissance utile",
                "Tension / courant",
                "Courant / tension"
            ],
            index=None,
            key="r12"
        )

        st.markdown("---")

        # ============================================================
        #           SECTION 3 : ELECTRONIQUE DE PUISSANCE
        # ============================================================
        st.markdown("""
        <div class='section-title'>
            📙 SECTION 3 : ÉLECTRONIQUE DE PUISSANCE
        </div>
        """, unsafe_allow_html=True)

        r13 = st.radio(
            "Q13. Un redresseur convertit :",
            [
                "AC vers DC",
                "DC vers AC",
                "AC vers AC",
                "DC vers DC"
            ],
            index=None,
            key="r13"
        )

        r14 = st.radio(
            "Q14. Un onduleur convertit :",
            [
                "AC vers DC",
                "DC vers AC",
                "AC vers AC",
                "DC vers DC"
            ],
            index=None,
            key="r14"
        )

        r15 = st.radio(
            "Q15. Un hacheur permet :",
            [
                "D'obtenir une tension continue variable",
                "D'obtenir une tension alternative",
                "D'augmenter la fréquence",
                "De mesurer le courant"
            ],
            index=None,
            key="r15"
        )

        r16 = st.radio(
            "Q16. Le composant de puissance le plus utilisé dans les variateurs modernes est :",
            [
                "IGBT",
                "LED",
                "Résistance",
                "Fusible"
            ],
            index=None,
            key="r16"
        )

        r17 = st.radio(
            "Q17. Un variateur de vitesse agit principalement sur :",
            [
                "La fréquence appliquée au moteur",
                "La couleur du moteur",
                "Le nombre de roulements",
                "La température ambiante"
            ],
            index=None,
            key="r17"
        )

        r18 = st.radio(
            "Q18. Le rôle d'un condensateur de filtrage est :",
            [
                "Réduire l'ondulation de la tension redressée",
                "Augmenter la fréquence",
                "Protéger contre les courts-circuits",
                "Réduire le courant nominal"
            ],
            index=None,
            key="r18"
        )

        st.markdown("---")

        # ============================================================
        #        SECTION 4 : DISTRIBUTION ET PROTECTION
        # ============================================================
        st.markdown("""
        <div class='section-title'>
            📕 SECTION 4 : DISTRIBUTION ET PROTECTION ÉLECTRIQUE
        </div>
        """, unsafe_allow_html=True)

        r19 = st.radio(
            "Q19. Le rôle principal d'un disjoncteur est :",
            [
                "Protéger contre les surcharges et courts-circuits",
                "Augmenter la tension",
                "Mesurer la fréquence",
                "Contrôler un moteur"
            ],
            index=None,
            key="r19"
        )

        r20 = st.radio(
            "Q20. Un relais de protection sert à :",
            [
                "Détecter les défauts électriques",
                "Produire de l'énergie",
                "Augmenter la puissance",
                "Stocker l'énergie"
            ],
            index=None,
            key="r20"
        )

        r21 = st.radio(
            "Q21. BT signifie :",
            [
                "Basse Tension",
                "Bonne Tension",
                "Batterie Technique",
                "Bus Tension"
            ],
            index=None,
            key="r21"
        )

        r22 = st.radio(
            "Q22. HTA signifie :",
            [
                "Haute Tension Alternative",
                "Haute Température Assistée",
                "Haute Technologie Automatique",
                "Hyper Tension Automatique"
            ],
            index=None,
            key="r22"
        )

        r23 = st.radio(
            "Q23. La mise à la terre permet :",
            [
                "La protection des personnes",
                "L'augmentation de puissance",
                "La réduction de fréquence",
                "Le stockage d'énergie"
            ],
            index=None,
            key="r23"
        )

        r24 = st.radio(
            "Q24. Le court-circuit se caractérise par :",
            [
                "Une très forte intensité de courant",
                "Une faible tension",
                "Une fréquence nulle",
                "Une puissance nulle"
            ],
            index=None,
            key="r24"
        )

        st.markdown("---")

        # ============================================================
        #           SECTION 5 : DIMENSIONNEMENT
        # ============================================================
        st.markdown("""
        <div class='section-title'>
            📒 SECTION 5 : DIMENSIONNEMENT DES INSTALLATIONS ÉLECTRIQUES
        </div>
        """, unsafe_allow_html=True)

        r25 = st.radio(
            "Q25. Le choix de la section d'un câble dépend principalement :",
            [
                "Du courant transporté",
                "De sa couleur",
                "Du fabricant",
                "Du prix"
            ],
            index=None,
            key="r25"
        )

        r26 = st.radio(
            "Q26. La norme NFC 15-100 concerne :",
            [
                "Les installations électriques basse tension",
                "Les réseaux GSM",
                "Les moteurs thermiques",
                "Les systèmes hydrauliques"
            ],
            index=None,
            key="r26"
        )

        r27 = st.radio(
            "Q27. Une chute de tension excessive peut provoquer :",
            [
                "Un mauvais fonctionnement des équipements",
                "Une augmentation du rendement",
                "Une amélioration de la sécurité",
                "Une diminution des pertes"
            ],
            index=None,
            key="r27"
        )

        r28 = st.radio(
            "Q28. Les normes IEC sont :",
            [
                "Des normes internationales en électrotechnique",
                "Des logiciels industriels",
                "Des instruments de mesure",
                "Des fabricants de matériel"
            ],
            index=None,
            key="r28"
        )

        r29 = st.radio(
            "Q29. Le pouvoir de coupure d'un disjoncteur représente :",
            [
                "Le courant maximal qu'il peut interrompre en sécurité",
                "Son courant nominal",
                "Sa tension nominale",
                "Son rendement"
            ],
            index=None,
            key="r29"
        )

        r30 = st.radio(
            "Q30. L'objectif principal du dimensionnement électrique est :",
            [
                "Garantir sécurité, conformité et continuité de service",
                "Réduire le nombre de câbles",
                "Diminuer le nombre de protections",
                "Augmenter la consommation énergétique"
            ],
            index=None,
            key="r30"
        )

        st.markdown("---")

        # ============================================================
        #                    BOUTON SOUMETTRE
        # ============================================================
        bouton_submit = st.form_submit_button(
            "📩 SOUMETTRE MON EXAMEN",
            use_container_width=True
        )

        if bouton_submit or temps_restant <= 0:

            reponses_etudiant = {
                "Q1": r1,   "Q2": r2,   "Q3": r3,
                "Q4": r4,   "Q5": r5,   "Q6": r6,
                "Q7": r7,   "Q8": r8,   "Q9": r9,
                "Q10": r10, "Q11": r11, "Q12": r12,
                "Q13": r13, "Q14": r14, "Q15": r15,
                "Q16": r16, "Q17": r17, "Q18": r18,
                "Q19": r19, "Q20": r20, "Q21": r21,
                "Q22": r22, "Q23": r23, "Q24": r24,
                "Q25": r25, "Q26": r26, "Q27": r27,
                "Q28": r28, "Q29": r29, "Q30": r30
            }

            # Calcul de la note
            note_brute = 0
            for q, bonne in bonnes_reponses.items():
                if reponses_etudiant.get(q) == bonne:
                    note_brute += 1

            note_sur_20 = round((note_brute / 30) * 20, 2)

            # Sauvegarde dans le fichier CSV
            data = {
                "Date et Heure":    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Nom":              st.session_state.nom,
                "Matricule":        st.session_state.matricule,
                "Établissement":    st.session_state.etablissement,
                "Bonnes Réponses":  f"{note_brute}/30",
                "Note sur 20":      note_sur_20
            }

            for q, rep in reponses_etudiant.items():
                data[q] = rep if rep else "Sans réponse"

            df_new = pd.DataFrame([data])

            if os.path.exists(FICHIER):
                df_new.to_csv(
                    FICHIER,
                    mode='a',
                    header=False,
                    index=False,
                    encoding='utf-8-sig'
                )
            else:
                df_new.to_csv(
                    FICHIER,
                    mode='w',
                    header=True,
                    index=False,
                    encoding='utf-8-sig'
                )

            st.session_state.submitted = True
            st.rerun()

    # Rafraîchissement automatique du timer
    if temps_restant > 0 and not st.session_state.submitted:
        time.sleep(1)
        st.rerun()

# ================================================================
#                    ESPACE ADMINISTRATEUR
# ================================================================
st.markdown("---")
with st.expander("🔐 Espace Administrateur"):
    st.markdown("**Réservé à l'enseignant uniquement.**")
    code_admin = st.text_input(
        "Entrez le code secret :",
        type="password",
        placeholder="Code secret..."
    )

    if code_admin == CODE_ADMIN:
        st.success("✅ Accès autorisé !")

        if os.path.exists(FICHIER):
            df_admin = pd.read_csv(FICHIER, encoding='utf-8-sig')

            # Statistiques
            st.markdown("### 📊 Statistiques Générales")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Étudiants", len(df_admin))
            with col2:
                st.metric("Note Moyenne", f"{df_admin['Note sur 20'].mean():.2f}/20")
            with col3:
                st.metric("Note Max", f"{df_admin['Note sur 20'].max()}/20")
            with col4:
                st.metric("Note Min", f"{df_admin['Note sur 20'].min()}/20")

            # Tableau des résultats
            st.markdown("### 📋 Tableau des Résultats")
            st.dataframe(
                df_admin[["Date et Heure", "Nom", "Matricule", "Bonnes Réponses", "Note sur 20"]],
                use_container_width=True
            )

            # Bouton télécharger
            st.markdown("### 📥 Télécharger le fichier complet")
            with open(FICHIER, "rb") as f:
                st.download_button(
                    label="📥 TÉLÉCHARGER LE FICHIER EXCEL (CSV)",
                    data=f,
                    file_name=f"Resultats_Examen_GEII_{datetime.now().strftime('%d_%m_%Y_%Hh%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Aucun étudiant n'a encore soumis l'examen.")

    elif code_admin != "":
        st.error("❌ Code incorrect ! Accès refusé.")
