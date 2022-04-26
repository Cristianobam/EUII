#%%
import os
import pandas as pd
import streamlit as st

#%%
@st.cache(ttl=3600, show_spinner=True)
def load_data():
    databases = [i for i in os.listdir('data') if i.endswith('.csv')]
    df = pd.DataFrame()
    for database in databases:
        df = pd.concat([df, pd.read_csv('data/' + database, encoding='latin-1')])
        df['Data'] = pd.to_datetime(df['Data'])
    return df

dataframe = load_data()

def app():
    st.title("Download de Dados")

    row0_1, row0_2 = st.columns(2)
    with row0_1:
        selected_station = st.multiselect('Selecione as estações de interesse', ['Todas']+list(dataframe['Estacao'].unique()), ['Campinas - Centro'])
        if 'Todas' not in selected_station: filtered_df = dataframe[dataframe['Estacao'].apply(lambda x: x in selected_station)]
        else: filtered_df = dataframe

    with row0_2:
        selected_pollutant = st.multiselect('Selecione os poluentes de interesse', ['Todos']+list(filtered_df['Poluente'].unique()), ['Todos'])
        if 'Todos' not in selected_pollutant: filtered_df = filtered_df[filtered_df['Poluente'].apply(lambda x: x in selected_pollutant)]

    st.dataframe(filtered_df.sample(10))

    csv = filtered_df.to_csv().encode('utf-8')
    _, _, row1 = st.columns((.35, 1, .35))
    with row1:
        st.download_button(
            label="Fazer Download",
            data=csv,
            file_name='dataframe.csv',
            mime='text/csv',
        )