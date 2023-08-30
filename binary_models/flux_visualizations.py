import cobra
import pandas as pd
import binary_models.helpers as helpers
from binary_models.load_ternary import load_community_model, model_folder
from cobra import Metabolite, Reaction

def create_explicit_carbon(community_model):

    source_carbon = Metabolite('co2_source_m',
                               name='Source CO2',
                               compartment='m'
                               )

    co2_source2Azoto = Reaction('EX_co2_source_e__Azotobacter',
                                name='co2 source2Azoto'
                                )
    co2_source2Rhodo = Reaction('EX_co2_source_e__Rhodosporidium',
                                name='co2 source2Rhodo'
                                )
    co2_source2Synec = Reaction('EX_co2_source_e__Synechococcus',
                                name='co2 source2Synec'
                                )

    community_model.add_metabolites([source_carbon])
    community_model.add_boundary(
        community_model.metabolites.get_by_id("co2_source_m"), type="exchange"
    )
    co2_source_m = community_model.metabolites.co2_source_m
    co2_m = community_model.metabolites.co2_m
    co2_e__Azotobacter = community_model.metabolites.co2_e__Azotobacter
    co2_e__Rhodosporidium = community_model.metabolites.co2_e__Rhodosporidium
    co2_e__Synechococcus = community_model.metabolites.co2_e__Synechococcus

    co2_source2Azoto.add_metabolites({
        co2_source_m: -1.0,
        co2_e__Azotobacter: 1.0
    })

    co2_source2Rhodo.add_metabolites({
        co2_source_m: -1.0,
        co2_e__Rhodosporidium: 1.0
    })

    co2_source2Synec.add_metabolites({
        co2_source_m: -1.0,
        co2_e__Synechococcus: 1.0
    })

    community_model.add_reactions([co2_source2Azoto,co2_source2Rhodo,co2_source2Synec])

    # Set Micom Global IDs and Community IDs
    community_model.metabolites.co2_source_m.global_id = 'co2_source_m'
    community_model.metabolites.co2_source_m.community_id = 'medium'
    community_model.reactions.EX_co2_source_e__Azotobacter.global_id = 'EX_co2_source_e'
    community_model.reactions.EX_co2_source_e__Azotobacter.community_id = 'Azotobacter'
    community_model.reactions.EX_co2_source_e__Rhodosporidium.global_id = 'EX_co2_source_e'
    community_model.reactions.EX_co2_source_e__Rhodosporidium.community_id = 'Rhodosporidium'
    community_model.reactions.EX_co2_source_e__Synechococcus.global_id = 'EX_co2_source_e'
    community_model.reactions.EX_co2_source_e__Synechococcus.community_id = 'Synechococcus'
    community_model.reactions.EX_co2_source_m.global_id = 'EX_co2_source_m'
    community_model.reactions.EX_co2_source_m.community_id = 'medium'

    # Force EX_co2_source_m to push only and EX_co2_m to pull only
    community_model.reactions.EX_co2_source_m.lower_bound = -1.9
    community_model.reactions.EX_co2_source_m.upper_bound = 0
    community_model.reactions.EX_co2_m.lower_bound = 0
    # 
    
    return community_model


def remove_hco3_to_co2(community_model):
    """Removes the the hco3 to co2 reaction in Rhodosporidium"""

    HCO3E = community_model.reactions.HCO3E__Rhodosporidium
    community_model.remove_reactions([HCO3E])
    
    return community_model


if __name__ == '__main__':
    community, manifest = load_community_model(prep_files=False)

    source_carbon_community = create_explicit_carbon(community)

    

    
