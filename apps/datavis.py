#%%
import os
from turtle import pos
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pingouin as pg

from scipy.stats import iqr
from apps.utils import make_cmap, map_val, moving_average

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

@st.cache(ttl=3600, show_spinner=True)
def station_colors():
    categorical = make_cmap([(100, 143, 255), (120, 94, 240), (220, 38, 127), (254,97,0), (255, 176, 0)], bit=True, cmap_name='grouping')
    stations = np.unique(dataframe['Estacao'])
    st_colors = {station:categorical((n+1)/(len(stations)+1)) for n,station in enumerate(stations)}
    return st_colors

st_colors = station_colors()    

#%%
def plot_poluentes(filtered_df, jitter=0.1) -> list:
        figs = list()
        for data in filtered_df.groupby('Poluente'):
            height = map_val(len(np.unique(data[1]['Estacao'])), 0, len(np.unique(dataframe['Estacao'])), 4.8, 15)
            fig, ax = plt.subplots(1, 1, figsize=(6.4, height))
            figs.append(fig)
            for n, city in enumerate(data[1].groupby('Estacao')):
                y_vals = city[-1]['Valor']
                ax.scatter(y_vals, np.full_like(y_vals, n)+jitter*(np.random.rand(len(y_vals))-.5), s=2, alpha=.4, color=st_colors[city[0]])
                ax.errorbar(np.median(y_vals), n, xerr=iqr(y_vals), zorder=2, color='k', marker='o')
            
            if n == 0: ax.set_ylim(-1,1)
            ax.set_yticks(range(n+1))
            ax.set_yticklabels(np.unique(data[1]['Estacao']))
            fig.suptitle(data[0])
        return figs

def plot_time_series(filtered_df, window):
    figs = list()
    for data in filtered_df.groupby('Poluente'):
        fig, ax = plt.subplots(1, 1, figsize=(12.8, 4))
        figs.append(fig)
        for city in data[1].groupby('Estacao'):
            dates = np.unique(city[-1]['Data'])[window-1:]
            y_vals = city[-1].groupby('Data')['Valor'].median()
            ax.plot(dates, moving_average(y_vals, window), linestyle='-', color=st_colors[city[0]], label=city[0])
        ax.grid(linestyle='dashed', alpha=.3)
        ax.legend(loc='best')
        fig.suptitle(data[0])
    return figs
    

def app():
    st.title("Visualização dos Poluentes")
    
    st.header("Distribuição de Dados")
    row0_1, row0_2 = st.columns(2)
    with row0_1:
        selected_station = st.multiselect('Selecione as estações de interesse', ['Todas']+list(dataframe['Estacao'].unique()), ['Campinas - Centro'])
        if 'Todas' not in selected_station: filtered_df = dataframe[dataframe['Estacao'].apply(lambda x: x in selected_station)]
        else: filtered_df = dataframe

    with row0_2:
        selected_pollutant = st.multiselect('Selecione os poluentes de interesse', ['Todos']+list(filtered_df['Poluente'].unique()), ['Todos'])
        if 'Todos' not in selected_pollutant: filtered_df = filtered_df[filtered_df['Poluente'].apply(lambda x: x in selected_pollutant)]

    if len(filtered_df) > 0:
        _, row1, _ = st.columns((.35, 1, .35))
        with row1:
                figs = plot_poluentes(filtered_df)
                for fig in figs:
                    st.pyplot(fig)
        
        st.header("Série Temporal")
        window = st.selectbox('Janela de média móvel: ', ('3', '5', '15', '30', '90', '120', '180'))

        figs = plot_time_series(filtered_df, int(window))
        for fig in figs:
                st.pyplot(fig)

        st.header("Estatísticas")
        for data in filtered_df.groupby('Poluente'):
            st.markdown(f'# {data[0]}')
            n_stations = len(np.unique(data[-1]['Estacao']))
            if n_stations == 1:
                st.markdown('## Correlações')
                dates = np.unique(data[-1]['Data']).astype('datetime64[s]').astype('int')
                y_vals = data[-1].groupby('Data')['Valor'].median()
                st.dataframe(pg.corr(dates, y_vals, method='shepherd'))
            
            elif n_stations == 2:
                st.markdown('## Teste-T')
                st.dataframe(pg.pairwise_ttests(data[-1].groupby(['Data','Estacao','Poluente'], as_index=False).median(), between='Estacao', dv='Valor', parametric=False, padjust='holm', effsize='cohen'))
                st.markdown('## Correlações')
                for city in data[-1].groupby('Estacao'):
                    city_df = city[-1].dropna(subset=['Valor'], axis=0)
                    if len(city_df) > 3:
                        st.markdown(f'### {city[0]}')
                        dates = np.unique(city_df['Data']).astype('datetime64[s]').astype('int')
                        y_vals = city_df.groupby('Data')['Valor'].median()
                        st.dataframe(pg.corr(dates, y_vals, method='shepherd'))
            
            elif n_stations > 2:
                st.markdown('## ANOVA')
                st.dataframe(pg.kruskal(data[-1].groupby(['Data','Estacao','Poluente'], as_index=False).median(), between='Estacao', dv='Valor'))
                st.markdown('## Post-hoc')
                result = pg.pairwise_ttests(filtered_df.groupby(['Data','Estacao','Poluente'], as_index=False).median(), between='Estacao', dv='Valor', parametric=False, padjust='holm', effsize='cohen')
                st.dataframe(result[result['p-corr']<=0.05])
                for city in data[-1].groupby('Estacao'):
                    city_df = city[-1].dropna(subset=['Valor'], axis=0)
                    if len(city_df) > 3:
                        st.markdown(f'### {city[0]}')
                        dates = np.unique(city_df['Data']).astype('datetime64[s]').astype('int')
                        y_vals = city_df.groupby('Data')['Valor'].median()
                        st.dataframe(pg.corr(dates, y_vals, method='shepherd'))