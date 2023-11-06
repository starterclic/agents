
import streamlit as st
from agents.summarize import execute as summarize_execute
from agents.scrape_linkedin_agent import execute as scrape_linkedin_execute
from agents.research_agent import execute as research_execute
from agents.create_outreach_msg_agent import execute as create_outreach_msg_execute

# La configuration de page et le chargement des variables d'environnement restent en haut du fichier

# Interface utilisateur pour sélectionner l'agent
st.sidebar.title("Agents")
selected_agent = st.sidebar.selectbox("Choisir un agent", ["Résumé", "Scrape LinkedIn", "Recherche", "Créer Message d'Approche"])

# Logique principale de l'application pour l'agent de résumé
if selected_agent == "Résumé":
    st.header("Agent de Résumé")
    content_to_summarize = st.text_area("Entrez le texte à résumer")
    if st.button("Générer Résumé"):
        summary = summarize_execute(content_to_summarize)
        st.write(summary)


# Interface utilisateur pour l'agent Scrape LinkedIn
if selected_agent == "Scrape LinkedIn":
    st.header("Agent Scrape LinkedIn")
    linkedin_url = st.text_input("Entrez l'URL LinkedIn à scraper")
    if st.button("Scrape"):
        scrape_result = scrape_linkedin_execute(linkedin_url)
        st.write(scrape_result)

# Interface utilisateur pour l'agent Recherche
if selected_agent == "Recherche":
    st.header("Agent de Recherche")
    lead_data = st.text_area("Entrez les données du lead")
    if st.button("Rechercher"):
        research_result = research_execute(lead_data)
        st.write(research_result)

# Interface utilisateur pour l'agent Créer Message d'Approche
if selected_agent == "Créer Message d'Approche":
    st.header("Agent Créer Message d'Approche")
    research_material = st.text_area("Entrez le matériel de recherche")
    lead_info = st.text_area("Entrez les informations du lead")
    if st.button("Créer Message"):
        outreach_message = create_outreach_msg_execute(research_material, lead_info)
        st.write(outreach_message)

# (Le reste de la logique de l'application à intégrer ici)


# ...

# (Le reste de la logique de l'application à intégrer ici)


# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="Ma Super App", layout="wide")

# Import agent modules here
# from agents import summarize_agent, agent2, agent3

# ... (le reste du contenu de app.py)

import streamlit as st
from agents import summarize, scrape_linkedin, research, create_outreach_msg
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="Ma Super App", layout="wide")

# Sidebar user input for summary
st.sidebar.title("Résumé")
summary_input = st.sidebar.text_area("Entrez votre texte à résumer")
summary_type = st.sidebar.selectbox("Type de résumé", options=['Court', 'Long'])
if st.sidebar.button('Résumer'):
    if summary_input:
        summary_result = summarize.summarize(summary_input, summary_type)
        st.success('Résumé généré avec succès!')
        st.write(summary_result)
    else:
        st.error('Veuillez entrer du texte à résumer.')

# Sidebar user input for LinkedIn scraping
st.sidebar.title("Scraper LinkedIn")
linkedin_input = st.sidebar.text_input("Entrez l'URL LinkedIn")
if st.sidebar.button('Scraper LinkedIn'):
    if linkedin_input:
        linkedin_data = scrape_linkedin.scrape_linkedin(linkedin_input)
        st.success('Données LinkedIn récupérées avec succès!')
        st.write(linkedin_data)
    else:
        st.error('Veuillez entrer une URL LinkedIn.')

# Sidebar user input for research
st.sidebar.title("Recherche")
research_input = st.sidebar.text_input("Entrez les données pour la recherche")
if st.sidebar.button('Rechercher'):
    if research_input:
        research_result = research.research(research_input)
        st.success('Recherche effectuée avec succès!')
        st.write(research_result)
    else:
        st.error('Veuillez entrer des données pour la recherche.')

# Sidebar user input for outreach message creation
st.sidebar.title("Créer un message de prospection")
outreach_lead = st.sidebar.text_input("Entrez les données du lead")
outreach_material = st.sidebar.text_area("Entrez le matériel de recherche")
if st.sidebar.button('Créer un message'):
    if outreach_lead and outreach_material:
        outreach_message = create_outreach_msg.create_outreach_msg(outreach_material, outreach_lead)
        st.success('Message de prospection créé avec succès!')
        st.write(outreach_message)
    else:
        st.error('Veuillez entrer les données nécessaires pour créer le message.')
