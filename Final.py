import rdflib


# Make a graph and parse OWL file data onto it
q = rdflib.Graph()
q.parse("./Ferrybridge_Coal_Power_Station_UK.owl")


# Query 1 - annual generation of the power plant

qenergy = q.query(
    """PREFIX powerplant: <http://www.theworldavatar.com/ontology/ontoeip/powerplants/PowerPlant.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX coordinate: <http://www.theworldavatar.com/ontology/ontocape/upper_level/coordinate_system.owl#>
    PREFIX system: <http://www.theworldavatar.com/ontology/ontocape/upper_level/system.owl#>
    PREFIX space_and_time_extended: <http://www.theworldavatar.com/ontology/ontocape/supporting_concepts/space_and_time/space_and_time_extended.owl#>
    PREFIX technical_system: <http://www.theworldavatar.com/ontology/ontocape/upper_level/technical_system.owl#>
    SELECT DISTINCT ?value_of_AnnualGeneration ?unit_of_AnnualGeneration
    WHERE
    {
    ?powerPlantIRI rdf:type powerplant:PowerPlant .
    ?powerPlantIRI technical_system:realizes ?Generation_Type .
    ?Generation_Type powerplant:hasAnnualGeneration ?AnnualGeneration .
    ?AnnualGeneration system:hasValue ?AnnualGeneration_value .
    ?AnnualGeneration_value system:numericalValue ?value_of_AnnualGeneration .
    ?AnnualGeneration_value system:hasUnitOfMeasure ?unit_of_AnnualGeneration .
    }"""
    )

# Creating variables to use the queried values later
for row in qenergy:
    a = row.value_of_AnnualGeneration
    au = row.unit_of_AnnualGeneration


# Query 2 - rate of production of CO2 (to compare later)

qCO2 = q.query(
    """PREFIX powerplant: <http://www.theworldavatar.com/ontology/ontoeip/powerplants/PowerPlant.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX coordinate: <http://www.theworldavatar.com/ontology/ontocape/upper_level/coordinate_system.owl#>
    PREFIX system: <http://www.theworldavatar.com/ontology/ontocape/upper_level/system.owl#>
    PREFIX space_and_time_extended: <http://www.theworldavatar.com/ontology/ontocape/supporting_concepts/space_and_time/space_and_time_extended.owl#>
    PREFIX technical_system: <http://www.theworldavatar.com/ontology/ontocape/upper_level/technical_system.owl#>
    PREFIX system_performance: <http://www.theworldavatar.com/ontology/ontoeip/system_aspects/system_performance.owl#>
    SELECT DISTINCT ?value_of_CO2Emission ?unit_of_CO2Emission
    WHERE
    {
    ?powerPlantIRI rdf:type powerplant:PowerPlant .
    ?powerPlantIRI technical_system:realizes ?Generation_Type .
    ?Generation_Type system_performance:hasEmission ?CO2Emission .
    ?CO2Emission system:hasValue ?CO2Emission_value .
    ?CO2Emission_value system:numericalValue ?value_of_CO2Emission .
    ?CO2Emission_value system:hasUnitOfMeasure ?unit_of_CO2Emission .
    }"""
    )

# Creating variables to use the queried values later
for row in qCO2:
    b = row.value_of_CO2Emission
    bu = row.unit_of_CO2Emission


# Query 3 - type of fuel used

qfuel = q.query(
    """
    PREFIX powerplant:  			<http://www.theworldavatar.com/ontology/ontoeip/powerplants/PowerPlant.owl#>
    PREFIX rdf:        				<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX coordinate:  <http://www.theworldavatar.com/ontology/ontocape/upper_level/coordinate_system.owl#>
    PREFIX system:      <http://www.theworldavatar.com/ontology/ontocape/upper_level/system.owl#>
    PREFIX space_and_time_extended:<http://www.theworldavatar.com/ontology/ontocape/supporting_concepts/space_and_time/space_and_time_extended.owl#>
    PREFIX technical_system: <http://www.theworldavatar.com/ontology/ontocape/upper_level/technical_system.owl#>
    SELECT ?Primary_Fuel_type
    WHERE
    {
    ?powerPlantIRI rdf:type powerplant:PowerPlant .
    ?powerPlantIRI technical_system:realizes ?Generation_Type .
    ?Generation_Type powerplant:consumesPrimaryFuel ?Primary_Fuel_type .
    }"""
    )

# Creating variables to use the queried values later
for row in qfuel:
    c = str(row.Primary_Fuel_type)

# Creating a string with the fuel type
fueltype = c[c.index("#")+1:]


# Output statements
print("The annual energy production is", str(a), str(au[au.index("#")+1:]))
print("The amount of CO2 produced is", str(b), str(bu[bu.index("#")+1:]))
print("The fuel type is", fueltype)


# Fuel data
# Uncertainties in the following values: CoalBiomass was a guess, the rest use HHV rather than LHV
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

print("The fuel type is", fueltype + ".", "It has a rough efficiency of", str(E) + ",", "a HHV of", str(HHV), "MJ/kg and a carbon content of", str(q) + ".")

# CO2 produced by a fuel to give a MJ of electricity
kgCO2perMJe = (44/12) * q / (E * HHV)

print(fueltype, "produces", str(round(kgCO2perMJe, 3)), "kg of CO2 per MJ of electrical energy produced")
print("")


# To get the annual CO2, multiply this by the annual generation
AnnCO2 = float(a) * float(kgCO2perMJe) * 3600.0

# Hourly CO2 production of the plant, assuming it runs all year round
CO2tonperhour = AnnCO2 / (1000 * 365 * 24)
print(str(round(CO2tonperhour, 3)), "tonnes per hour of CO2 are produced by the plant")

# CO2 produced per hour compared to the OWL file value
print("This is", str(round(CO2tonperhour/float(b), 3)), "times the quoted value in the OWL file")

#scoring indicator 
indicator= (44/12) * q / (E * HHV * 0.0399)
print("indicator: CO2 emission per unit of value added is", str(round(indicator,3)), "kg/pounds")
