import streamlit as st

# Title
st.title("💀 Body Count Index (BCI) Calculator")
st.subheader("Not all body counts are equal")

# User manually inputs the number of partners
num_partners_input = st.text_input("Total partners:", value="")

# Validate input (ensure it's a number)
if num_partners_input.isdigit():
    num_partners = int(num_partners_input)
else:
    num_partners = 0

# Initialize total BCI score
total_bci = 0
show_result = False  # Controls when the verdict is displayed

# Multipliers
race_multiplier = {"White": 1.0, "Black": 2.0, "Latino": 1.3, "Asian": 0.8, "Indian": 1.5}
attractiveness_multiplier = {"Ugly": 1.2, "Average": 1.0, "Hot": 1.4, "Male Model": 1.8}
wealth_multiplier = {"Broke": 1.3, "Middle-class": 1.0, "Rich": 1.3, "Ultra Rich": 2.0}
relationship_duration_multiplier = {
    "One-night stand": 2.0,
    "Short-term (0-6 months)": 1.0,
    "Long-term (>6 months)": 0.8,
    "Toxic ex (On-again, off-again)": 1.5,
}
sex_position_multiplier = {
    "Missionary only": 0.7,
    "Standard positions (includes Missionary)": 1.0,
    "Rough (choking, spitting, etc.)": 2.0,
    "BDSM (restraints, pain, etc.)": 3.0,
    "Anal": 5.0,
    "Golden Shower / Degradation": 10.0,  # Ultimate outlier multiplier
}
sex_location_multiplier = {
    "Her place": 1.0,
    "His place": 1.3,
    "Vacation hookup": 1.8,
    "Italy/Dubai": 3.0,
    "Club bathroom": 2.5,
}

# Collect partner details only if num_partners is valid
partner_data = []
if num_partners > 0:
    for i in range(num_partners):
        st.subheader(f"Partner {i+1}")

        race = st.selectbox(f"Race of partner {i+1}:", ["Select..."] + list(race_multiplier.keys()), key=f"race_{i}")
        attractiveness = st.selectbox(
            f"Attractiveness of partner {i+1}:", ["Select..."] + list(attractiveness_multiplier.keys()), key=f"attractiveness_{i}"
        )
        wealth = st.selectbox(f"Wealth of partner {i+1}:", ["Select..."] + list(wealth_multiplier.keys()), key=f"wealth_{i}")
        relationship_duration = st.selectbox(
            f"Relationship duration with partner {i+1}:", ["Select..."] + list(relationship_duration_multiplier.keys()), key=f"relationship_{i}"
        )

        # Select the max sex position per partner
        sex_position = st.selectbox(
            f"Most extreme sex act with partner {i+1} (Listed in order of extremity):",
            ["Select..."] + list(sex_position_multiplier.keys()),
            key=f"sex_pos_{i}",
        )

        # Location applies ONLY if it's a one-night stand
        location_weight = 1.0  # Default weight unless changed
        if relationship_duration == "One-night stand":
            sex_location = st.selectbox(
                f"Location of sex with partner {i+1}:", ["Select..."] + list(sex_location_multiplier.keys()), key=f"sex_loc_{i}"
            )
            if sex_location != "Select...":
                location_weight = sex_location_multiplier[sex_location]

        # Ensure all selections are made before storing partner data
        if (
            race != "Select..."
            and attractiveness != "Select..."
            and wealth != "Select..."
            and relationship_duration != "Select..."
            and sex_position != "Select..."
        ):
            partner_data.append((race, attractiveness, wealth, relationship_duration, sex_position, location_weight))

# Only calculate when user presses the button
if st.button("Calculate BCI"):
    if len(partner_data) != num_partners:
        st.error("Please complete all selections for each partner before calculating.")
    else:
        show_result = True  # Enable results display

        # Compute BCI for each partner
        for data in partner_data:
            race, attractiveness, wealth, relationship_duration, sex_position, location_weight = data
            partner_bci = (
                race_multiplier[race]
                * attractiveness_multiplier[attractiveness]
                * wealth_multiplier[wealth]
                * relationship_duration_multiplier[relationship_duration]
                * sex_position_multiplier[sex_position]
                * location_weight
            )
            total_bci += partner_bci

# Display results **only after calculation**
if show_result:
    st.subheader("Final Body Count Index Score:")
    st.write(f"🔥 **{total_bci:.2f}** 🔥")

    # BCI Verdict System
    if num_partners == 0:
        verdict = "🕊️ **Virgin Queen** – Uncorrupted, Pure Soul. Marry her now, king."
    elif total_bci < 10:
        verdict = "💍 Wifey Material: Low mileage, minimal damage. A solid investment."
    elif 10 <= total_bci < 25:
        verdict = "🛠️ Salvageable: Some wear and tear, but still has potential with the right man."
    elif 25 <= total_bci < 50:
        verdict = "🚨 Ran Through: She’s been places. Proceed with extreme caution."
    else:
        verdict = "🛑 FOR THE STREETS: Past the point of no return. Do not fall in love."

    st.subheader("🚨 Verdict:")
    st.write(f"**{verdict}**")

    st.markdown("---")
    st.markdown("🔗 **Share your results & spread the awareness.**")
