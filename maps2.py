import json
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx

# === 1. Load data JSON ===
with open("jakarta_to_bsd_dummy_data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df.rename(columns={"dtTime": "time", "lat": "latitude", "lon": "longitude"})

# === 2. Plot GPS track on OpenStreetMap ===
fig, ax = plt.subplots(figsize=(10, 8))

# Plot garis rute
ax.plot(df["lon"], df["latitude"], color="red", linewidth=2, label="Route")

# Plot titik koordinat
ax.scatter(df["lon"], df["latitude"], color="blue", s=10, label="GPS Points")

# Tambahkan label
for i, row in df.iterrows():
    if i % 10 == 0:  # biar nggak kebanyakan teks
        ax.text(row["lon"], row["latitude"], str(row["time"]), fontsize=6)

# Set axis to geographic projection (Web Mercator)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.legend()

# Tambah background OSM
ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.OpenStreetMap.Mapnik)

# Simpan jadi gambar
plt.savefig("gps_tracking.png", dpi=300, bbox_inches="tight")
plt.show()

print("Peta GPS disimpan sebagai gps_tracking.png")
