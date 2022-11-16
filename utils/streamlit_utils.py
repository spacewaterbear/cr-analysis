from pathlib import Path

import pandas as pd
import streamlit as st



class STUtils:

    @staticmethod
    def convert_df_to_bytes(df: pd.DataFrame):
        """Convert a pandas dataframe to csv or html
        """
        return df.to_csv().encode('utf-8')

    @staticmethod
    def generate_df_download_button(df: pd.DataFrame, file_name: str):
        csv = STUtils.convert_df_to_bytes(df)
        file_name = f"{Path(file_name).stem}.csv"
        st.download_button(
            f"Télécharger le csv : {file_name}",
            csv,
            file_name,
            f"text/{file_name}",
            key=file_name
        )
