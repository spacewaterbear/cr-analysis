import pandas as pd
import streamlit as st
import variables as v
from utils.streamlit_utils import STUtils
import plotly.express as px

import locale

locale.setlocale(locale.LC_ALL, '')

st.set_page_config(layout="wide", page_icon="👨‍", page_title="Suivi de présence des conseillers de Paris")

# @st.experimental_memo
def load_main_csv():
    df = pd.read_csv(v.all_csv_path, parse_dates=["date"])
    df.sort_values(by="date", inplace=True)
    return df


df = load_main_csv()
if df.empty:
    st.error("No data found")
    st.stop()
# get unique year from the column date in df
years = df["date"].dt.year.unique().tolist()

st.title("Suivi de présence des conseillers de Paris")

with st.expander("Voir les données brutes"):
    st.dataframe(df)
    STUtils.generate_df_download_button(df=df, file_name="raw_data")



years = st.sidebar.multiselect("Choisir les années", options=years, default=years[0], format_func=str)

unique_dates = df[df["date"].dt.year.isin(years)]["date"].unique()
nb_dates = len(unique_dates)
st.sidebar.write(f"Nombres de jour analysées sur la période {', '.join(map(str,years))} : {nb_dates}")

all_days = st.sidebar.checkbox("Analyser tous les jours", value=True)

if not all_days:
    days = st.sidebar.multiselect("Choisissez un ou plusieurs jours à analyser", options=unique_dates,
                                  format_func=lambda x: pd.Timestamp(x).strftime("%d %B %Y")
                                  )
    df = df[df["date"].isin(days)]


dg = df.groupby(["date", "status"]).count()["title"].reset_index().rename(columns={"title":"count"})
long_df = px.data.medals_long()


fig = px.bar(df, x="date", y="status", color="status", title="Absence",
             category_orders={"status": ["present", "legit_forgive", "absent"]})
st.plotly_chart(fig)

