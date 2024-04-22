import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title="Einkommen Südtirol", page_icon=":bar_chart:", layout="centered")



st.title("Vergleich Einkommen in Südtiroler Gemeinden")
st.markdown("Das Italienische Ministerium für Wirtschaft und Finanzen veröffentlicht jedes Jahr Steuerdaten zu den Einkommen auf Gemeindebasis.")
st.markdown("Die folgenden Vergleiche verwenden als Schnitt die gesamte Summe des jeweiligen Steuereinkommens gebrochen durch die Anzahl der Steuererklärungen.")
st.markdown("Es handelt sich also um das **durchschnittliche Einkommen pro Steuererklärung** und nicht um das durchschnittliche Einkommen auf Vollzeitbasis.")
st.markdown("Dies beinhaltet alle Personen die eine Steuererklärung abgeben, also auch diejenigen die in Teilzeit bzw. saisonal arbeiten.")

url_ra = "https://www1.finanze.gov.it/finanze/pagina_dichiarazioni/public/dichiarazioni.php"
st.markdown("Weitere Informationen zu den verwendenten Daten finden Sie auf der Webseite des Ministeriums: [MEF](%s)" % url_ra)


df_region = pd.read_excel("https://raw.githubusercontent.com/Schesch/suedtirol_statistiken/main/data/all_region.xlsx")
df_comune = pd.read_excel("https://raw.githubusercontent.com/Schesch/suedtirol_statistiken/main/data/all_comune.xlsx")

df_region['Regione'] = df_region['Regione'].str.replace('Trentino Alto Adige(P.A.Trento)', 'Trentino', regex=False)
df_region['Regione'] = df_region['Regione'].str.replace('Average Region', 'Durchschnitt der Regionen', regex=False)

regionen_select = ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia Romagna', 'Friuli Venezia Giulia', 
                   'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 
                   'Sicilia', 'Toscana', 'Trentino', 'Umbria', "Valle d'Aosta", 'Veneto']


st.subheader("Vergleich: Südtirol mit anderen Regionen")
income1 = st.selectbox(
    "Wählen Sie die Art des Einkommen aus",
    ("Einkommen aus abhängiger Beschäftigung", 
     "Einkommen aus autonomer Arbeit", 
     "Unternehmer mit regulärer Buchführung", 
     "Unternehmer mit vereinfachter Buchführung",
     "Einkommen aus Pensionen",
     "Einkommen aus Gebäuden",
     "Gesamtes steuerpflichtiges Einkommen"),
    index=0,
    key=1
)

if income1 == "Einkommen aus abhängiger Beschäftigung":
    income_select = "medio_dipendente"
elif income1 == "Einkommen aus autonomer Arbeit":
    income_select = "medio_autonomo"
elif income1 == "Unternehmer mit regulärer Buchführung":
    income_select = "medio_impr_normale"
elif income1 == "Unternehmer mit vereinfachter Buchführung":
    income_select = "medio_impr_semplice"
elif income1 == "Einkommen aus Pensionen":
    income_select = "medio_pensione"
elif income1 == "Einkommen aus Gebäuden":
    income_select = "medio_fabbricati"
elif income1 == "Gesamtes steuerpflichtiges Einkommen":
    income_select = "medio_totale"


st.subheader("Wählen Sie die Regionen für den Vergleich")
col1, col2, col3 = st.columns(3)
# Place each widget in its respective column
with col1:
    r1 = st.selectbox("Region 1", options=regionen_select, index = 4)
with col2:
    r2 = st.selectbox("Region 2", options=regionen_select, index = 8)
with col3:
    r3 = st.selectbox("Region 3", options=regionen_select, index = 16)




