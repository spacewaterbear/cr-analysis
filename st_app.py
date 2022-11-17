import pandas as pd
import streamlit as st
import variables as v
from utils.streamlit_utils import STUtils
import plotly.express as px

import locale

locale.setlocale(locale.LC_ALL, '')

st.set_page_config(layout="wide",
                   page_title="Suivi de présence des conseillers de Paris",
                   page_icon=":bar_chart:"
                   )

@st.experimental_memo
def load_main_csv():
    df = pd.read_csv(v.all_csv_path, parse_dates=["date"])
    df["id"] = df["title"] + df["last_name"] + df["first_name"]
    df["Nom complet"] = df["title"] + " " + df["last_name"] + " " + df["first_name"]
    df.sort_values(by="date", inplace=True)
    return df


df = load_main_csv()
if df.empty:
    st.error("No data found")
    st.stop()
# get unique year from the column date in df
years = df["date"].dt.year.unique().tolist()

st.title("Suivi de présence des conseillers de Paris (version alpha)")
st.write(f":warning: Les données ont été récupéré automatiquement à partir des pdfs disponibles sur [le site de la ville de Paris]({v.paris_pdf_url}). Il est possible que certaines données soient erronées. :warning:")

st.write("check out this ")
with st.expander("Voir les données brutes"):
    st.dataframe(df)
    STUtils.generate_df_download_button(df=df, file_name="raw_data")

st.sidebar.image("https://www.anticor.org/wp-content/uploads/2022/09/logo-anti-cor.png")

st.sidebar.write("## Paramètres")

years = st.sidebar.multiselect("Choisir les années que vous souhaitez analyser", options=years, default=years[0], format_func=str, help="Par défaut, prend une année parmi celles disponibles")

unique_dates = df[df["date"].dt.year.isin(years)]["date"].unique()
nb_dates = len(unique_dates)

st.sidebar.write(f"Nombres de jour analysées sur la période {', '.join(map(str,years))} : {nb_dates}")

all_days = st.sidebar.checkbox("Analyser tous les jours", value=True, help="Si décoché, il faudra sélectionner les jours manuellement")

if not all_days:
    days = st.sidebar.multiselect("Choisissez un ou plusieurs jours à analyser", options=unique_dates,
                                  format_func=lambda x: pd.Timestamp(x).strftime("%d %B %Y")
                                  )
    df = df[df["date"].isin(days)]


dg = df.groupby(["date", "status"]).count()["title"].reset_index().rename(columns={"title":"count"})
long_df = px.data.medals_long()

st.write("## Vision globale")
fig = px.bar(df, x="raw_time", y="status", color="status", title="Absence",
             category_orders={"status": ["present", "legit_forgive", "forgive", "absent"]})
st.plotly_chart(fig)


presence_type_dg = df.groupby("status").count()["title"].reset_index().rename(columns={"title":"count"})


pie_fig = px.pie(presence_type_dg, values="count", names="status", title="Répartition des présences")
st.plotly_chart(pie_fig)
with st.expander("Voir les données brutes"):
    st.dataframe(presence_type_dg)

best_absent = df[df["status"] == "absent"].groupby(["Nom complet"]).count()["title"].reset_index().rename(columns={"title":"count"})
top_ten_absent = best_absent.sort_values(by="count", ascending=False).head(10).reset_index(drop=True)
st.write("## Top 10 des absents par demi-journée")
st.dataframe(top_ten_absent)