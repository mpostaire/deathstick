# Pycon
Game jam 2.0 submission

To launch the game, open a terminal in the game folder and execute `python order66.py`

## dependencies
- python >= 3.6.5
- cocos2d

## Modding API
You can make your custom made map. 
It's very easy just let me introduce you to our **beautiful** work.

- Download and install [this map editor](https://www.mapeditor.org/).
- Launch it and apply a background image which will be your game world.
- Add hitboxes where you want to make walls that kills you.
  Follow this formatting:
  ```
  name = loose
  ```
- Add turrets where you want to make projectiles that targets you.
Follow this formatting:
    ```
    name = turret:{char}:{firing_delay}:{target_range}:{projectile_speed}:{projectile_lifetime}
    ```
- Add spawn point (starting location)
Follow this formatting:
    ```
    name = spawn
    ```
- Add win point (this level ending location)
Follow this formatting:
    ```
    name = win:{next_level_dirname || end}:
    ```
- Save your map in a folder named after your level name,
place inside it your background image and both generated `*.tmx` and `*.tsx` files.
