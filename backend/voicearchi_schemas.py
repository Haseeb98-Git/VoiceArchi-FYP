voiceArchi_json_schema = """
Here is the description of the JSON schema:
1. **single_floor_apartment:**
   description: Indicates whether the floorplan is a single-floor apartment.
   
   type: string
   
   options: ["yes", "no", "notspecified"]

2. **floor_level:**
   description: The level of the floor being described.
   
   type: string
   
   options: ["ground", "middle", "top", "notspecified"]

3. **has_outdoor_space:**
   description: Whether the floorplan has outdoor space or not. Set "notspecified" if not mentioned.
   
   type: string
   
   options: ["yes", "no", "notspecified"]

4. **has_backyard:**
   description: Indicates if the floorplan has a backyard. Set "notspecified" if not mentioned.
   
   type: string
   
   options: ["yes", "no", "notspecified"]

5. **has_frontyard:**
   description: Indicates if the floorplan has a frontyard. Set "notspecified" if not mentioned.
   
   type: string
   
   options: ["yes", "no", "notspecified"]

6. **has_right_sideyard:**
   description: Indicates if the floorplan has a right sideyard. Set "notspecified" if not mentioned.
   
   type: string
   
   options: ["yes", "no", "notspecified"]

7. **has_left_sideyard:**
   description: Indicates if the floorplan has a left sideyard. Set "notspecified" if not mentioned.
   
   type: string
   
   options: ["yes", "no", "notspecified"]

8. **indoor_floorplan_size:**
   description: Size of the indoor space.
   
   type: object
   
   properties:
      numeric_value:
         description: The numeric part of the size. If not provided, set "notspecified". If given in dimensions (e.g. "20 by 40"), use 20x40 format.
         
         type: string
         
         options: ["notspecified", "400", "200", "20x20", "40x20"]
         
      unit:
         description: Unit of measurement. If not provided, set "notspecified".
         
         type: string
         
         options: ["squarefeet", "squaremeters", "squareyards", "squareinches", "acres", "hectares", "cubicfeet", "cubicmeters", "cubicyards",
                   "centimeters", "millimeters", "marla", "kanal", "notspecified"]

9. **outdoor_floorplan_size:**
   description: The sizes of the outdoor areas.
   
   type: object
   
   properties:
      frontyard:
         description: Size of the frontyard.
         
         type: object (same as indoor_floorplan_size)
      
      backyard:
         description: Size of the backyard.
         
         type: object (same as indoor_floorplan_size)
      
      left_sideyard:
         description: Size of the left sideyard.
         
         type: object (same as indoor_floorplan_size)
      
      right_sideyard:
         description: Size of the right sideyard.
         
         type: object (same as indoor_floorplan_size)

10. **indoor_room_info:**
    description: List of indoor room names and their sizes.
    
    type: array
    
    items:
       properties:
          name:
             description: Room name with index. Pick a room name from the options list given below and add "_index" to it. Where index is an integer.
             
             type: string
             
             options: ["bedroom", "livingroom", "kitchen", "bathroom", "drawingroom", "studyroom", "diningroom", "pantry", "guestroom", "laundryroom", "storeroom",
                       "attic", "homeoffice", "gym", "library", "sunroom", "utilityroom", "workshop", "cloakroom", "foyer"]
             
             examples: ["bedroom_1", "bedroom_2", "kitchen_1", "diningroom_2"]
          
          size:
             description: Set "medium" as default if not specified.
             
             type: string
             
             options: ["small", "medium", "large"]


12. **outdoor_area_info:**
		description: List of outdoor areas, including their names, sizes, and locations. If the size or location is not specified, set it to "notspecified".
		type: array
		items:
			properties:
				  name:
						 description: The name of the outdoor area.
				     type: string  
				     
				     options: ["patio","garden","pool", "driveway", "lawn", "playrgound", "nursery", "garage", "porch"]
				     
				     examples: ["patio_1", "pool_1", "driveway_1", "garage_1", "porch_1"]  
				  
				  size:  
				     description: The size of the outdoor area. Set `"notspecified"` if not provided.  
				     
				     type: string  
				     
				     options: ["small", "medium", "large", "notspecified"]  
				  
				  location:  
				     description: The location of the outdoor area. Set `"notspecified"` if not provided.  
				     
				     type: string  
				     
				     options: ["frontyard", "backyard", "left_sideyard", "right_sideyard", "notspecified"]  
              attached:
                 description: Indicates if the outdoor area is attached to the house or not. Set `"notspecified"` if not provided.
                 
                 type: string
                 
                 options: ["yes", "no", "notspecified"]
				
13. **floorplan_relationships:**
    description: All the Relationships between rooms/areas mentioned by the user.
    
    type: object
    
    properties:
       adjacentTo:
          description: Pairs of rooms that are adjacent.
          
          type: array
          
          items: [string, string]
          
          examples: [["bedroom_1", "bathroom_1"], ["kitchen_1", "bedroom_2"]]
       
       hasBalcony:
          description: Rooms that have a balcony.
          
          type: array
          
          items: string
       
       oppositeTo:
          description: Pairs of rooms that are opposite to each other.
          
          type: array
          
          items: [string, string]
      
       hasWindows:
          description: Rooms that have windows.
          type: array
          items: string
          examples: ["bedroom_1", "kitchen_1", "livingroom_1"]

       hasAttachedBathroom:
          description: List of rooms that have attached bathrooms.
          type: array
          items: string
          examples: ["bedroom_1"]

       opensTo:
          description: Specifies that the first room has an opening (door, archway, etc.) leading directly to the second room or outdoor space.
          type: array
          items: [string, string]
          examples: [["livingroom_1", "patio_1"], ["kitchen_1", "backyard"]]


"""