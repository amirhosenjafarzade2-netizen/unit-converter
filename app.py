import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Petroleum Engineering Unit Converter Pro",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #1a3c5e;
        --primary-light: #2d5985;
        --accent: #4CAF50;
        --accent-hover: #45a049;
        --background: #f5f7fa;
        --card-bg: #ffffff;
        --border: #e0e6ed;
        --text-primary: #2c3e50;
        --text-secondary: #7f8c8d;
        --success: #27ae60;
        --warning: #f39c12;
        --danger: #e74c3c;
        --info: #3498db;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        background-color: var(--background);
        border-radius: 12px;
        padding: 2rem;
    }
    
    .stSidebar {
        background-color: var(--card-bg) !important;
        border-right: 1px solid var(--border);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--accent) 0%, #2ecc71 100%);
        color: white;
        border: none;
        padding: 12px 28px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        font-weight: 600;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        margin: 1.5rem 0;
        color: white;
    }
    
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .result-label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .metric-card {
        background-color: var(--card-bg);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid var(--accent);
        margin: 1rem 0;
    }
    
    .metric-title {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.75rem;
        color: var(--text-primary);
        font-weight: 700;
    }
    
    .history-item {
        background-color: var(--card-bg);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid var(--accent);
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateX(4px);
    }
    
    .favorite-badge {
        background-color: #ffd700;
        color: #000;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    h1 {
        color: var(--primary);
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--primary);
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 2rem;
    }
    
    h3 {
        color: var(--primary-light);
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .stExpander {
        background-color: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .quick-convert-chip {
        display: inline-block;
        background-color: var(--card-bg);
        padding: 8px 16px;
        margin: 4px;
        border-radius: 20px;
        border: 2px solid var(--accent);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .quick-convert-chip:hover {
        background-color: var(--accent);
        color: white;
        transform: scale(1.05);
    }
    
    @media (max-width: 768px) {
        .result-value {
            font-size: 2rem;
        }
        h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'conversion_count' not in st.session_state:
    st.session_state.conversion_count = 0

# Unit definitions (comprehensive)
length_units = {
    "millimeter (mm)": 0.001,
    "centimeter (cm)": 0.01,
    "meter (m)": 1,
    "kilometer (km)": 1000,
    "inch (in)": 0.0254,
    "foot (ft)": 0.3048,
    "yard (yd)": 0.9144,
    "mile (mi)": 1609.34,
    "nautical mile (nmi)": 1852
}

area_units = {
    "square millimeter (mm²)": 1e-6,
    "square centimeter (cm²)": 1e-4,
    "square meter (m²)": 1,
    "square kilometer (km²)": 1e6,
    "square inch (in²)": 0.00064516,
    "square foot (ft²)": 0.092903,
    "square yard (yd²)": 0.836127,
    "acre": 4046.86,
    "hectare (ha)": 10000,
    "square mile (mi²)": 2.58999e6
}

volume_units = {
    "cubic millimeter (mm³)": 1e-9,
    "cubic centimeter (cm³)": 1e-6,
    "cubic meter (m³)": 1,
    "liter (L)": 0.001,
    "milliliter (mL)": 1e-6,
    "barrel (bbl)": 0.158987,
    "US gallon (gal)": 0.00378541,
    "imperial gallon (UK gal)": 0.00454609,
    "cubic foot (ft³)": 0.0283168,
    "cubic inch (in³)": 1.63871e-5,
    "acre-foot": 1233.48,
    "standard cubic foot (scf)": 0.0283168,
    "thousand standard cubic feet (mscf)": 28.3168,
    "million standard cubic feet (mmscf)": 28316.8,
    "billion cubic feet (bcf)": 2.83168e7,
    "standard cubic meter (sm³)": 1
}

mass_units = {
    "milligram (mg)": 1e-6,
    "gram (g)": 0.001,
    "kilogram (kg)": 1,
    "tonne (metric ton)": 1000,
    "ounce (oz)": 0.0283495,
    "pound (lb)": 0.453592,
    "short ton (US)": 907.185,
    "long ton (UK)": 1016.05
}

density_units = {
    "kg/m³": 1,
    "g/cm³": 1000,
    "g/mL": 1000,
    "lb/ft³": 16.0185,
    "lb/gal (US)": 119.826,
    "lb/bbl": 2.85301,
    "g/L": 1
}

pressure_units = {
    "Pascal (Pa)": 1,
    "kilopascal (kPa)": 1000,
    "megapascal (MPa)": 1e6,
    "bar": 1e5,
    "millibar (mbar)": 100,
    "psi": 6894.76,
    "ksi (1000 psi)": 6.89476e6,
    "atmosphere (atm)": 101325,
    "mmHg (torr)": 133.322,
    "kg/cm²": 98066.5,
    "kg/m²": 9.80665
}

force_units = {
    "Newton (N)": 1,
    "kilonewton (kN)": 1000,
    "meganewton (MN)": 1e6,
    "pound-force (lbf)": 4.44822,
    "kilogram-force (kgf)": 9.80665,
    "dyne": 1e-5,
    "kilopond (kp)": 9.80665
}

energy_units = {
    "Joule (J)": 1,
    "kilojoule (kJ)": 1000,
    "megajoule (MJ)": 1e6,
    "gigajoule (GJ)": 1e9,
    "erg": 1e-7,
    "calorie (cal)": 4.184,
    "kilocalorie (kcal)": 4184,
    "British thermal unit (BTU)": 1055.06,
    "kilowatt-hour (kWh)": 3.6e6,
    "megawatt-hour (MWh)": 3.6e9,
    "therm": 1.05506e8,
    "barrel of oil equivalent (boe)": 6.12e9,
    "tonne of oil equivalent (toe)": 4.1868e10,
    "foot-pound (ft·lbf)": 1.35582
}

power_units = {
    "Watt (W)": 1,
    "kilowatt (kW)": 1000,
    "megawatt (MW)": 1e6,
    "gigawatt (GW)": 1e9,
    "horsepower (hp)": 745.7,
    "metric horsepower (PS)": 735.499,
    "BTU/hour": 0.293071,
    "ton of refrigeration": 3516.85
}

dynamic_visc_units = {
    "Pascal-second (Pa·s)": 1,
    "centipoise (cP)": 0.001,
    "millipascal-second (mPa·s)": 0.001,
    "poise (P)": 0.1,
    "lb/(ft·s)": 1.48816,
    "lb/(ft·hr)": 0.000413378
}

kinematic_visc_units = {
    "square meter per second (m²/s)": 1,
    "centistoke (cSt)": 1e-6,
    "stoke (St)": 1e-4,
    "square millimeter per second (mm²/s)": 1e-6,
    "square foot per second (ft²/s)": 0.092903
}

liquid_flow_units = {
    "cubic meter per second (m³/s)": 1,
    "cubic meter per hour (m³/h)": 1/3600,
    "cubic meter per day (m³/d)": 1/86400,
    "barrel per second (bps)": 0.158987,
    "barrel per minute (bpm)": 0.158987 / 60,
    "barrel per hour (bph)": 0.158987 / 3600,
    "barrel per day (bpd)": 0.158987 / 86400,
    "US gallon per minute (gpm)": 0.00378541 / 60,
    "US gallon per hour (gph)": 0.00378541 / 3600,
    "liter per second (L/s)": 0.001,
    "liter per minute (L/min)": 0.001 / 60,
    "liter per hour (L/h)": 0.001 / 3600
}

gas_flow_units = {
    "standard cubic meter per day (sm³/d)": 1,
    "standard cubic meter per hour (sm³/h)": 24,
    "thousand standard cubic feet per day (mscfd)": 28.3168,
    "million standard cubic feet per day (mmscfd)": 28316.8,
    "billion cubic feet per day (bcfd)": 2.83168e7,
    "normal cubic meter per hour (nm³/h)": 24 / 1.0549,
    "normal cubic meter per day (nm³/d)": 1 / 1.0549,
    "standard cubic foot per hour (scfh)": 0.0283168 / 24,
    "standard cubic foot per day (scfd)": 0.0283168
}

perm_units = {
    "square meter (m²)": 1,
    "Darcy (D)": 9.86923e-13,
    "millidarcy (mD)": 9.86923e-16,
    "microdarcy (μD)": 9.86923e-19
}

time_units = {
    "microsecond (μs)": 1e-6,
    "millisecond (ms)": 0.001,
    "second (s)": 1,
    "minute (min)": 60,
    "hour (h)": 3600,
    "day (d)": 86400,
    "week": 604800,
    "month (30 days)": 2592000,
    "year (yr)": 31536000
}

velocity_units = {
    "meter per second (m/s)": 1,
    "kilometer per hour (km/h)": 1/3.6,
    "foot per second (ft/s)": 0.3048,
    "foot per minute (ft/min)": 0.00508,
    "mile per hour (mph)": 0.44704,
    "knot (nautical mile/h)": 0.514444
}

torque_units = {
    "Newton-meter (N·m)": 1,
    "kilonewton-meter (kN·m)": 1000,
    "foot-pound (ft·lb)": 1.35582,
    "foot-pound-force (ft·lbf)": 1.35582,
    "inch-pound (in·lb)": 0.112985,
    "dyne-centimeter (dyn·cm)": 1e-7
}

gor_units = {
    "standard cubic meter per cubic meter (sm³/m³)": 1,
    "standard cubic foot per barrel (scf/bbl)": 0.178107,
    "normal cubic meter per cubic meter (nm³/m³)": 1.0549,
    "cubic foot per barrel (cf/bbl)": 0.178107
}

conc_units = {
    "milligram per liter (mg/L)": 1,
    "parts per million (ppm)": 1,
    "gram per liter (g/L)": 1000,
    "kilogram per cubic meter (kg/m³)": 1,
    "parts per billion (ppb)": 0.001,
    "percent (%)": 10000,
    "pound per million gallon (lb/Mgal)": 0.119826
}

heat_cap_units = {
    "J/(kg·K)": 1,
    "kJ/(kg·K)": 1000,
    "cal/(g·°C)": 4186.8,
    "Btu/(lb·°F)": 4186.8
}

therm_cond_units = {
    "W/(m·K)": 1,
    "cal/(cm·s·°C)": 418.68,
    "Btu/(hr·ft·°F)": 1.73073,
    "Btu·in/(hr·ft²·°F)": 0.144228
}

angle_units = {
    "radian (rad)": 1,
    "degree (deg or °)": math.pi / 180,
    "gradian (grad)": math.pi / 200,
    "minute of arc (')" : math.pi / 10800,
    "second of arc (\")" : math.pi / 648000
}

resist_units = {
    "ohm-meter (Ω·m)": 1,
    "ohm-centimeter (Ω·cm)": 0.01,
    "ohm-foot (Ω·ft)": 0.3048
}

mud_units = {
    "Specific Gravity (SG)": 1,
    "pounds per gallon (ppg)": 1 / 8.3454,
    "pounds per cubic foot (lb/ft³)": 1 / 62.428,
    "kilograms per cubic meter (kg/m³)": 1 / 1000,
    "grams per cubic centimeter (g/cm³)": 1
}

rop_units = {
    "meter per hour (m/h)": 1,
    "meter per minute (m/min)": 60,
    "foot per hour (ft/h)": 0.3048,
    "foot per minute (ft/min)": 18.288
}

productivity_units = {
    "barrel per day per psi (bpd/psi)": 1,
    "cubic meter per day per bar (m³/d/bar)": 6.89476 / 0.158987,
    "cubic meter per day per kPa (m³/d/kPa)": 0.00689476 / 0.158987
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
            "Heat Capacity": heat_cap_units,
            "Thermal Conductivity": therm_cond_units,
            "Angle": angle_units,
            "Electrical Resistivity": resist_units,
            "Mud Weight": mud_units,
            "Rate of Penetration (ROP)": rop_units,
            "Productivity Index": productivity_units
        }
        self.special_conversions = {
            "Temperature": self.convert_temperature,
            "API Gravity ↔ Specific Gravity": self.convert_api_sg,
        }

    def validate_input(self, category, value):
        """Validate input values based on category"""
        invalid_negative = [
            "Length", "Mass", "Volume", "Area", "Density", "Time", "Permeability",
            "Dynamic Viscosity", "Kinematic Viscosity", "Liquid Flow Rate", 
            "Gas Flow Rate", "Energy", "Power", "Force"
        ]
        if category in invalid_negative and value < 0:
            raise ValueError(f"Negative values are not valid for {category}.")
        if category == "API Gravity ↔ Specific Gravity" and value <= 0:
            raise ValueError("Invalid value for gravity (must be positive).")
        return True

    def get_units(self, category):
        """Get available units for a category"""
        return self.units.get(category, {})

    def convert(self, category, from_unit, to_unit, value, pvt_correction=1.0):
        """Convert value from one unit to another"""
        self.validate_input(category, value)
        
        if category in self.special_conversions:
            return self.special_conversions[category](from_unit, to_unit, value)
        
        units = self.get_units(category)
        if from_unit == to_unit:
            return value
        
        # Convert to base unit, then to target unit
        base_value = value * units[from_unit]
        result = base_value / units[to_unit] * pvt_correction
        return result

    def convert_temperature(self, from_unit, to_unit, value):
        """Convert temperature between different scales"""
        temp_units = {
            "Celsius (°C)": lambda x: x,
            "Fahrenheit (°F)": lambda x: (x - 32) / 1.8,
            "Kelvin (K)": lambda x: x - 273.15,
            "Rankine (°R)": lambda x: (x - 491.67) / 1.8
        }
        
        # Convert to Celsius first
        to_celsius = temp_units[from_unit](value)
        
        # Convert from Celsius to target
        return {
            "Celsius (°C)": to_celsius,
            "Fahrenheit (°F)": to_celsius * 1.8 + 32,
            "Kelvin (K)": to_celsius + 273.15,
            "Rankine (°R)": to_celsius * 1.8 + 491.67
        }[to_unit]

    def convert_api_sg(self, from_unit, to_unit, value):
        """Convert between API Gravity and Specific Gravity"""
        if from_unit == to_unit:
            return value
        if from_unit == "API Gravity (°API)":
            return 141.5 / (value + 131.5)
        return 141.5 / value - 131.5

# Initialize converter
converter = UnitConverter()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🛢️ Petroleum Engineering Unit Converter Pro")
    st.markdown("*Professional-grade unit conversion with advanced features*")
with col2:
    st.metric("Total Conversions", st.session_state.conversion_count)

# Categories
categories = [
    "Length", "Area", "Volume", "Mass", "Density", "Temperature", "Pressure", 
    "Force", "Energy", "Power", "Dynamic Viscosity", "Kinematic Viscosity", 
    "Liquid Flow Rate", "Gas Flow Rate", "Permeability", "Time", "Velocity", 
    "Torque", "Gas-Oil Ratio (GOR)", "API Gravity ↔ Specific Gravity", 
    "Salinity / Concentration", "Heat Capacity", "Thermal Conductivity", 
    "Angle", "Electrical Resistivity", "Mud Weight", "Rate of Penetration (ROP)",
    "Productivity Index"
]

# Sidebar
with st.sidebar:
    st.header("⚙️ Conversion Settings")
    
    # Handle favorite selection if requested
    favorite_category = st.session_state.get('favorite_selected')
    if favorite_category:
        del st.session_state.favorite_selected
    
    # Handle reuse conversion if requested
    reuse_category = None
    reuse_value = None
    if st.session_state.get('reuse_conversion'):
        reuse_entry = st.session_state.reuse_conversion
        reuse_category = reuse_entry['category']
        reuse_value = reuse_entry['from_value']
        del st.session_state.reuse_conversion
    
    # Determine default category (priority: favorite > reuse > default)
    if favorite_category and favorite_category in categories:
        default_category = categories.index(favorite_category)
    elif reuse_category and reuse_category in categories:
        default_category = categories.index(reuse_category)
    else:
        default_category = 0
    
    # Category selection
    category = st.selectbox(
        "📊 Select Category",
        categories,
        index=default_category,
        key="category_select",
        help="Choose the type of unit conversion you want to perform"
    )
    
    # Add to favorites
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("⭐", help="Add to favorites"):
            if category not in st.session_state.favorites:
                st.session_state.favorites.append(category)
                st.success("Added!")
    
    st.markdown("---")
    
    # Handle swap units if requested
    swap_from = None
    swap_to = None
    if st.session_state.get('swap_units'):
        swap_from = st.session_state.get('to_unit')
        swap_to = st.session_state.get('from_unit')
        st.session_state.swap_units = False
    
    # Unit selection
    units = converter.get_units(category)
    
    if category == "Temperature":
        temp_units = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Rankine (°R)"]
        default_from = temp_units.index(swap_from) if swap_from and swap_from in temp_units else 0
        default_to = temp_units.index(swap_to) if swap_to and swap_to in temp_units else 1
        from_unit = st.selectbox("🔵 From Unit", temp_units, index=default_from, key="from_unit")
        to_unit = st.selectbox("🔴 To Unit", temp_units, index=default_to, key="to_unit")
    elif category == "API Gravity ↔ Specific Gravity":
        grav_units = ["API Gravity (°API)", "Specific Gravity (SG at 60°F)"]
        default_from = grav_units.index(swap_from) if swap_from and swap_from in grav_units else 0
        default_to = grav_units.index(swap_to) if swap_to and swap_to in grav_units else 1
        from_unit = st.selectbox("🔵 From Unit", grav_units, index=default_from, key="from_unit")
        to_unit = st.selectbox("🔴 To Unit", grav_units, index=default_to, key="to_unit")
    else:
        unit_list = list(units.keys())
        default_from = unit_list.index(swap_from) if swap_from and swap_from in unit_list else 0
        default_to = unit_list.index(swap_to) if swap_to and swap_to in unit_list else (1 if len(unit_list) > 1 else 0)
        from_unit = st.selectbox("🔵 From Unit", unit_list, index=default_from, key="from_unit")
        to_unit = st.selectbox("🔴 To Unit", unit_list, index=default_to, key="to_unit")
    
    # Value input with scientific notation support
    st.markdown("---")
    
    # Check if there's a multiplier value or reuse value to use
    if reuse_value is not None:
        default_value = reuse_value
    else:
        default_value = st.session_state.get('multiplier_value', 0.0)
        if 'multiplier_value' in st.session_state:
            del st.session_state.multiplier_value
    
    value = st.number_input(
        "💯 Value",
        value=default_value,
        format="%.6f",
        key="value_input",
        help="Enter the value you want to convert"
    )
    
    # Quick multipliers
    st.markdown("**Quick Multipliers:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("×10"):
            st.session_state.multiplier_value = value * 10
            st.rerun()
    with col2:
        if st.button("×100"):
            st.session_state.multiplier_value = value * 100
            st.rerun()
    with col3:
        if st.button("÷10"):
            st.session_state.multiplier_value = value / 10
            st.rerun()
    
    st.markdown("---")
    
    # Conversion button
    convert_button = st.button("🔄 Convert", use_container_width=True, type="primary")
    
    # Swap units button
    if st.button("⇅ Swap Units", use_container_width=True):
        # Store swap instruction
        st.session_state.swap_units = True
        st.rerun()
    
    # PVT Correction for GOR
    pvt_correction = 1.0
    if category == "Gas-Oil Ratio (GOR)":
        st.markdown("---")
        with st.expander("⚗️ PVT Adjustments"):
            pressure_psia = st.number_input("Reservoir Pressure (psia)", value=14.7, min_value=0.0)
            temp_f = st.number_input("Reservoir Temperature (°F)", value=60.0)
            pvt_correction = (pressure_psia / 14.7) * ((temp_f + 460) / 520)
            st.info(f"PVT Correction Factor: **{pvt_correction:.4f}**")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["🔄 Converter", "📊 Batch Convert", "📜 History", "🧮 Calculators"])

with tab1:
    # Conversion result
    if convert_button or st.session_state.get("auto_convert"):
        try:
            if value == 0:
                st.info("💡 Zero value converts to zero in any unit system.")
                result = 0
            else:
                result = converter.convert(category, from_unit, to_unit, value, pvt_correction)
            
            # Display result in beautiful card
            st.markdown(f"""
                <div class='result-card'>
                    <div class='result-label'>From: {value:,.6f} {from_unit}</div>
                    <div class='result-value'>{result:,.8g}</div>
                    <div class='result-label'>To: {to_unit}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Show conversion formula
            with st.expander("📐 Conversion Formula & Details"):
                if from_unit == to_unit:
                    st.write("✅ Same unit - no conversion needed")
                else:
                    if category not in converter.special_conversions:
                        units = converter.get_units(category)
                        from_factor = units.get(from_unit, 1)
                        to_factor = units.get(to_unit, 1)
                        st.latex(f"Result = {value} \\times \\frac{{{from_factor}}}{{{to_factor}}} \\times {pvt_correction}")
                    st.code(f"{value} {from_unit} = {result:.8g} {to_unit}")
            
            # Scientific notation
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Scientific Notation:** {result:.4e}")
            with col2:
                st.info(f"**Precision:** {len(str(result).split('.')[-1])} decimal places")
            
            # Add to history
            history_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": category,
                "from_value": value,
                "from_unit": from_unit,
                "to_value": result,
                "to_unit": to_unit,
                "pvt_correction": pvt_correction
            }
            st.session_state.conversion_history.insert(0, history_entry)
            if len(st.session_state.conversion_history) > 50:
                st.session_state.conversion_history.pop()
            st.session_state.conversion_count += 1
            
        except ValueError as e:
            st.error(f"❌ Conversion error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
    
    # Quick reference table
    if category not in ["Temperature", "API Gravity ↔ Specific Gravity"]:
        with st.expander(f"📋 Quick Reference Table - {category}"):
            try:
                test_value = 1.0
                results = []
                units_dict = converter.get_units(category)
                
                for unit in list(units_dict.keys())[:10]:  # Limit to first 10 units
                    try:
                        converted = converter.convert(category, from_unit, unit, test_value, pvt_correction)
                        results.append({
                            "Unit": unit,
                            f"Value (from 1 {from_unit})": f"{converted:.6g}"
                        })
                    except:
                        pass
                
                if results:
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            except:
                st.warning("Reference table not available for this category")

with tab2:
    st.subheader("📊 Batch Unit Conversion")
    st.markdown("Convert multiple values at once")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file with values to convert",
        type=['csv'],
        help="CSV should have a column named 'value' with numbers to convert"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        batch_values = st.text_area(
            "Or enter values (one per line):",
            height=150,
            placeholder="10\n20\n30\n40\n50"
        )
    
    if st.button("🔄 Convert Batch", type="primary"):
        values_to_convert = []
        
        # Get values from file or text area
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            if 'value' in df.columns:
                values_to_convert = df['value'].tolist()
        elif batch_values:
            values_to_convert = [float(v.strip()) for v in batch_values.split('\n') if v.strip()]
        
        if values_to_convert:
            results = []
            for val in values_to_convert:
                try:
                    converted = converter.convert(category, from_unit, to_unit, val, pvt_correction)
                    results.append({
                        "Input Value": val,
                        "Input Unit": from_unit,
                        "Output Value": converted,
                        "Output Unit": to_unit
                    })
                except Exception as e:
                    results.append({
                        "Input Value": val,
                        "Input Unit": from_unit,
                        "Output Value": "Error",
                        "Output Unit": str(e)
                    })
            
            # Display results
            df_results = pd.DataFrame(results)
            st.dataframe(df_results, use_container_width=True, hide_index=True)
            
            # Download button
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"batch_conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Please provide values to convert")

with tab3:
    st.subheader("📜 Conversion History")
    
    if st.session_state.conversion_history:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear History"):
                st.session_state.conversion_history = []
                st.rerun()
        
        # Display history
        for i, entry in enumerate(st.session_state.conversion_history[:20]):  # Show last 20
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.markdown(f"**{entry['timestamp']}**")
                    st.caption(entry['category'])
                with col2:
                    st.markdown(f"`{entry['from_value']:.4g}` {entry['from_unit']} → `{entry['to_value']:.4g}` {entry['to_unit']}")
                with col3:
                    if st.button("↺", key=f"reuse_{i}", help="Reuse this conversion"):
                        st.session_state.reuse_conversion = entry
                        st.rerun()
                st.markdown("---")
        
        # Export history
        if st.button("📥 Export History as JSON"):
            json_str = json.dumps(st.session_state.conversion_history, indent=2)
            st.download_button(
                label="Download History",
                data=json_str,
                file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    else:
        st.info("📭 No conversion history yet. Start converting to build your history!")

with tab4:
    st.subheader("🧮 Petroleum Engineering Calculators")
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        with st.expander("💧 Hydrostatic Pressure Calculator", expanded=True):
            st.markdown("**Formula:** `P = 0.052 × TVD × MW`")
            tvd = st.number_input("True Vertical Depth (ft)", value=10000.0, min_value=0.0, key="tvd_hp")
            mud_weight = st.number_input("Mud Weight (ppg)", value=9.0, min_value=0.0, key="mw_hp")
            
            hydro_pressure = tvd * mud_weight * 0.052
            
            st.success(f"**Hydrostatic Pressure:** {hydro_pressure:,.2f} psi")
            st.info(f"**In bar:** {hydro_pressure * 0.0689476:,.2f} bar")
            st.info(f"**In MPa:** {hydro_pressure * 0.00689476:,.3f} MPa")
        
        with st.expander("🔄 Drill Pipe Capacity/Displacement"):
            st.markdown("**Pipe Capacity Formula:** `V = L × ID² / 1029.4` (bbl)")
            st.markdown("**Pipe Displacement Formula:** `V = L × OD² / 1029.4` (bbl)")
            
            calc_type = st.radio("Calculate:", ["Capacity", "Displacement"], horizontal=True)
            
            length_ft = st.number_input("Pipe Length (ft)", value=10000.0, min_value=0.0, key="length_pipe")
            
            if calc_type == "Capacity":
                id_in = st.number_input("Inner Diameter (in)", value=4.276, min_value=0.0, key="id_pipe")
                volume_bbl = length_ft * (id_in ** 2) / 1029.4
                st.success(f"**Pipe Capacity:** {volume_bbl:,.3f} bbl")
            else:
                od_in = st.number_input("Outer Diameter (in)", value=5.0, min_value=0.0, key="od_pipe")
                volume_bbl = length_ft * (od_in ** 2) / 1029.4
                st.success(f"**Pipe Displacement:** {volume_bbl:,.3f} bbl")
            
            st.info(f"**In cubic meters:** {volume_bbl * 0.158987:,.3f} m³")
            st.info(f"**In gallons:** {volume_bbl * 42:,.1f} gal")
    
    with calc_col2:
        with st.expander("📊 Annular Velocity Calculator", expanded=True):
            st.markdown("**Formula:** `V = Q / (2.448 × (D² - d²))`")
            st.markdown("Where V = velocity (ft/min), Q = flow rate (gpm)")
            
            flow_rate = st.number_input("Flow Rate (gpm)", value=500.0, min_value=0.0, key="flow_av")
            hole_dia = st.number_input("Hole Diameter (in)", value=8.5, min_value=0.0, key="hole_av")
            pipe_od = st.number_input("Pipe OD (in)", value=5.0, min_value=0.0, key="pipe_av")
            
            if hole_dia > pipe_od:
                ann_velocity = flow_rate / (2.448 * (hole_dia**2 - pipe_od**2))
                st.success(f"**Annular Velocity:** {ann_velocity:,.2f} ft/min")
                st.info(f"**In ft/sec:** {ann_velocity/60:,.3f} ft/sec")
                st.info(f"**In m/min:** {ann_velocity * 0.3048:,.2f} m/min")
            else:
                st.error("⚠️ Hole diameter must be larger than pipe OD")
        
        with st.expander("⚡ Pump Pressure Required"):
            st.markdown("**Simplified Formula:** `ΔP = (Δρ × D × 0.052) + P_friction`")
            
            depth = st.number_input("Depth (ft)", value=10000.0, min_value=0.0, key="depth_pp")
            mud_density = st.number_input("Mud Density (ppg)", value=10.0, min_value=0.0, key="mud_pp")
            friction_loss = st.number_input("Estimated Friction Loss (psi)", value=500.0, min_value=0.0, key="friction_pp")
            
            hydrostatic = depth * mud_density * 0.052
            total_pressure = hydrostatic + friction_loss
            
            st.success(f"**Total Pump Pressure:** {total_pressure:,.0f} psi")
            st.info(f"**Hydrostatic Component:** {hydrostatic:,.0f} psi")
            st.info(f"**Friction Component:** {friction_loss:,.0f} psi")

# Footer with useful references
st.markdown("---")

with st.expander("📚 Common Unit Definitions & References"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Oil & Gas Units:**
        - **bbl**: Barrel (42 US gallons)
        - **bpd**: Barrels per day
        - **scf**: Standard cubic feet
        - **mscf**: Thousand standard cubic feet
        - **mmscf**: Million standard cubic feet
        - **bcf**: Billion cubic feet
        """)
    
    with col2:
        st.markdown("""
        **Reservoir Units:**
        - **mD**: Millidarcy (permeability)
        - **API°**: API Gravity
        - **GOR**: Gas-Oil Ratio
        - **ppg**: Pounds per gallon
        - **psi**: Pounds per square inch
        - **cP**: Centipoise (viscosity)
        """)
    
    with col3:
        st.markdown("""
        **Important Formulas:**
        - **SG = 141.5 / (API + 131.5)**
        - **P(psi) = 0.052 × TVD × MW**
        - **1 bbl = 0.158987 m³**
        - **1 bbl = 42 US gallons**
        - **1 ft = 0.3048 m**
        - **Standard conditions: 14.7 psia, 60°F**
        """)

with st.expander("⚠️ Important Notes & Assumptions"):
    st.markdown("""
    - **Temperature Conversions**: Formulas assume absolute temperature scales where applicable
    - **GOR Calculations**: Standard conditions are 14.7 psia and 60°F unless PVT corrections are applied
    - **Gas Flow Rates**: US standard conditions (14.7 psia/60°F) vs Normal conditions (1 atm/0°C) differ by ~5%
    - **Mud Weight**: Conversions assume fresh water equivalent at 60°F
    - **Permeability**: Darcy conversions assume isotropic, homogeneous media
    - **API Gravity**: Formula assumes 60°F reference temperature
    - **Pressure**: Gauge pressure vs absolute pressure - verify your application requirements
    """)

# Favorites sidebar
if st.session_state.favorites:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ⭐ Favorites")
        for fav in st.session_state.favorites:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(fav, key=f"fav_{fav}", use_container_width=True):
                    st.session_state.favorite_selected = fav
                    st.rerun()
            with col2:
                if st.button("✖", key=f"remove_{fav}", help="Remove from favorites"):
                    st.session_state.favorites.remove(fav)
                    st.rerun()

# Auto-save preferences
st.sidebar.markdown("---")
st.sidebar.caption("💾 Your conversion history and favorites are saved for this session")
