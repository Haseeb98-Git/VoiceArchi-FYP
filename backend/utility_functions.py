import copy
def get_ambiguities(extracted_json):
    # Ambiguity resolution
    user_constraints = copy.deepcopy(extracted_json)

    general_ambiguities = {}
    size_ambiguities = {}
    general_ambiguity_count = 0
    size_ambiguity_count = 0

    # resolving general ambiguities
    if user_constraints['single_floor_apartment'] == 'notspecified':
        general_ambiguity_count += 1
        general_ambiguities[f"ambiguity_{general_ambiguity_count}"] = "Is your floorplan a single floor apartment?"
    if user_constraints['floor_level'] == 'notspecified':
        general_ambiguity_count += 1
        general_ambiguities[f"ambiguity_{general_ambiguity_count}"] = "What is the floorplan level? Ground, Middle or Top?"

    # resolving size ambiguities
    if user_constraints['indoor_floorplan_size']['numeric_value'] == 'notspecified':
        size_ambiguity_count += 1
        size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "What is your indoor floorplan size and its unit?"

    if user_constraints['indoor_floorplan_size']['unit'] == "notspecified" and user_constraints['indoor_floorplan_size']['numeric_value'] != "notspecified":
        size_ambiguity_count +=1
        size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "You mentioned your indoor floorplan size, please also specify the unit."

    if user_constraints['has_frontyard'] == 'yes':
        if user_constraints['outdoor_floorplan_size']['frontyard']['numeric_value'] == 'notspecified':
            size_ambiguity_count += 1
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "What is your frontyard size and unit?"
        if user_constraints['outdoor_floorplan_size']['frontyard']['unit'] == 'notspecified' and user_constraints['outdoor_floorplan_size']['frontyard']['numeric_value'] != 'notspecified':
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "You mentioned your frontyard size, please also specify the unit."

    if user_constraints['has_backyard'] == 'yes':
        if user_constraints['outdoor_floorplan_size']['backyard']['numeric_value'] == 'notspecified':
            size_ambiguity_count += 1
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "What is your backyard size and unit?"
        if user_constraints['outdoor_floorplan_size']['backyard']['unit'] == 'notspecified' and user_constraints['outdoor_floorplan_size']['backyard']['numeric_value'] != 'notspecified':
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "You mentioned your backyard size, please also specify the unit."

    if user_constraints['has_left_sideyard'] == 'yes':
        if user_constraints['outdoor_floorplan_size']['left_sideyard']['numeric_value'] == 'notspecified':
            size_ambiguity_count += 1
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "What is your left sideyard size and unit?"
        if user_constraints['outdoor_floorplan_size']['left_sideyard']['unit'] == 'notspecified' and user_constraints['outdoor_floorplan_size']['left_sideyard']['numeric_value'] != 'notspecified':
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "You mentioned your left sideyard size, please also specify the unit."

    if user_constraints['has_right_sideyard'] == 'yes':
        if user_constraints['outdoor_floorplan_size']['right_sideyard']['numeric_value'] == 'notspecified':
            size_ambiguity_count += 1
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "What is your right sideyard size and unit?"
        if user_constraints['outdoor_floorplan_size']['right_sideyard']['unit'] == 'notspecified' and user_constraints['outdoor_floorplan_size']['right_sideyard']['numeric_value'] != 'notspecified':
            size_ambiguities[f"ambiguity_{size_ambiguity_count}"] = "You mentioned your right sideyard size, please also specify the unit."
    
    return general_ambiguities, size_ambiguities