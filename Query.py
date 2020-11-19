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

