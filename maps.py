import json
import pandas as pd
import folium
import webbrowser
import os

# === 1. Load data JSON ===
with open("jakarta_to_bsd_dummy_data.json", "r") as f:
    data = json.load(f)

# Kalau data formatnya berupa list of dict
df = pd.DataFrame(data)

# Pastikan kolomnya sesuai
df = df.rename(columns={"dtTime": "time", "lat": "latitude", "lon": "longitude"})

# === 2. Buat peta folium ===
# Ambil titik awal sebagai center map
start_lat, start_lon = df.iloc[0]["latitude"], df.iloc[0]["longitude"]
m = folium.Map(location=[start_lat, start_lon], zoom_start=15)

# Tambahkan titik-titik GPS ke peta
for i, row in df.iterrows():s
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3,
        popup=f'Time: {row["time"]}',
        color="blue",
        fill=True,
    ).add_to(m)

# Tambahkan garis penghubung (track)
coords = df[["latitude", "longitude"]].values.tolist()
folium.PolyLine(coords, color="red", weight=2.5, opacity=1).add_to(m)

# === 3. Simpan dan buka di browser ===
output_file = r"C:\Users\Acer\AI_training\gps_tracking.html"
m.save(output_file)
print(f"GPS tracking map saved to {output_file}")

# buka otomatis di browser default
webbrowser.open('file://' + os.path.realpath(output_file))
