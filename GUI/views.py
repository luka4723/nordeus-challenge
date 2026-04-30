import arcade
from pathlib import Path
import arcade.gui
import GUI.elements as ui

assets_path = Path(__file__).parent.parent.resolve() / Path("resources")
arcade.resources.add_resource_handle("res",assets_path)



