# Attributes:
# walk: player can walk onto this tile.
# transp: this tile doesn't block light.
# door: this tile functions as a door, which means +walk +transp when open and -walk -transp when closed.
TILES = """
>tile FOOTPATH_1 +walk +transp textchar= 
>tile FOOTPATH_2 +walk +transp textchar=_
>tile TILE_1 +walk +transp textchar=.
>tile TILE_2 +walk +transp textchar=,
>tile TILE_3 +walk +transp textchar=,
>tile GRASS_1 +walk +transp textchar=;
>tile SHRUB_1 textchar=%
>tile SHRUB_2 textchar=%
>tile TREE_1 textchar=T
>tile TREE_2 textchar=t
>tile BRICK_1 textchar=#
>tile BRICK_2 textchar=#
>tile BRICK_3 textchar=#
>tile DOOR_1 +door textchar=[
>tile WINDOW_1 +transp textchar=O
"""

