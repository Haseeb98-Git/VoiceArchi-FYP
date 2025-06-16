user_constraints = {
  "single_floor_apartment": "yes",
  "floor_level": "notspecified",
  "has_outdoor_space": "yes",
  "has_backyard": "yes",
  "has_frontyard": "yes",
  "has_right_sideyard": "yes",
  "has_left_sideyard": "yes",
  "indoor_floorplan_size": {
    "numeric_value": "notspecified",
    "unit": "notspecified"
  },
  "outdoor_floorplan_size": {
    "frontyard": {
      "numeric_value": "notspecified",
      "unit": "notspecified"
    },
    "backyard": {
      "numeric_value": "notspecified",
      "unit": "notspecified"
    },
    "left_sideyard": {
      "numeric_value": "notspecified",
      "unit": "notspecified"
    },
    "right_sideyard": {
      "numeric_value": "notspecified",
      "unit": "notspecified"
    }
  },
  "indoor_room_info": [
    {
      "name": "bedroom_1",
      "size": "large"
    },
    {
      "name": "bedroom_2",
      "size": "medium"
    },
    {
      "name": "bedroom_3",
      "size": "medium"
    },
    {
      "name": "bedroom_4",
      "size": "medium"
    },
    {
      "name": "bathroom_1",
      "size": "medium"
    },
    {
      "name": "bathroom_2",
      "size": "medium"
    },
    {
      "name": "bathroom_3",
      "size": "medium"
    },
    {
      "name": "kitchen_1",
      "size": "medium"
    },
    {
      "name": "kitchen_2",
      "size": "medium"
    },
    {
      "name": "garage_1",
      "size": "medium"
    }
  ],
  "outdoor_area_info": [
    {
      "name": "pool_1",
      "size": "notspecified",
      "location": "backyard",
      "attached": "notspecified"
    },
    {
      "name": "playground_1",
      "size": "small",
      "location": "frontyard",
      "attached": "notspecified"
    },
    {
      "name": "driveway_1",
      "size": "notspecified",
      "location": "frontyard",
      "attached": "notspecified"
    }
  ],
  "floorplan_relationships": {
    "adjacentTo": [
      ["bedroom_1", "kitchen1"],
      ["bedroom_1", "bathroom_1"],
      ["bedroom_2", "livingroom_1"],
      ["bedroom_3", "livingroom_1"],
      ["bedroom_4", "livingroom_1"],
      ["bedroom_2", "bathroom_2"],
      ["bedroom_3", "bathroom_3"],
      ["garage_1", "livingroom_1"]
    ],
    "hasBalcony": ["bedroom_1", "kitchen_1", "bedroom_3"],
    "oppositeTo": [],
    "hasWindows": [],
    "hasAttachedBathroom": ["bedroom_1"],
    "opensTo": []
  }
}

area_types = {
    'bedroom': 'private',
    'livingroom': 'social',
    'kitchen': 'service',
    'bathroom': 'private',
    'drawingroom': 'social',
    'studyroom': 'private',
    'diningroom': 'social',
    'pantry': 'service',
    'guestroom': 'private',
    'laundryroom': 'service',
    'storeroom': 'service',
    'attic': 'service',
    'homeoffice': 'private',
    'gym': 'private',
    'library': 'private',
    'sunroom': 'social',
    'utilityroom': 'service',
    'workshop': 'service',
    'garage': 'social',
    'cloakroom': 'service',
    'foyer': 'social'
}

room_sizes = {
    'bedroom': {'small': 6, 'medium': 9, 'large': 12},
    'masterbedroom': {'small': 12, 'medium': 12, 'large': 12},
    'livingroom': {'small': 8, 'medium': 12, 'large': 15},
    'kitchen': {'small': 5, 'medium': 8, 'large': 11},
    'bathroom': {'small': 3, 'medium': 5, 'large': 7},
    'drawingroom': {'small': 7, 'medium': 10, 'large': 13},
    'studyroom': {'small': 4, 'medium': 6, 'large': 8},
    'diningroom': {'small': 6, 'medium': 9, 'large': 12},
    'pantry': {'small': 2, 'medium': 4, 'large': 6},
    'guestroom': {'small': 6, 'medium': 9, 'large': 12},
    'garage': {'small':4, 'medium': 6, 'large': 9},
    'laundryroom': {'small': 3, 'medium': 5, 'large': 7},
    'storeroom': {'small': 2, 'medium': 4, 'large': 6},
    'attic': {'small': 3, 'medium': 5, 'large': 7},
    'homeoffice': {'small': 4, 'medium': 6, 'large': 8},
    'gym': {'small': 6, 'medium': 9, 'large': 12},
    'library': {'small': 5, 'medium': 7, 'large': 10},
    'sunroom': {'small': 5, 'medium': 8, 'large': 11},
    'utilityroom': {'small': 3, 'medium': 5, 'large': 7},
    'workshop': {'small': 5, 'medium': 8, 'large': 11},
    'cloakroom': {'small': 2, 'medium': 3, 'large': 4},
    'foyer': {'small': 4, 'medium': 6, 'large': 8}
}