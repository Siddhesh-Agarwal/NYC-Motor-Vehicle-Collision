import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_PATH = "./data/nypd-motor-vehicle-collisions.csv"
st.title("NYC Motor Vehicle Collisions")
st.markdown(
    "This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in New York City."
)


def load_data(nrows):
    data = pd.read_csv(
        DATA_PATH, nrows=nrows, parse_dates=[["ACCIDENT DATE", "ACCIDENT TIME"]]
    )
    data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(
        columns={
            "accident date_accident time": "date/time",
            "number of persons injured": "injured_persons",
        },
        inplace=True,
    )
    return data


st.header("Where are the most people injured in NYC?")
data = load_data(100000)
injured_people = st.slider(
    label="Number of persons injured in vehicle collisions",
    min_value=0,
    max_value=20,
    step=1,
    help="Choose the number of persons injured in vehicle collisions",
)

results = data.query("injured_persons >= @injured_people")[
    ["latitude", "longitude"]
].dropna(how="any")
midpoint = (np.average(results["latitude"]), np.average(results["longitude"]))

st.write(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=results,
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ],
    )
)

if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)
