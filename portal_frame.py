import math
from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Ax1, gp_Dir, gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Display.SimpleGui import init_display
from draw_i_section import create_i_section
from draw_rectangular_prism import create_rectangular_prism

# Parametric dimensions
COLUMN_HEIGHT = 4000  
COLUMN_SPACING = 6000 
NUM_FRAMES = 5 
RAFTER_ANGLE = 15 
RAFTER_LENGTH = COLUMN_SPACING / (2 * math.cos(math.radians(RAFTER_ANGLE)))
PURLIN_SPACING = 1500  


COLUMN_LENGTH = 400  
COLUMN_WIDTH = 250  
COLUMN_FLANGE_THICKNESS = 12.7  
COLUMN_WEB_THICKNESS = 9.1 

RAFTER_WIDTH = 140 
RAFTER_FLANGE_THICKNESS = 12.4 
RAFTER_WEB_THICKNESS = 7.5  

BRACING_WIDTH = 40 
BRACING_HEIGHT = 20 

FOOTING_WIDTH = 500  
FOOTING_HEIGHT = 300  

portal_frames = []
for i in range(NUM_FRAMES):
    x_offset = i * COLUMN_SPACING
    
    column1 = create_i_section(COLUMN_LENGTH, COLUMN_WIDTH, COLUMN_HEIGHT, COLUMN_FLANGE_THICKNESS, COLUMN_WEB_THICKNESS)
    column2 = create_i_section(COLUMN_LENGTH, COLUMN_WIDTH, COLUMN_HEIGHT, COLUMN_FLANGE_THICKNESS, COLUMN_WEB_THICKNESS)
    
    trsf_col1 = gp_Trsf()
    trsf_col1.SetTranslation(gp_Vec(x_offset, 0, 0))
    column1_transformed = BRepBuilderAPI_Transform(column1, trsf_col1, True).Shape()
    
    trsf_col2 = gp_Trsf()
    trsf_col2.SetTranslation(gp_Vec(x_offset + COLUMN_SPACING, 0, 0))
    column2_transformed = BRepBuilderAPI_Transform(column2, trsf_col2, True).Shape()
    
    rafter1 = create_i_section(RAFTER_LENGTH, RAFTER_WIDTH, RAFTER_WIDTH, RAFTER_FLANGE_THICKNESS, RAFTER_WEB_THICKNESS)
    rafter2 = create_i_section(RAFTER_LENGTH, RAFTER_WIDTH, RAFTER_WIDTH, RAFTER_FLANGE_THICKNESS, RAFTER_WEB_THICKNESS)
    
    trsf_r1 = gp_Trsf()
    trsf_r1.SetRotation(gp_Ax1(gp_Pnt(x_offset, 0, COLUMN_HEIGHT), gp_Dir(0, 1, 0)), math.radians(RAFTER_ANGLE))
    trsf_r1.SetTranslation(gp_Vec(x_offset, 0, COLUMN_HEIGHT))
    rafter1_transformed = BRepBuilderAPI_Transform(rafter1, trsf_r1, True).Shape()
    
    trsf_r2 = gp_Trsf()
    trsf_r2.SetRotation(gp_Ax1(gp_Pnt(x_offset + COLUMN_SPACING, 0, COLUMN_HEIGHT), gp_Dir(0, 1, 0)), -math.radians(RAFTER_ANGLE))
    trsf_r2.SetTranslation(gp_Vec(x_offset + COLUMN_SPACING, 0, COLUMN_HEIGHT))
    rafter2_transformed = BRepBuilderAPI_Transform(rafter2, trsf_r2, True).Shape()
    
    num_purlins = 5
    purlins = []
    for j in range(num_purlins):
        purlin = create_rectangular_prism(RAFTER_LENGTH, BRACING_WIDTH, BRACING_HEIGHT)
        trsf_purlin = gp_Trsf()
        trsf_purlin.SetTranslation(gp_Vec(x_offset + COLUMN_SPACING / 2, j * PURLIN_SPACING, COLUMN_HEIGHT + 200))
        purlin_transformed = BRepBuilderAPI_Transform(purlin, trsf_purlin, True).Shape()
        purlins.append(purlin_transformed)
    
    bracing = create_rectangular_prism(BRACING_WIDTH, BRACING_HEIGHT, COLUMN_SPACING)
    trsf_br = gp_Trsf()
    trsf_br.SetTranslation(gp_Vec(x_offset, 0, COLUMN_HEIGHT / 2))
    bracing_transformed = BRepBuilderAPI_Transform(bracing, trsf_br, True).Shape()

    footing1 = create_rectangular_prism(FOOTING_WIDTH, FOOTING_WIDTH, FOOTING_HEIGHT)
    trsf_f1 = gp_Trsf()
    trsf_f1.SetTranslation(gp_Vec(x_offset, 0, -FOOTING_HEIGHT))
    footing1_transformed = BRepBuilderAPI_Transform(footing1, trsf_f1, True).Shape()
    
    footing2 = create_rectangular_prism(FOOTING_WIDTH, FOOTING_WIDTH, FOOTING_HEIGHT)
    trsf_f2 = gp_Trsf()
    trsf_f2.SetTranslation(gp_Vec(x_offset + COLUMN_SPACING, 0, -FOOTING_HEIGHT))
    footing2_transformed = BRepBuilderAPI_Transform(footing2, trsf_f2, True).Shape()
    
    frame = BRepAlgoAPI_Fuse(column1_transformed, column2_transformed).Shape()
    frame = BRepAlgoAPI_Fuse(frame, rafter1_transformed).Shape()
    frame = BRepAlgoAPI_Fuse(frame, rafter2_transformed).Shape()
    for purlin in purlins:
        frame = BRepAlgoAPI_Fuse(frame, purlin).Shape()
    frame = BRepAlgoAPI_Fuse(frame, bracing_transformed).Shape()
    frame = BRepAlgoAPI_Fuse(frame, footing1_transformed).Shape()
    frame = BRepAlgoAPI_Fuse(frame, footing2_transformed).Shape()
    portal_frames.append(frame)

# Fusing all frames together
portal_frame_structure = portal_frames[0]
for frame in portal_frames[1:]:
    portal_frame_structure = BRepAlgoAPI_Fuse(portal_frame_structure, frame).Shape()

# Visualization
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(portal_frame_structure, update=True)
display.FitAll()
start_display()
