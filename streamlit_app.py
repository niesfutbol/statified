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
    st.subheader("Pressure indices")
    """
    The PPDA is a metric that we use to evaluate the defensive pressure of a team on the opposing
    team. The PPDA measures the number of passes the defending team allows before it takes defensive
    action. These defensive actions can be a steal attempt, an interception, or a foul.

    BDP (Build-Up Disruption) is a metric to measure a team's ability to disrupt the opposing team's
    build-up game. The name refers to the interruption in the construction phase of the play.

    You will find the full description in the entry [Pressure indices: PPDA and Build-Up Disruption](https://www.nies.futbol/2023/04/indices-de-presion-ppda-y-build-up.html).
    """
    st.plotly_chart(fig)

with team:
    st.subheader("Gráficas de consistencia")
    """
    In the figure below, we show a heat map.
    We can see the team's players (including the substitutes) in the lines.
    The columns correspond to the matches played.
    Thus, the color of each box represents the minutes played in a match by each player.

    You will find the complete description in the entry [Consistency in
    lineups](https://www.nies.futbol/2023/08/consistencia-en-las-alineaciones-la.html).
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
    These graphs have a set of metrics selected from artificial intelligence techniques.
    Each bar represents the relative strength of the player in each of the metrics.
    The distance from the bar to the center indicates the percentile compared to the complete database.

    You will find the full description in the entry [Player performance
    graph](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/niesfutbol/statified_nies/develop/static/logo_serie_a.png",
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
            source="https://raw.githubusercontent.com/niesfutbol/statified_nies/develop/static/logo_nies.png",
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
