import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import numpy as np


st.set_page_config(page_title="Immobilien Südtirol", page_icon=":bar_chart:", layout="centered")


st.title("Vergleich Immobilienpreise in Südtiroler Gemeinden")
st.markdown("Das OMI (Osservatorio Mercato Immobiliare) erhebt halbjährlich Daten zu Immobilienpreisen. Die Berechnung basiert auf einer Stichprobe von **abgeschlossenen Kaufverträgen** im jeweiligen Jahr. Mittels eines statistischen Verfahrens wird ein minimaler und maximaler Wert für die jeweilige Art der Immobilie geschätzt.")
st.markdown("Die OMI Werte entsprechen nicht den durchschnittlichen Wert von Immobilien, sondern geben eine Bandbreite an, in der ein Wert für Immobilien am wahrscheinlichsten liegt.")
st.markdown("In der folgenden Applikation können Sie die Werte von Immobilienp verschiedener Art in Südtiroler Gemeinden vergleichen. Dazu werden die Daten aller Jahre vom zweiten Semester verwendet. Der **mittlere Verkauspreis** wird berechnet indem die Summe von minimaler und maximaler Schätzung halbiert wird.")
st.markdown("Je nach Eingabe Ihrer Parameter kann es sein, dass einige Gemeinden nicht vorhanden sind. So haben zum Beispiel nur größere Gemeinden halbzentrale Zonen. Bei kleineren Gemeinden sind Flächen außerhalb des Zentrums als peripher, suburban oder extraurban definiert.")

url_ra = "https://www.agenziaentrate.gov.it/portale/web/guest/schede/fabbricatiterreni/omi/banche-dati/quotazioni-immobiliari"
st.markdown("Weitere Informationen zu den verwendenten Daten finden Sie hier: [OMI](%s)" % url_ra)


df = pd.read_excel("https://raw.githubusercontent.com/Schesch/suedtirol_statistiken/main/data/preise_df.xlsx")



st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)


st.subheader("Wählen Sie den Typ der Immobilie")
col1, col2, col3 = st.columns(3)
with col1:
    typ_immobilie = st.selectbox(
        "Art der Immobilie",
        ("Privatwohnungen", "Villen und Einfamilienhäuser", "Büros", "Geschäfte", "Garagen", "Magazine"),
        index=0,
        )
with col2:
    zone = st.selectbox(
        "Zone der Immobilie",
        ("Zentral", "Halbzentral", "Peripher", "Suburban", "Extraurban"),
        index=0,
        )
with col3:
    zustand = st.selectbox(
        "Zustand der Immobilie",
        ("Normal", "Ausgezeichnet"),
        index=0,
        )

if typ_immobilie == "Privatwohnungen":
    typ_immobilie = 20
elif typ_immobilie == "Villen und Einfamilienhäuser":
    typ_immobilie = 1
elif typ_immobilie == "Büros":
    typ_immobilie = 6
elif typ_immobilie == "Geschäfte":
    typ_immobilie = 9
elif typ_immobilie == "Garagen":
    typ_immobilie = 13
elif typ_immobilie == "Magazine":
    typ_immobilie = 9

if zone == "Zentral":
    zone = "B"
elif zone == "Halbzentral":
    zone = "C"
elif zone == "Peripher":
    zone = "D"
elif zone == "Extraurban":
    zone = "R"
elif zone == "Suburban":
    zone = "E"

if zustand == "Normal":
    zustand = "NORMALE"
elif zustand == "Ausgezeichnet":
    zustand = "OTTIMO"


# Filter the DataFrame based on specified conditions
filtered_df = df[(df['Cod_Tip'] == typ_immobilie) & (df['Fascia'] == zone) & (df['Stato'] == zustand)]

unique_gemeinde_de_list = filtered_df['gemeinde_de'].unique().tolist()



st.subheader("Vergleich von Gemeinden")
gm1, gm2, gm3 = st.columns(3)
with gm1:
    gemeinde1 = st.selectbox(
        "Gemeinde 1",
        options=unique_gemeinde_de_list,
        placeholder="Gemeinde",
        index= 0,
        )
