fueltype = "Lignite"

# Uncertainties in these values: CoalBiomass was a guess, the rest use HHV rather than LHV
# All the efficiencies are dodgy at this stage
if fueltype == "CoalBiomass":
    E = 0.35
    HHV = 20
    q = 0.5
elif fueltype == "Anthracite":
    E = 0.35
    HHV = 32.6
    q = 0.92
elif fueltype == "Bituminous":
    E = 0.35
    HHV = 30.2
    q = 0.65
elif fueltype == "Lignite":
    E = 0.35
    HHV = 14.0
    q = 0.3
elif fueltype == "Subbituminous":
    E = 0.35
    HHV = 24.4
    q = 0.4
elif fueltype == "NaturalGas":
    E = 0.5
    HHV = 52.2
    q = 0.75
elif fueltype == "Nuclear":
    E = 0.4
    HHV = 500000.0
    q = 0
elif fueltype == "Oil":
    E = 0.45
    HHV = 41.7
    q = 0.85
else:
    E = 0
    HHV = 0
    q = 0
    print("This fuel type isn't in the list!")
    quit()

# print("The fuel type is", fueltype + ".", "It has a rough efficiency of", str(E) + ",", "a HHV of", str(HHV), "MJ/kg and a carbon content of", str(q) + ".")

kgCO2perMJe = (44/12) * q / (E * HHV)
# print(round(kgCO2perMJe, 3))

print(fueltype, "produces", str(round(kgCO2perMJe, 3)), "kg of CO2 per MJ of electrical energy produced")

# To get the annual CO2, multiply this by the annual generation

a = 6351414
AnnCO2 = a * kgCO2perMJe * 3600.0

CO2tonperhour = AnnCO2 / (1000 * 365 * 24)
print(str(CO2tonperhour), "tonnes per hour of CO2 are produced by the plant")
