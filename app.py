import streamlit as st
import math

# Custom CSS for improved UI with wider sidebar
st.markdown("""
<style>
    :root {
        --primary: #1a3c5e;
        --accent: #4CAF50;
        --background: #e6ecf0;
    }
    .main {
        background-color: var(--background);
        font-family: 'Arial', sans-serif;
    }
    .stSidebar {
        width: 350px !important;
        position: sticky;
        top: 0;
        height: 100vh;
        overflow-y: auto;
    }
    .stButton>button {
        background-color: var(--accent);
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stSelectbox, .stNumberInput, .stMultiSelect {
        background-color: white;
        border-radius: 4px;
        padding: 10px;
    }
    h1, h2, h3 {
        color: var(--primary);
    }
    .result {
        font-size: 24px;
        color: #2980b9;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .result:hover {
        transform: scale(1.05);
    }
    .note {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 4px;
        border-left: 4px solid #ffc107;
    }
    @media (max-width: 600px) {
        .stSidebar {
            width: 300px !important;
        }
        .stButton>button {
            font-size: 14px;
            padding: 8px 16px;
        }
        .stSelectbox, .stNumberInput, .stMultiSelect {
            padding: 8px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Unit definitions
length_units = {
    "millimeter (mm)": 0.001,
    "centimeter (cm)": 0.01,
    "meter (m)": 1,
    "kilometer (km)": 1000,
    "inch (in)": 0.0254,
    "foot (ft)": 0.3048,
    "yard (yd)": 0.9144,
    "mile (mi)": 1609.34
}

area_units = {
    "square meter (m²)": 1,
    "square kilometer (km²)": 1e6,
    "square foot (ft²)": 0.092903,
    "square yard (yd²)": 0.836127,
    "acre": 4046.86,
    "hectare": 10000,
    "square mile (mi²)": 2.58999e6
}

volume_units = {
    "cubic meter (m³)": 1,
    "liter (L)": 0.001,
    "cubic centimeter (cm³)": 1e-6,
    "barrel (bbl)": 0.158987,
    "US gallon (gal)": 0.00378541,
    "cubic foot (ft³)": 0.0283168,
    "acre-foot": 1233.48,
    "standard cubic foot (scf)": 0.0283168,
    "thousand standard cubic feet (mscf)": 28.3168,
    "million standard cubic feet (mmscfd)": 28316.8,
    "billion cubic feet (bcf)": 2.83168e7,
    "standard cubic meter (sm³)": 1
}

mass_units = {
    "gram (g)": 0.001,
    "kilogram (kg)": 1,
    "tonne (metric ton)": 1000,
    "pound (lb)": 0.453592,
    "short ton (US)": 907.185,
    "long ton (UK)": 1016.05
}

density_units = {
    "kg/m³": 1,
    "g/cm³": 1000,
    "lb/ft³": 16.0185,
    "lb/gal (US)": 119.826,
    "lb/bbl": 2.85301
}

pressure_units = {
    "Pascal (Pa)": 1,
    "kilopascal (kPa)": 1000,
    "megapascal (MPa)": 1e6,
    "bar": 1e5,
    "psi": 6894.76,
    "atmosphere (atm)": 101325,
    "mmHg (torr)": 133.322,
    "kg/cm²": 98066.5
}

force_units = {
    "Newton (N)": 1,
    "kilonewton (kN)": 1000,
    "pound-force (lbf)": 4.44822,
    "dyne": 1e-5,
    "kilopond (kp)": 9.80665
}

energy_units = {
    "Joule (J)": 1,
    "kilojoule (kJ)": 1000,
    "megajoule (MJ)": 1e6,
    "erg": 1e-7,
    "calorie (cal)": 4.184,
    "kilocalorie (kcal)": 4184,
    "British thermal unit (BTU)": 1055.06,
    "kilowatt-hour (kWh)": 3.6e6,
    "therm": 1.05506e8,
    "barrel of oil equivalent (boe)": 6.12e9,
    "tonne of oil equivalent (toe)": 4.1868e10
}

power_units = {
    "Watt (W)": 1,
    "kilowatt (kW)": 1000,
    "horsepower (hp)": 745.7,
    "metric horsepower (PS)": 735.499
}

dynamic_visc_units = {
    "Pascal-second (Pa·s)": 1,
    "centipoise (cP)": 0.001,
    "poise (P)": 0.1,
    "lb/(ft·s)": 1.48816
}

kinematic_visc_units = {
    "square meter per second (m²/s)": 1,
    "centistoke (cSt)": 1e-6,
    "stoke (St)": 1e-4,
    "square foot per second (ft²/s)": 0.092903
}

liquid_flow_units = {
    "cubic meter per second (m³/s)": 1,
    "cubic meter per hour (m³/h)": 1/3600,
    "cubic meter per day (m³/d)": 1/86400,
    "barrel per day (bpd)": 0.158987 / 86400,
    "US gallon per minute (gpm)": 0.00378541 / 60,
    "liter per second (L/s)": 0.001,
    "barrel per hour (bph)": 0.158987 / 3600
}

gas_flow_units = {
    "standard cubic meter per day (sm³/d)": 1,
    "thousand standard cubic feet per day (mscfd)": 0.0283168,
    "million standard cubic feet per day (mmscfd)": 28.3168,
    "billion cubic feet per day (bcfd)": 28316.8,
    "normal cubic meter per hour (nm³/h)": 24 / 1.0549,
    "standard cubic foot per hour (scfh)": 0.0283168 / 24
}

perm_units = {
    "square meter (m²)": 1,
    "Darcy (D)": 9.86923e-13,
    "millidarcy (mD)": 9.86923e-16
}

time_units = {
    "second (s)": 1,
    "minute (min)": 60,
    "hour (h)": 3600,
    "day (d)": 86400,
    "year (yr)": 31536000
}

velocity_units = {
    "meter per second (m/s)": 1,
    "foot per second (ft/s)": 0.3048,
    "kilometer per hour (km/h)": 1/3.6,
    "mile per hour (mph)": 0.44704
}

torque_units = {
    "Newton-meter (N·m)": 1,
    "foot-pound (ft·lb)": 1.35582,
    "inch-pound (in·lb)": 0.112985
}

gor_units = {
    "standard cubic meter per cubic meter (sm³/m³)": 1,
    "standard cubic foot per barrel (scf/bbl)": 0.178107,
    "normal cubic meter per cubic meter (nm³/m³)": 1.0549
}

conc_units = {
    "mg/L": 1,
    "ppm (parts per million)": 1,
    "g/L": 1000,
    "kg/m³": 1
}

heat_cap_units = {
    "J/kg·K": 1,
    "Btu/lb·°F": 4186.8
}

therm_cond_units = {
    "W/m·K": 1,
    "Btu/hr·ft·°F": 1.73073
}

angle_units = {
    "radian (rad)": 1,
    "degree (deg)": math.pi / 180
}

resist_units = {
    "ohm-meter (ohm·m)": 1,
    "ohm-foot (ohm·ft)": 0.3048
}

mud_units = {
    "Specific Gravity (SG)": 1,
    "pounds per gallon (ppg)": 1 / 8.3454,
    "lb/ft³": 1 / 62.428
}

rop_units = {
    "meter per hour (m/h)": 1,
    "foot per hour (ft/h)": 0.3048
}

# Unit Converter Class
class UnitConverter:
    def __init__(self):
        self.units = {
            "Length": length_units,
            "Area": area_units,
            "Volume": volume_units,
            "Mass": mass_units,
            "Density": density_units,
            "Pressure": pressure_units,
            "Force": force_units,
            "Energy": energy_units,
            "Power": power_units,
            "Dynamic Viscosity": dynamic_visc_units,
            "Kinematic Viscosity": kinematic_visc_units,
            "Liquid Flow Rate": liquid_flow_units,
            "Gas Flow Rate": gas_flow_units,
            "Permeability": perm_units,
            "Time": time_units,
            "Velocity": velocity_units,
            "Torque": torque_units,
            "Gas-Oil Ratio (GOR)": gor_units,
            "Salinity / Concentration": conc_units,
            "Thermal Properties": {"Heat Capacity": heat_cap_units, "Thermal Conductivity": therm_cond_units},
            "Angle": angle_units,
            "Conductivity / Resistivity": resist_units,
            "Mud Weight": mud_units,
            "Rate of Penetration (ROP)": rop_units
        }
        self.special_conversions = {
            "Temperature": self.convert_temperature,
            "API Gravity and Specific Gravity": self.convert_api_sg,
            "Angle": self.convert_angle,
        }

    def validate_input(self, category, value):
        invalid_negative = ["Length", "Mass", "Volume", "Area", "Density", "Time", "Permeability",
                           "Dynamic Viscosity", "Kinematic Viscosity", "Liquid Flow Rate", "Gas Flow Rate"]
        if category in invalid_negative and value < 0:
            raise ValueError(f"Negative values are not valid for {category}.")
        if category == "API Gravity and Specific Gravity" and value <= 0:
            raise ValueError("Invalid value for gravity (must be positive).")
        return True

    def get_units(self, category, thermal_sub=None):
        if category == "Thermal Properties":
            return self.units[category].get(thermal_sub, {})
        return self.units.get(category, {})

    def convert(self, category, from_unit, to_unit, value, thermal_sub=None, pvt_correction=1.0):
        self.validate_input(category, value)
        if category in self.special_conversions:
            return self.special_conversions[category](from_unit, to_unit, value)
        units = self.get_units(category, thermal_sub)
        if from_unit == to_unit:
            return value
        return value * units[from_unit] / units[to_unit] * pvt_correction

    def convert_temperature(self, from_unit, to_unit, value):
        temp_units = {
            "Celsius (°C)": lambda x: x,
            "Fahrenheit (°F)": lambda x: (x - 32) / 1.8,
            "Kelvin (K)": lambda x: x - 273.15,
            "Rankine (°R)": lambda x: (x - 491.67) / 1.8
        }
        to_celsius = temp_units[from_unit](value)
        return {
            "Celsius (°C)": to_celsius,
            "Fahrenheit (°F)": to_celsius * 1.8 + 32,
            "Kelvin (K)": to_celsius + 273.15,
            "Rankine (°R)": to_celsius * 1.8 + 491.67
        }[to_unit]

    def convert_api_sg(self, from_unit, to_unit, value):
        if from_unit == to_unit:
            return value
        if from_unit == "API Gravity (°API)":
            return 141.5 / (value + 131.5)
        return 141.5 / value - 131.5

    def convert_angle(self, from_unit, to_unit, value):
        factor_from = angle_units[from_unit]
        factor_to = angle_units[to_unit]
        return value * factor_from / factor_to

# Main app
st.title("Petroleum Engineering Unit Converter")
st.markdown("Comprehensive converter for petroleum engineering. Includes salinity, thermal properties, angles, resistivity, mud weight, and more. Notes on approximations are included where relevant.")

# Categories
categories = [
    "Length", "Area", "Volume", "Mass", "Density", "Temperature", "Pressure", "Force",
    "Energy", "Power", "Dynamic Viscosity", "Kinematic Viscosity", "Liquid Flow Rate",
    "Gas Flow Rate", "Permeability", "Time", "Velocity", "Torque", "Gas-Oil Ratio (GOR)",
    "API Gravity and Specific Gravity", "Salinity / Concentration", "Thermal Properties",
    "Angle", "Conductivity / Resistivity", "Mud Weight", "Rate of Penetration (ROP)"
]

# Sidebar inputs (permanent, not hidable)
st.sidebar.header("Conversion Inputs")
category = st.sidebar.selectbox("Select Category", categories, key="category_select")

# Initialize converter
converter = UnitConverter()

# Thermal Properties sub-selection
thermal_sub = None
if category == "Thermal Properties":
    thermal_type = ["Heat Capacity", "Thermal Conductivity"]
    thermal_sub = st.sidebar.selectbox("Thermal Sub-Category", thermal_type)

# Unit filtering (in expander to keep sidebar clean)
units = converter.get_units(category, thermal_sub)
with st.sidebar.expander("Filter Units"):
    selected_units = st.multiselect("Select Units to Display", list(units.keys()), default=list(units.keys()), key="unit_filter")
if not selected_units:
    selected_units = list(units.keys())

# Unit selection and value input (permanent, not in expander)
if category == "Temperature":
    temp_units = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Rankine (°R)"]
    from_unit = st.sidebar.selectbox("From Unit", temp_units, key="from_unit")
    to_unit = st.sidebar.selectbox("To Unit", temp_units, key="to_unit")
elif category == "API Gravity and Specific Gravity":
    grav_units = ["API Gravity (°API)", "Specific Gravity (SG at 60°F)"]
    from_unit = st.sidebar.selectbox("From Unit", grav_units, key="from_unit")
    to_unit = st.sidebar.selectbox("To Unit", grav_units, key="to_unit")
else:
    from_unit = st.sidebar.selectbox("From Unit", selected_units, key="from_unit")
    to_unit = st.sidebar.selectbox("To Unit", selected_units, key="to_unit")
value = st.sidebar.number_input("Value", value=0.0, key="value_input")

# Conversion button (permanent, not in expander)
st.sidebar.button("Convert", key="convert_button")

# Special calculations (in expanders)
if category == "Pressure":
    with st.sidebar.expander("Hydrostatic Pressure Calc"):
        st.info("Pressure (psi) = TVD (ft) * Mud Weight (ppg) * 0.052")
        tvd = st.number_input("TVD (ft)", value=1000.0)
        mud_ppg = st.number_input("Mud Weight (ppg)", value=8.33)
        hydro_pressure = tvd * mud_ppg * 0.052
        st.markdown(f"**Hydrostatic Pressure: {hydro_pressure:.2f} psi**")

if category == "Volume":
    with st.sidebar.expander("Drill Pipe Volume Calc"):
        st.info("Volume (bbl) = Length (ft) * (Inner Diameter (in)² / 1029.4)")
        length_ft = st.number_input("Pipe Length (ft)", value=1000.0)
        id_in = st.number_input("Pipe Inner Diameter (in)", value=4.0)
        volume_bbl = (length_ft * (id_in ** 2) / 1029.4)
        st.markdown(f"**Drill Pipe Volume: {volume_bbl:.2f} bbl**")

if category == "Gas-Oil Ratio (GOR)":
    with st.sidebar.expander("PVT Adjustments"):
        pressure_psia = st.number_input("Reservoir Pressure (psia)", value=14.7)
        temp_f = st.number_input("Reservoir Temperature (°F)", value=60.0)
        pvt_correction = (pressure_psia / 14.7) * ((temp_f + 460) / 520)
        st.info(f"PVT Correction Factor: {pvt_correction:.4f}")
else:
    pvt_correction = 1.0

# Conversion logic
if st.session_state.get("convert_button"):
    try:
        if value == 0:
            st.info("Zero value converts to zero.")
        result = converter.convert(category, from_unit, to_unit, value, thermal_sub, pvt_correction)
        formula = "Same unit" if from_unit == to_unit else f"{value} × ({units.get(from_unit, 1)} / {units.get(to_unit, 1)}) × {pvt_correction:.4f}"
        st.session_state.conversion_result = result
        st.session_state.conversion_formula = formula
        st.session_state.conversion_value = value
        st.session_state.result_from_unit = from_unit
        st.session_state.result_to_unit = to_unit
        st.markdown(f"<div class='result'>{value} {from_unit} = {result:.6f} {to_unit}</div>", unsafe_allow_html=True)
        st.info(f"Formula: {formula}")
    except ValueError as e:
        st.error(f"Conversion error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# Notes and approximations
if category == "Gas-Oil Ratio (GOR)":
    st.info("GOR: Surface conditions; reservoir GOR requires PVT data. Factor approx for std conditions (14.7 psia/60°F).")
if category == "Gas Flow Rate":
    st.info("Gas flow: Approximations use US std (14.7 psia/60°F). EU normal (1 atm/0°C) differs by ~5%.")

# Unit definitions
with st.expander("Unit Definitions"):
    st.markdown("""
    - **scf/bbl**: Standard cubic feet per barrel, used in Gas-Oil Ratio (GOR).
    - **mD**: Millidarcy, a unit of permeability for reservoir rocks.
    - **bbl**: Barrel, commonly used in oil and gas (1 bbl = 0.158987 m³).
    - **ppg**: Pounds per gallon, used for mud weight (1 ppg ≈ 0.119826 SG).
    - **API Gravity**: Measure of oil density, related to SG by SG = 141.5 / (API + 131.5).
    - **sm³/d**: Standard cubic meter per day, used for gas flow rates.
    """)

# Reset button
if st.sidebar.button("Reset", key="reset_button"):
    st.rerun()

st.markdown("---")
st.markdown("Enhanced for Petroleum Engineering | Built with ❤️")
