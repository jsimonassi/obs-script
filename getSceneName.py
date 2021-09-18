import obspython as obs
import random

# ------------------------------------------------------------


def cycle():
    print("Entrei no cycle")
    scenes = obs.obs_frontend_get_scenes()
    print("Tipo de scene: " + str(type(scenes)))
    current_scene = obs.obs_frontend_get_current_scene()
    current_scene_index = 0
    for i in range(len(scenes)):
        if scenes[i] == current_scene:
            current_scene_index = i
            print("Achei a atual!")

    scenes_names = obs.obs_frontend_get_scene_names()
    print("Cena atual:" + str(scenes_names[current_scene_index]))
    
    scenes.remove(current_scene)
    obs.obs_frontend_set_current_scene(random.choice(scenes))

# ------------------------------------------------------------


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    print("Entrei nas propriedades")
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "cycle_rate", "Cycle Rate(ms)",
                               1000, 1000000, 90000)
    return props


def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    print("Entrei no update")
    obs.timer_remove(cycle)
    blink_rate = obs.obs_data_get_int(settings, "cycle_rate")
    obs.timer_add(cycle, blink_rate)  # Change scene every cycle_rate ms