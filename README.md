# Portal-Frame-Structure
1. Setting Up Parameters:
The code defines a set of parameters for a portal frame structure. These include dimensions for the columns, rafters, purlins, diagonal braces, and foundation blocks. The goal is to build a series of portal frames that are used in construction, typically for large buildings like warehouses or factories.
- Columns: These are vertical supports, and their dimensions (height, width, thickness) are defined.
-	Rafters: Horizontal beams that rest on top of the columns and support the roof.
- Purlins: Beams placed across the rafters that provide additional support for the roof.
- Bracing: Diagonal supports used for stability, preventing the frame from swaying.
-	Foundation Blocks: Concrete bases that provide stability to the columns.

2. Creating and Positioning Columns:
The code creates two columns for each portal frame. These columns are then positioned at regular intervals (using x_offset) along the length of the portal frame structure. The transformation (gp_Trsf) is applied to place each column in the correct position.


3. Creating and Positioning Rafters:
Each frame has two rafters that are slanted at an angle. The code calculates the rafter length based on the rafter angle and the column spacing. The rafters are rotated and positioned at the top of the columns, with each rafter placed on one side of the frame.

4. Adding Purlins:
Purlins are horizontal beams that span across the rafters. The code creates a series of purlins and positions them at intervals along the rafters, ensuring they are spaced evenly. The purlins are transformed to the correct position above the frame.

5. Creating Diagonal Bracing:
Diagonal braces are added between the columns and rafters to add structural stability to the frame. These braces are also transformed and positioned in the correct location.

6. Foundation Blocks:
The code creates foundation blocks for each column and places them at the base of the columns to ensure the structure is anchored to the ground.

7. Combining the Components:
Each portal frame is made up of the individual components (columns, rafters, purlins, braces, and foundation blocks). The code uses the BRepAlgoAPI_Fuse function to combine these shapes into a single frame. This is done for each portal frame, and then all the frames are fused together to create the full portal frame structure.

8. Visualization:
Finally, the structure is displayed using a graphical interface (via init_display), where the frame can be viewed in 3D. The display is updated to show the complete structure, and the view is adjusted to fit the entire structure on screen.
