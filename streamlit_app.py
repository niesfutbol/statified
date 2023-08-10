import altair as alt
import pandas as pd
from PIL import Image
import plotly.express as px
import streamlit as st


larga = pd.read_csv("static/larga_player.csv")
data = pd.read_csv("static/played_minutes.csv")
tilt_ppda = pd.read_csv("static/xG_build-up_ppda_tilt_135.csv")
weighted = pd.read_csv("static/weighted_g_and_xg.csv")
# ---------- plot weight --------------
min_x = weighted.weighted_deffense.min()
max_x = weighted.weighted_deffense.max()
diff = (max_x - min_x) / 5
weight_plot = (
    px.scatter(
        weighted,
        x="weighted_attack",
        y="weighted_deffense",
        labels={
            "weighted_attack": "Weighted xG and G For",
            "weighted_deffense": "Weighted xG and G Against",
        },
    )
    .update_layout(yaxis=dict(autorange="reversed"), xaxis_range=[min_x - diff, max_x + diff])
    .add_layout_image(
        dict(
            source=Image.open("static/logo_nies.png"),
            xref="paper",
            yref="paper",
            x=0.7,
            y=0.2,
            sizex=0.2,
            sizey=0.2,
        )
    )
)
for x, y, id_t in zip(weighted.weighted_attack, weighted.weighted_deffense, weighted.team_id):
    weight_plot.add_layout_image(
        x=x,
        y=y,
        source=Image.open(f"static/logo_{id_t}.png"),
        xref="x",
        yref="y",
        sizex=0.07,
        sizey=0.07,
        xanchor="center",
        yanchor="middle",
    )
# -------- plot league indices --------
dropdown = alt.binding_select(
    options=["build_up_disruption", "ppda", "tilt"], name="X-axis column "
)
xcol_param = alt.param(value="tilt", bind=dropdown)

tilt_plot = (
    alt.Chart(tilt_ppda)
    .mark_circle()
    .encode(
        x=alt.X("x:Q").title(""),
        y="xG:Q",
        tooltip=["team", "xG", "tilt", "build_up_disruption", "ppda"],
    )
    .transform_calculate(x=f"datum[{xcol_param.name}]")
    .add_params(xcol_param)
)
img = (
    alt.Chart(
        {
            "values": [
                {
                    "url": "https://raw.githubusercontent.com/niesfutbol/statified/develop/static/logo_nies.png"
                }
            ]
        }
    )
    .mark_image(opacity=0.5)
    .encode(
        x=alt.value(270),
        x2=alt.value(300),  # pixels from left
        y=alt.value(320),
        y2=alt.value(350),  # pixels from top
        url="url:N",
    )
)
new_plot = alt.layer(tilt_plot, img)
# ------------- game start ------------
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
    st.subheader("Tilt and pressure indices")
    """
    The tilt tells us about the possession of a team's ball in an area where it can do damage, the last third of the pitch.
    The definition of tilt is the percentage of total passes that a team made in the final third of the field.
    For example, suppose that there were ten passes in the last third of the pitch in a game.
    Let's say the home team made seven passes, and the away team made 3.
    So the home team's tilt would be 70%, and the away team's 30%.

    The PPDA is a metric that we use to evaluate the defensive pressure of a team on the opposing
    team. The PPDA measures the number of passes the defending team allows before it takes defensive
    action. These defensive actions can be a steal attempt, an interception, or a foul.

    BDP (Build-Up Disruption) is a metric to measure a team's ability to disrupt the opposing team's
    build-up game. The name refers to the interruption in the construction phase of the play.

    You will find the full description in the blog notes [The inclination and pressure for Napoles](https://www.nies.futbol/2023/05/la-inclinacion-y-la-presion-para-el.html)
    and [Pressure indices: PPDA and Build-Up Disruption](https://www.nies.futbol/2023/04/indices-de-presion-ppda-y-build-up.html).
    """
    st.altair_chart(new_plot)
    st.plotly_chart(weight_plot)

    """
        - The repo to calculate the pressure indeces is [pressure_index](https://github.com/niesfutbol/pressure_index) (R y Python)
        - The repo to calculate the weighted G and xG is [calculator-trs](https://github.com/nepito/calculator-trs) (R)
    """

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
    teams = data.team.unique().tolist()
    colours = {t:c for t,c in zip(weighted.names, weighted.colours)}
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

    """
        - The repo to download data about consistency in lineups is [football](https://gitlab.com/nepito/football) (Python)
        - The repo to calculate consistency in lineups is [consistent_lineup_setup](https://github.com/niesfutbol/consistent_lineup_setup) (Python)
    """
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
            source="https://raw.githubusercontent.com/niesfutbol/statified/develop/static/logo_serie_a.png",
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
            source=Image.open("static/logo_nies.png"),
            xref="paper",
            yref="paper",
            x=0.05,
            y=0.05,
            sizex=0.2,
            sizey=0.2,
        )
    )
    st.plotly_chart(fig)
    """
        - The repo to calculate the player's cluster is [cluster_players](https://github.com/niesfutbol/cluster_players) (R)
    """


st.markdown("Made with 💖 by [nies.futbol](https://nies.futbol)")