with gm2:
    gemeinde2 = st.selectbox(
        "Gemeinde 2",
        options=unique_gemeinde_de_list,
        placeholder="Benchmark Gemeinde",
        index = 1,
        )
with gm3:
    gemeinde3 = st.selectbox(
        "Gemeinde 3",
        options=unique_gemeinde_de_list,
        placeholder="Benchmark Gemeinde",
        index = 2,
        )

# Assuming gemeinde1 and gemeinde2 have been set from the user's input in the Streamlit app
mean_df = filtered_df.groupby('Anno')['Compr_medio'].mean().round(0).reset_index()
gemeinde1_df = filtered_df[filtered_df['gemeinde_de'] == gemeinde1]
gemeinde2_df = filtered_df[filtered_df['gemeinde_de'] == gemeinde2]
gemeinde3_df = filtered_df[filtered_df['gemeinde_de'] == gemeinde3]

mean_df = mean_df.rename(columns={
    'Compr_medio': 'Mittelwert Durchschnitt'
})

# Rename the columns to reflect the selected municipalities
gemeinde1_df = gemeinde1_df.rename(columns={
    'Compr_min': f'Minimum {gemeinde1}',
    'Compr_medio': f'Mittelwert {gemeinde1}',
    'Compr_max': f'Maximum {gemeinde1}'
})

gemeinde2_df = gemeinde2_df.rename(columns={
    'Compr_min': f'Minimum {gemeinde2}',
    'Compr_medio': f'Mittelwert {gemeinde2}',
    'Compr_max': f'Maximum {gemeinde2}'
})

gemeinde3_df = gemeinde3_df.rename(columns={
    'Compr_min': f'Minimum {gemeinde3}',
    'Compr_medio': f'Mittelwert {gemeinde3}',
    'Compr_max': f'Maximum {gemeinde3}'
})

# Merge the two DataFrames based on the 'Anno' column
temp_1 = pd.merge(
    gemeinde1_df[['Anno', f'Minimum {gemeinde1}', f'Mittelwert {gemeinde1}', f'Maximum {gemeinde1}']],
    gemeinde2_df[['Anno', f'Minimum {gemeinde2}', f'Mittelwert {gemeinde2}', f'Maximum {gemeinde2}']],
    on='Anno',
    how='inner'
)

temp_2 = pd.merge(
    temp_1,
    gemeinde3_df[['Anno', f'Minimum {gemeinde3}', f'Mittelwert {gemeinde3}', f'Maximum {gemeinde3}']],
    on='Anno',
    how='inner'
)

comparison_df = pd.merge(
    temp_2,
    mean_df[['Anno', 'Mittelwert Durchschnitt']],
    on='Anno',
    how='inner'
)

# Sort the DataFrame based on the 'Anno' column, in case it's not already sorted
comparison_df = comparison_df.sort_values('Anno')
comparison_df['Anno'] = comparison_df['Anno'].apply(lambda x: '{:.0f}'.format(x))
comparison_df.rename(columns={'Anno': 'Jahr'}, inplace=True)
comparison_df.reset_index(drop=True)


mittelwert_col1 = f'Mittelwert {gemeinde1}'
mittelwert_col2 = f'Mittelwert {gemeinde2}'
mittelwert_col3 = f'Mittelwert {gemeinde3}'
mean_col = 'Mittelwert Durchschnitt'

# Calculate the min and max values across both 'Mittelwert' columns
min_mittelwert = min(comparison_df[mittelwert_col1].min(), comparison_df[mittelwert_col2].min(), comparison_df[mittelwert_col3].min(), mean_df[mean_col].min())
max_mittelwert = max(comparison_df[mittelwert_col1].max(), comparison_df[mittelwert_col2].max(), comparison_df[mittelwert_col3].max(), mean_df[mean_col].max())

