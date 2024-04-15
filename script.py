import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np


st.set_page_config(page_title="Immobilien Südtirol", page_icon=":bar_chart:", layout="centered")


st.title("Preisvergleich Immobilien in Südtiroler Gemeinden")
st.markdown("Das OMI (Osservatorio Mercato Immobiliare) erhebt halbjährlich Daten zu Immobilienpreisen. Die Berechnung basiert auf einer Stichprobe von abgeschlossenen Kaufverträgen. Mittels eines statistischen Verfahrens wird ein minimaler und maximaler Wert für die jeweilige Immobilie geschätzt.")
st.markdown("Die OMI Werte ersetzen nicht die genaue Bewertung einzelner Immobilien, sondern geben eine Bandbreite an, in der der durchschnittliche Wert für Immobilien am wahrscheinlichsten liegt.")
st.markdown("In der folgenden Applikation können Sie die Schätzung von Immobilienp verschiedener Art in Südtiroler Gemeinden vergleichen. Dazu werden die Daten aller Jahre vom zweiten Semester verwendet. Der **mittlere Verkauspreis** wird berechnet indem die Summe von minimaler und maximaler Schätzung halbiert wird.")
st.markdown("Je nach Eingabe Ihrer Parameter kann es sein, dass einige Gemeinden nicht vorhanden sind. So haben zum Beispiel nur größere Gemeinden halbzentrale Zonen. Bei kleineren Gemeinden sind Flächen außerhalb des Zentrums als peripher, suburban oder extraurban definiert.")

url_ra = "https://www.agenziaentrate.gov.it/portale/web/guest/schede/fabbricatiterreni/omi/banche-dati/quotazioni-immobiliari"
st.markdown("Weitere Informationen zu den verwendenten Daten finden Sie hier: [OMI](%s)" % url_ra)


df = pd.read_excel("https://raw.githubusercontent.com/Schesch/suedtirol_immobilienpreise/main/preise_df.xlsx")



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

# Define subplot to hold two tables
fig = make_subplots(
    rows=1, 
    cols=2, 
    column_widths=[0.6, 0.6], 
    subplot_titles=('Top 5 2023', 'Bottom 5 2023'),
    horizontal_spacing=0.2,
    vertical_spacing= 0.5,
    specs=[[{'type': 'table'}, {'type': 'table'}]] # Define the subplot types as 'table'
)

# Assuming you have top_5 and bottom_5 DataFrames as before
# Create the top 5 table
top_5_table = go.Table(
    header=dict(values=['Rang', 'Gemeinde', 'Mittelwert Verkaufspreis (€/m2)'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[top_5['Rank'], top_5['gemeinde_de'], top_5['Mittelwert Verkaufspreis']], fill_color='white', align='left')
)

# Create the bottom 5 table
bottom_5_table = go.Table(
    header=dict(values=['Rang', 'Gemeinde', 'Mittelwert Verkaufspreis (€/m2)'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[bottom_5['Rank'], bottom_5['gemeinde_de'], bottom_5['Mittelwert Verkaufspreis']], fill_color='white', align='left')
)

# Add tables to the subplot
fig.add_trace(top_5_table, row=1, col=1)
fig.add_trace(bottom_5_table, row=1, col=2)

# Update layout for better spacing
fig.update_layout(
    width=1400,
    height=400
)

# Add tables to the subplot
fig.add_trace(top_5_table, row=1, col=1)
fig.add_trace(bottom_5_table, row=1, col=2)



st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)


# Display the figure
st.plotly_chart(fig, use_container_width=True)



st.subheader("Vergleich von Gemeinden")
gm1, gm2 = st.columns(2)
with gm1:
    gemeinde1 = st.selectbox(
        "Wählen Sie eine Gemeinde",
        options=unique_gemeinde_de_list,
        placeholder="Gemeinde",
        index= 0,
        )
with gm2:
    gemeinde2 = st.selectbox(
        "Wählen Sie eine Benchmark Gemeinde",
        options=unique_gemeinde_de_list,
        placeholder="Benchmark Gemeinde",
        index = 1,
        )

# Assuming gemeinde1 and gemeinde2 have been set from the user's input in the Streamlit app
gemeinde1_df = filtered_df[filtered_df['gemeinde_de'] == gemeinde1]
gemeinde2_df = filtered_df[filtered_df['gemeinde_de'] == gemeinde2]

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

# Merge the two DataFrames based on the 'Anno' column
comparison_df = pd.merge(
    gemeinde1_df[['Anno', f'Minimum {gemeinde1}', f'Mittelwert {gemeinde1}', f'Maximum {gemeinde1}']],
    gemeinde2_df[['Anno', f'Minimum {gemeinde2}', f'Mittelwert {gemeinde2}', f'Maximum {gemeinde2}']],
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

# Calculate the min and max values across both 'Mittelwert' columns
min_mittelwert = min(comparison_df[mittelwert_col1].min(), comparison_df[mittelwert_col2].min())
max_mittelwert = max(comparison_df[mittelwert_col1].max(), comparison_df[mittelwert_col2].max())

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

# Create the figure and add the traces
fig = go.Figure()
fig.add_trace(trace1)
fig.add_trace(trace2)


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
        y=-0.3,  # Adjust as needed for your layout
        xanchor="center",
        x=0.5
    )
)

# Update the layout for the legend
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,  # You might need to adjust this value based on your exact layout
        xanchor="center",
        x=0.0
    )
)

# Display the line plot in Streamlit
st.plotly_chart(fig, use_container_width=True)



# Create a Plotly table
fig = go.Figure(data=[go.Table(
    header=dict(values=list(comparison_df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[comparison_df[col] for col in comparison_df.columns],
               fill_color='white',
               align='left'))
])

# Add a title to the figure
fig.update_layout(
    title='Alle Preise im Zeitverlauf als Tabelle der Immobilie Ihrer ausgewählten Gemeinden',
    height = 800
)


# Display the Plotly table in Streamlit
st.plotly_chart(fig, use_container_width=True)