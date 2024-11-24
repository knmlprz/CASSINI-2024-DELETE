import pydeck as pdk
import requests
import pandas as pd
import streamlit as st
import json

with open("trip.json") as f:
    trip = json.load(f)
    
with open("floods.json") as f:
    floods = json.load(f)
   
with open("icons.json") as f:
    icons = json.load(f) 


df = pd.DataFrame(trip)

df2 = pd.DataFrame(floods)

df3 = pd.DataFrame(icons)

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


df["color"] = df["color"].apply(hex_to_rgb)


view_state = pdk.ViewState(latitude=50.03786872013036, longitude=22.00363581536894550, zoom=10)

layer = pdk.Layer(
    type="PathLayer",
    data=df,
    pickable=True,
    get_color="color",
    width_scale=3,
    width_min_pixels=2,
    get_path="path",
    get_width=5,
)
layer2 = pdk.Layer(
    "ScatterplotLayer",
    df2,
    pickable=False,
    opacity=0.6,
    stroked=False,
    filled=True,
    radius_scale=1,
    radius_min_pixels=100,
    line_width_min_pixels=1,
    get_position="coordinates",
    get_radius=700,
    get_fill_color=[255, 119, 0],  # Red-Orange color
    get_line_color=[0, 0, 0],
)

icon_layer = pdk.Layer(
    type="IconLayer",
    data=df3,
    get_icon="icon",
    get_size=4,
    size_scale=15,
    get_position=["lon", "lat"],
    pickable=True,
) 

deck1 = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"{name}"})
deck2 = pdk.Deck(layers=[layer2], initial_view_state=view_state, tooltip={"{name}\n{address}"})
deck3 = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{tags}"})

combined_layers = [layer2,layer,icon_layer]
deck_combined = pdk.Deck(layers=combined_layers, initial_view_state=view_state, tooltip={"text": "{name}\n{address}"})

st.pydeck_chart(deck_combined)