def plot_income_comparison(df, income_type, regions, years='Anno'):
    # Create a new figure object
    fig = go.Figure()

    # Filter data for the specified regions
    plot_data = df[df['Regione'].isin(regions)]

    # Setting up a dynamic y-axis range
    min_mittelwert = plot_data[income_type].min()
    max_mittelwert = plot_data[income_type].max()
    lower_bound = (min_mittelwert // 1000) * 1000
    upper_bound = ((max_mittelwert // 1000) + 1) * 1000
    y_ticks = np.arange(start=lower_bound, stop=upper_bound + 1, step=2000)  # Including upper bound

    # Loop through each region to add traces
    for region in regions:
        region_data = plot_data[plot_data['Regione'] == region]
        fig.add_trace(go.Scatter(
            x=region_data[years],
            y=region_data[income_type],
            mode='lines',
            name=region
        ))

    # Update the layout with customized axes, title, legend
    fig.update_layout(
        title=f'Vergleich: {income1}',
        xaxis=dict(
            title='Jahr',
            tickmode='array',
            tickvals=region_data[years].unique(),  # Ensuring all years are displayed
            ticktext=[str(year) for year in region_data[years].unique()]
        ),
        yaxis=dict(
            title='Einkommen in €',
            tickmode='array',
            tickvals=y_ticks,
            range=[lower_bound, upper_bound],  # Setting the range for the y-axis
            tickformat="."
        ),
        legend_title="Regionen",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,  # Adjust this value to position the legend below the chart
            xanchor="center",
            x=0.5
        )
    )


    # Use Streamlit's function to display the plot
    st.plotly_chart(fig, use_container_width=True)

# Example usage
selected_regions = ['Südtirol', 'Durchschnitt der Regionen', r1, r2, r3]  # Modify based on user selections
plot_income_comparison(df_region, income_select, selected_regions)


# Assuming 'df_region' is your DataFrame and 'income_select' is the selected type of income
#plot_income_comparison(df_region, income_select, selected_regions)  # Change 'medio_dipendente' to the actual income column if needed

df_comune['Comune_DE'] = df_comune['Comune_DE'].str.replace('Average Comune', 'Durchschnitt der Gemeinden', regex=False)


gemeinden_select = ['Abtei', 'Ahrntal', 'Aldein', 'Algund', 'Altrei', 'Andrian', 'Auer', 'Barbian', 'Bozen', 'Branzoll', 'Brenner', 
                    'Brixen', 'Bruneck', 'Burgstall', 'Corvara', 'Deutschnofen', 'Enneberg', 'Eppan an der Weinstrasse', 'Feldthurns', 
                    'Franzensfeste', 'Freienfeld', 'Gais', 'Gargazon', 'Glurns', 'Graun im Vinschgau', 'Gsies', 'Hafling', 'Innichen', 
                    'Kaltern', 'Kardaun', 'Kastelbell -Tschars', 'Kastelruth', 'Kiens', 'Klausen', 'Kuens', 'Kurtatsch an der Weinstrasse', 
                    'Kurtinig an der Weinstrasse', 'Laas', 'Lajen', 'Lana', 'Latsch', 'Laurein', 'Leifers', 'Lüsen', 'Mals', 
                    'Margreid an der Weinstrasse', 'Marling', 'Martell', 'Meran', 'Montan', 'Moos in Passeier', 'Mölten', 'Mühlbach', 
                    'Mühlwald', 'Nals', 'Naturns', 'Natz-Schabs', 'Neumarkt', 'Niederdorf', 'Olang', 'Partschins', 'Percha', 'Pfalzen', 
                    'Pfatten', 'Pfitsch', 'Plaus', 'Prad am Stilfserjoch', 'Prags', 'Prettau', 'Proveis', 'Rasen-Antholz', 'Ratschings', 
                    'Riffian', 'Ritten', 'Rodeneck', 'Salurn', 'Sand in Taufers', 'Sarntal', 'Schenna', 'Schlanders', 'Schluderns', 'Schnals', 
                    'Seis', 'St. Christina in Gröden', 'St. Leonhard in Passeier', 'St. Lorenzen', 'St. Martin in Passeier', 'St. Martin in Thurn', 
                    'St. Pankraz', 'St. Ulrich', 'Sterzing', 'Stilfs', 'Taufers', 'Terenten', 'Terlan', 'Tiers', 'Tirol', 'Tisens', 'Toblach', 
                    'Tramin an der Weinstrasse', 'Truden', 'Tscherms', 'Ulten', 'Unsere Liebe Frau im Walde - St. Felix', 'Vahrn', 'Villanders', 
                    'Villnöss', 'Vintl', 'Völs am Schlern', 'Vöran', 'Waidbruck', 'Welsberg', 'Welschnofen', 'Wengen', 'Wolkenstein in Gröden']



st.subheader("Vergleich: Südtiroler Gemeinden")
income2 = st.selectbox(
    "Wählen Sie die Art des Einkommen aus",
    ("Einkommen aus abhängiger Beschäftigung", 
     "Einkommen aus autonomer Arbeit", 
     "Unternehmer mit regulärer Buchführung", 
     "Unternehmer mit vereinfachter Buchführung",
     "Einkommen aus Pensionen",
     "Einkommen aus Gebäuden",
     "Gesamtes steuerpflichtiges Einkommen"),
    index=0,
    key=2
)

if income2 == "Einkommen aus abhängiger Beschäftigung":
    income_select2 = "medio_dipendente"
elif income2 == "Einkommen aus autonomer Arbeit":
    income_select2 = "medio_autonomo"
elif income2 == "Unternehmer mit regulärer Buchführung":
    income_select2 = "medio_impr_normale"
elif income2 == "Unternehmer mit vereinfachter Buchführung":
    income_select2 = "medio_impr_semplice"
elif income2 == "Einkommen aus Pensionen":
    income_select2 = "medio_pensione"
elif income2 == "Einkommen aus Gebäuden":
    income_select2 = "medio_fabbricati"
elif income2 == "Gesamtes steuerpflichtiges Einkommen":
    income_select2 = "medio_totale"


st.subheader("Wählen Sie die Gemeinden für den Vergleich")
col1, col2, col3 = st.columns(3)
# Place each widget in its respective column
with col1:
    g1 = st.selectbox("Gemeinde 1", options=gemeinden_select, index = 3)
with col2:
    g2 = st.selectbox("Gemeinde 2", options=gemeinden_select, index = 8)
with col3:
    g3 = st.selectbox("Gemeinde 3", options=gemeinden_select, index = 48)



def plot_income_comparison(df, income_type, regions, years='Anno'):
    # Create a new figure object
    fig = go.Figure()

    # Filter data for the specified regions
    plot_data = df[df['Comune_DE'].isin(regions)]

    # Calculate dynamic y-axis range
    min_mittelwert = plot_data[income_type].min()
    max_mittelwert = plot_data[income_type].max()
    lower_bound = (min_mittelwert // 1000) * 1000
    upper_bound = ((max_mittelwert // 1000) + 1) * 1000
    y_ticks = np.arange(start=lower_bound, stop=upper_bound + 1, step=2000)  # Including upper bound

    # Loop through each region to add traces
    for region in regions:
        region_data = plot_data[plot_data['Comune_DE'] == region]
        fig.add_trace(go.Scatter(
            x=region_data[years],
            y=region_data[income_type],
            mode='lines',
            name=region
        ))

    # Update the layout with customized axes, title, legend
    fig.update_layout(
        title=f'Vergleich: {income2}',
        xaxis=dict(
            title='Jahr',
            tickmode='array',
            tickvals=region_data[years].unique(),  # Ensuring all years are displayed
            ticktext=[str(year) for year in region_data[years].unique()]
        ),
        yaxis=dict(
            title='Einkommen in €',
            tickmode='array',
            tickvals=y_ticks,
            range=[lower_bound, upper_bound],  # Setting the range for the y-axis
            tickformat="."  # Ensures numbers are formatted with commas for thousands
        ),
        legend_title="Gemeinden",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,  # Adjust this value to position the legend below the chart
            xanchor="center",
            x=0.5
        )
    )

    # Use Streamlit's function to display the plot
    st.plotly_chart(fig, use_container_width=True)

# Define the regions to plot - Südtirol, Average Region, and selected regions
selected_comune = ['Durchschnitt der Gemeinden', g1, g2, g3]

# Call the function to plot the data
plot_income_comparison(df_comune, income_select2, selected_comune)
