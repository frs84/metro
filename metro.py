import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")  # active le style seaborn
st.title("Moscow Metro Ticket Selector")

# Colonnes : inputs à gauche, graphique à droite
col1, col2 = st.columns([1, 2])

with col1:
    zone = st.radio("Select travel area:",
                    ["Moscow", "Moscow + MO"],
                    index=0,
                    horizontal=True)
with col2:
    trips_per_week_input = st.number_input("Number of trips per week", min_value=1, max_value=15, value=10)

choice = [67,3160,7650] if zone == "Moscow" else [90,3940,10080]
onetrip, onemonth, threemonths = choice

st.write(f"""
    - one trip = {onetrip}r.,\n
    - one month pass = {onemonth}r.,\n
    - three months pass = {threemonths}r.
    """)

priceMsc = {onetrip : 67, onemonth: 3160, threemonths : 7650}
priceMscMO = {onetrip : 90, onemonth: 3940, threemonths : 10080}

# Ici on considère que "trips" est le nombre de trajets par semaine
trips = np.arange(5, 16)  # par exemple de 5 à 27 trajets par semaine

df = pd.DataFrame({
    "Trips per week": trips,
    "Single Ticket (₽)": [onetrip] * len(trips),
    "1-Month Pass (₽)": [(onemonth / 30) * 7 / t for t in trips],     # coût par trajet via abonnement 1 mois
    "3-Month Pass (₽)": [(threemonths / 90) * 7 / t for t in trips]   # coût par trajet via abonnement 3 mois
})
# Format "long" pour seaborn
df_long = df.melt(id_vars="Trips per week", var_name="Ticket Type", value_name="Cost per Trip (₽)")

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_long, x="Trips per week", y="Cost per Trip (₽)", hue="Ticket Type", marker="o")
plt.axvline(x=trips_per_week_input, color='red', linestyle='--', linewidth=2)
plt.title("Cost per Trip vs Number of Weekly Trips", fontsize=16)
plt.xlabel("Number of Trips per Week")
plt.ylabel("Cost per Trip (₽)")
plt.grid(True)
plt.legend(title="Ticket Type")
st.pyplot(plt.gcf())

decision = list(zip(
    ["one trip pass", "one month pass", "three month pass"],
    [onetrip, onemonth / 30 * 7/trips_per_week_input, threemonths / 90 * 7/trips_per_week_input]
))

bestchoice = min(decision, key=lambda x: x[1])

st.write(f"For **{trips_per_week_input} trips** per week, the best choice is to buy a **{bestchoice[0]}**.")
