import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st


larga = pd.read_csv("static/larga_player.csv")
data = pd.read_csv("static/played_minutes.csv")
# ----------------- game start --------
radar_player = "J. Musiala"
player_t = larga[larga.Player == radar_player]
fig = px.bar_polar(
    player_t,
    r="deciles",
    theta="variable",
    color="type_variable",
    title=f"Gráfica Radial de Barras Interactiva de {radar_player}",
)

fig.update_traces(showlegend=False)
fig.update_polars(radialaxis_showticklabels=True)
fig.update_layout(
    polar_radialaxis_ticksuffix="",
    polar_angularaxis_rotation=90,
    polar_angularaxis_direction="clockwise",
    polar_radialaxis_dtick=10,
    polar_hole=0.10,
)

league, team, player = st.tabs(["League", "Team", "Player"])

with league:
    st.subheader("Gráficas de desempeño")
    """
    Estas gráficas tienen un conjunto de métricas seleccionadas a partir de técnicas de inteligencia artificial.
    Cada barra representa la fuerza relativa del jugador en cada una de las métricas.
    La distancia que existe de la barra al centro indica el percentil comparado con la base de datos completa.

    La descripción completa la encontrarás en la entrada [Gráfica de desempeño de jugadores](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    st.plotly_chart(fig)

with team:
    st.subheader("Gráficas de consistencia")
    """
    En la figura de abajo mostramos un mapa de calor.
    En los renglones podemos ver a los jugadores del equipo (incluyendo a los sustitutos).
    Las columnas corresponden a los partidos disputados.
    Así, el color de cada cuadro representa los minutos disputados en un partido por cada jugador.

    La descripción completa la encontrarás en la entrada [Consistencia en las alineaciones](https://www.nies.futbol/2023/08/consistencia-en-las-alineaciones-la.html).
    """
    teams = ["Cimarrones", "Cancún", "Mineros de Zacatecas"]
    colours = {"Cimarrones": "oranges", "Cancún": "blues", "Mineros de Zacatecas": "reds"}
    team = st.selectbox("Selecciona un equipo:", teams)
    color = colours[team]
    played_minutes = data[data.team == team]

    # Crear el gráfico de Altair
    chart = (
        alt.Chart(played_minutes, title=f"Minutes Played by Player and Match: \n{team}")
        .mark_rect()
        .encode(
            alt.X("match:N", sort=alt.EncodingSortField(field="date", order="ascending")).title(
                "Match"
            ),
            alt.Y(
                "player:N",
                sort=alt.EncodingSortField(field="minutes", op="sum", order="descending"),
                title="Player",
            ),
            alt.Color("minutes:Q", scale=alt.Scale(scheme=color)).title("Minutes"),
            tooltip=[
                alt.Tooltip("match:N", title="Match"),
                alt.Tooltip("player:N", title="Player"),
                alt.Tooltip("minutes:Q", title="Minutes"),
            ],
        )
        .configure_view(step=13, strokeWidth=0)
        .configure_axis(domain=False, labelFontSize=10)
    )
    st.altair_chart(chart)

with player:
    st.subheader("Gráficas de desempeño")
    """
    Estas gráficas tienen un conjunto de métricas seleccionadas a partir de técnicas de inteligencia artificial.
    Cada barra representa la fuerza relativa del jugador en cada una de las métricas.
    La distancia que existe de la barra al centro indica el percentil comparado con la base de datos completa.

    La descripción completa la encontrarás en la entrada [Gráfica de desempeño de jugadores](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/niesfutbol/streamlit_nies/develop/static/logo_serie_a.png",
            xref="paper",
            yref="paper",
            x=0.9,
            y=1.05,
            sizex=0.2,
            sizey=0.2,
            xanchor="right",
            yanchor="bottom",
        )
    ).add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/niesfutbol/streamlit_nies/develop/static/logo_nies.png",
            xref="paper",
            yref="paper",
            x=0.05,
            y=0.05,
            sizex=0.2,
            sizey=0.2,
        )
    )
    st.plotly_chart(fig)


st.markdown("Made with 💖 by [nies.futbol](https://nies.futbol)")
