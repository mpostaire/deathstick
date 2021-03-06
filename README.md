# Pycon
Louvain-li-Nux's Game jam 2.0 submission

To launch the game, open a terminal in the game folder and execute `python order66.py`

## Controls
`Left/Right Arrows` to move, `Space` to activate adstop shield, `B` to activate bullet time

## dependencies
- python >= 3.7.1
- cocos2d
- pytmx

## Custom map creation
You can make your custom made map. 
It's very easy just let me introduce you to our **beautiful** work.

- Download and install [this map editor](https://www.mapeditor.org/).
- Launch the editor.
- All the levels are placed within the res folder. There, you nade to create a 
   folder named after your future level.
- Within this new folder, create a new tileset containing only one tile. That tile is your background.
- Create a new tilemap with the same dimensions as your background image. It is important that it is named "map.tmx" and
 saved in your level's directory.
- Click the background in the tileset bar
- Place it on the bottom left corner.
- Now you can place the game objects, in the layer menu create a new object layer
- Add object rectangles where you want to make walls that kills you.
  Follow this formatting:
  ```
  name = lose
  ```
- Add turrets where you want to make projectiles that targets you.
Follow this formatting:
    ```
    name = turret:{char}:{firing_delay}:{target_range}:{projectile_speed}:{projectile_lifetime}:{turret_level}
    ```
- Add spawn point (starting location)
Follow this formatting:
    ```
    name = spawn:{starting_angle}
    ```
- Add win point (this level ending location)
Follow this formatting:
    ```
    name = win:{next_level_dirname || end}:
    ```
- Save your map in a folder named after your level name,
place inside it your background image and both generated `*.tmx` and `*.tsx` files.
