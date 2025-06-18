import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")  # active le style seaborn

st.title("Moscow Metro Ticket Selector")

trips_per_week_input = st.number_input("Number of trips per week", min_value=1, max_value=15, value=10)

# Colonnes : inputs à gauche, graphique à droite
col1, col2 = st.columns([1, 2])


with col1:
    onetrip = st.number_input("Price for 1 trip (₽)", value=67)
    onemonth = st.number_input("Price for 1-month pass (₽)", value=3160)
    threemonths = st.number_input("Price for 3-month pass (₽)", value=7650)

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

with col2:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_long, x="Trips per week", y="Cost per Trip (₽)", hue="Ticket Type", marker="o")
    plt.axvline(x=trips_per_week_input, color='red', linestyle='--', linewidth=2)
    plt.title("Cost per Trip vs Number of Weekly Trips", fontsize=16)
    plt.xlabel("Number of Trips per Week")
    plt.ylabel("Cost per Trip (₽)")
    plt.grid(True)
    plt.legend(title="Ticket Type")
    st.pyplot(plt.gcf())

st.write(f"""For {trips_per_week_input} trips per week, the cost is:
- {onetrip*trips_per_week_input}r. with one trip payments ({74*trips_per_week_input}r. if you pay per bank card),
- {onemonth/30*7:.0f}r. with a one month pass,
- {threemonths/90*7:.0f}r. with a three month pass.""")