# Define the lower and upper bounds of the y-axis ticks as multiples of 500
lower_bound = (min_mittelwert // 500) * 500
upper_bound = ((max_mittelwert // 500) + 1) * 500

# Generate the y-ticks from lower_bound to upper_bound at intervals of 500
y_ticks = np.arange(start=lower_bound, stop=upper_bound+1, step=500)  # +1 ensures the upper_bound is included if it's a multiple of 500


# Create traces for each line
trace1 = go.Scatter(
    x=comparison_df['Jahr'],
    y=comparison_df[mittelwert_col1],
    mode='lines',
    name=gemeinde1
)

trace2 = go.Scatter(
    x=comparison_df['Jahr'],
    y=comparison_df[mittelwert_col2],
    mode='lines',
    name=gemeinde2
)

trace3 = go.Scatter(
    x=comparison_df['Jahr'],
    y=comparison_df[mittelwert_col3],
    mode='lines',
    name=gemeinde3
)

trace4 = go.Scatter(
    x=comparison_df['Jahr'],
    y=comparison_df[mean_col],
    mode='lines',
    name='Durchschnitt Gemeinden'
)

# Create the figure and add the traces
fig = go.Figure()
fig.add_trace(trace1)
fig.add_trace(trace2)
fig.add_trace(trace3)
fig.add_trace(trace4)


# Update layout with y-axis ticks
fig.update_layout(
    title="Vergleich der mittleren Verkaufspreise als Liniendiagramm",
    xaxis=dict(
        title="Jahr",
        tickmode='array',
        tickvals=comparison_df['Jahr'],  # set the ticks to the 'Jahr' values
        ticktext=comparison_df['Jahr']   # set the tick text to the 'Jahr' values
    ),
    yaxis=dict(
        title="€ pro Quadratmeter",
        tickmode='array',
        tickvals=y_ticks,
        range=[lower_bound, upper_bound]   # set the ticks to your custom y-axis values
    ),
    legend_title="Gemeinden",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,  # Adjust as needed for your layout
        xanchor="center",
        x=0.5
    )
)

# Display the line plot in Streamlit
st.plotly_chart(fig, use_container_width=True)


st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)

# Filter for the year 2023
df_2023 = filtered_df[filtered_df['Anno'] == 2023]

df_2023 = filtered_df[filtered_df['Anno'] == 2023].rename(columns={'Compr_medio': 'Mittelwert Verkaufspreis'})

# Get the top 5 values
top_5 = df_2023.nlargest(5, 'Mittelwert Verkaufspreis')

# Get the bottom 5 values
bottom_5 = df_2023.nsmallest(5, 'Mittelwert Verkaufspreis')

# Add ranks to the top and bottom DataFrames
top_5['Rank'] = range(1, len(top_5) + 1)
bottom_5['Rank'] = range(1, len(bottom_5) + 1)



# Create the top 5 table
top_5_table = go.Figure(go.Table(
    header=dict(values=['Rang', 'Gemeinde', 'Mittelwert Verkaufspreis (€/m2)'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[top_5['Rank'], top_5['gemeinde_de'], top_5['Mittelwert Verkaufspreis']], fill_color='white', align='left')
))

# Update layout for the top 5 table
top_5_table.update_layout(
    title='Top 5 2023',
    width=800,  # Adjust width according to your needs
    height=350   # Adjust height based on your content
)

# Create the bottom 5 table
bottom_5_table = go.Figure(go.Table(
    header=dict(values=['Rang', 'Gemeinde', 'Mittelwert Verkaufspreis (€/m2)'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[bottom_5['Rank'], bottom_5['gemeinde_de'], bottom_5['Mittelwert Verkaufspreis']], fill_color='white', align='left')
))

# Update layout for the bottom 5 table
bottom_5_table.update_layout(
    title='Bottom 5 2023',
    width=800,  # Adjust width according to your needs
    height=400   # Adjust height based on your content
)

# Display the figures in Streamlit
st.plotly_chart(top_5_table, use_container_width=True)
st.plotly_chart(bottom_5_table, use_container_width=True)