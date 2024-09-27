# Copyright (C) 2021 Victor Soupday
# This file is part of CC/iC Blender Tools <https://github.com/soupday/cc_blender_tools>
#
# CC/iC Blender Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CC/iC Blender Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CC/iC Blender Tools.  If not, see <https://www.gnu.org/licenses/>.

import bpy
from mathutils import Vector
from . import meshutils, utils, vars
from rna_prop_ui import rna_idprop_ui_create

def make_driver_var(driver, var_type, var_name, target, target_type = "OBJECT", data_path = "", bone_target = "", transform_type = "", transform_space = ""):
    """
    var_type = "SINGLE_PROP", "TRANSFORMS"\n
    var_name = variable name\n
    target = target object/bone\n
    target_type = "OBJECT", "MESH"...
    target_data_path = "..."
    """
    var : bpy.types.DriverVariable = driver.variables.new()
    var.name = var_name
    if var_type == "SINGLE_PROP":
        var.type = var_type
        var.targets[0].id_type = target_type
        var.targets[0].id = target.id_data
        var.targets[0].data_path = data_path
    elif var_type == "TRANSFORMS":
        var.targets[0].id = target.id_data
        var.targets[0].bone_target = bone_target
        var.targets[0].rotation_mode = "AUTO"
        var.targets[0].transform_type = transform_type
        var.targets[0].transform_space = transform_space
    return var


def make_driver(source, prop_name, driver_type, driver_expression = "", index = -1):
    """
    prop_name = "value", "influence"\n
    driver_type = "SUM", "SCRIPTED", "AVERAGE"\n
    driver_expression = "..."
    """
    driver = None
    if source:
        fcurve : bpy.types.FCurve
        if index > -1:
            fcurve = source.driver_add(prop_name, index)
        else:
            fcurve = source.driver_add(prop_name)
        driver : bpy.types.Driver = fcurve.driver
        if driver_type == "SUM" or driver_type == "AVERAGE":
            driver.type = driver_type
        elif driver_type == "SCRIPTED":
            driver.type = driver_type
            driver.expression = driver_expression
    return driver


def add_custom_float_property(object, prop_name, prop_value : float,
                              value_min : float = 0.0, value_max : float = 1.0,
                              soft_min = None, soft_max = None,
                              overridable = True,
                              description : str = ""):

    if soft_max is None:
        soft_max = value_max
    if soft_min is None:
        soft_min = value_min

    rna_idprop_ui_create(object, prop_name, default=prop_value, overridable=overridable,
                         min=value_min, max=value_max, soft_min=soft_min, soft_max=soft_max, description=description)


def add_custom_string_property(object, prop_name, prop_value : str,
                              overridable = True,
                              description : str = ""):

    object[prop_name] = prop_value
    try:
        id_props = object.id_properties_ui(prop_name)
        id_props.update(default=prop_value, description=description)
    except:
        pass


def add_custom_float_array_property(object, prop_name, prop_value : list,
                                     value_min : float = 0.0, value_max : float = 1.0,
                                     soft_min = None, soft_max = None,
                                     overridable = True,
                                     description : str = ""):

    if soft_max is None:
        soft_max = value_max
    if soft_min is None:
        soft_min = value_min

    rna_idprop_ui_create(object, prop_name, default=prop_value, overridable=overridable,
                         min=value_min, max=value_max, soft_min=soft_min, soft_max=soft_max, description=description)


SHAPE_KEY_DRIVERS = {

    "V_Open": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,18.0],
    },

    "Ah": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,18.0],
    },

    "Oh": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,12.0],
    },

    "Jaw_Open": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [0,0,0],
        "rotate": [0,0,46.331],
    },

    "Jaw_Forward": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [1.13,0,0],
        "rotate": [0,0,0],
    },

    "Jaw_Backward": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [-0.75,0,0],
        "rotate": [0,0,0],
    },

    "Jaw_L": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [0,0,1.19],
        "rotate": [0,0,0],
    },

    "Jaw_R": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [0,0,-1.19],
        "rotate": [0,0,0],
    },

    "Jaw_Up": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [0,-0.35,0],
        "rotate": [0,0,0],
    },

    "Jaw_Down": {
        "bone": ["CC_Base_JawRoot","jaw_master"],
        "range": 150.0,
        "translate": [0,0.86,0],
        "rotate": [0,0,0],
    },



    "Head_Turn_Up": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [0,0,0],
        "rotate": [-45,0,0],
    },

    "Head_Turn_Down": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [0,0,0],
        "rotate": [27,0,0],
    },

    "Head_Turn_L": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [3.02,0,0],
        "rotate": [-2.26,76.49,-2.46],
    },

    "Head_Turn_R": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [-3.02,0,0],
        "rotate": [-2.26,-76.49,2.46],
    },

    "Head_Tilt_L": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [1.15,0,0],
        "rotate": [0,0,-35.1],
    },

    "Head_Tilt_R": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [-1.15,0,0],
        "rotate": [0,0,35.1],
    },

    "Head_L": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [3.59,0,0],
        "rotate": [0,0,0],
    },

    "Head_R": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [-3.59,0,0],
        "rotate": [0,0,0],
    },

    "Head_Forward": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [0,0.05,5.31],
        "rotate": [0,0,0],
    },

    "Head_Backward": {
        "bone": ["CC_Base_Head","head","spine.006"],
        "range": 150.0,
        "translate": [0,-0.04,-4.67],
        "rotate": [0,0,0],
    },


    "Eye_L_Look_L": {
        "bone": ["CC_Base_L_Eye","eye.L"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,40],
    },

    "Eye_R_Look_L": {
        "bone": ["CC_Base_R_Eye","eye.R"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,30],
    },

    "Eye_L_Look_R": {
        "bone": ["CC_Base_L_Eye","eye.L"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,-30],
    },

    "Eye_R_Look_R": {
        "bone": ["CC_Base_R_Eye","eye.R"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [0,0,-40],
    },

    "Eye_L_Look_Up": {
        "bone": ["CC_Base_L_Eye","eye.L"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [-20,0,0],
    },

    "Eye_R_Look_Up": {
        "bone": ["CC_Base_R_Eye","eye.R"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [-20,0,0],
    },

    "Eye_L_Look_Down": {
        "bone": ["CC_Base_L_Eye","eye.L"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [22,0,0],
    },

    "Eye_R_Look_Down": {
        "bone": ["CC_Base_R_Eye","eye.R"],
        "range": 100.0,
        "translate": [0,0,0],
        "rotate": [22,0,0],
    },
}


def clear_facial_shape_key_bone_drivers(chr_cache):
    """Add drivers for the jaw, eye and head bones (optional) based on the facial
       expression shape keys.
    """

    body = chr_cache.get_body()
    arm = chr_cache.get_armature()

    if not body or not arm:
        return

    bone_names_done = []

    utils.object_mode_to(arm)

    # remove existing drivers
    for key_name in SHAPE_KEY_DRIVERS.keys():
        bone_names = SHAPE_KEY_DRIVERS[key_name]["bone"]
        for bone_name in bone_names:
            if bone_name in arm.pose.bones:
                if bone_name not in bone_names_done:
                    bone_names_done.append(bone_name)
                    pose_bone = arm.pose.bones[bone_name]
                    utils.log_info(f"Removing drivers for: {bone_name}")
                    pose_bone.driver_remove("location", 0)
                    pose_bone.driver_remove("location", 1)
                    pose_bone.driver_remove("location", 2)
                    pose_bone.driver_remove("rotation_euler", 0)
                    pose_bone.driver_remove("rotation_euler", 1)
                    pose_bone.driver_remove("rotation_euler", 2)
                    pose_bone.rotation_mode = "QUATERNION"


def add_facial_shape_key_bone_drivers(chr_cache, jaw, eye_look, head):
    """Add drivers for the jaw, eye and head bones (optional) based on the facial
       expression shape keys.
    """

    body = chr_cache.get_body()
    arm = chr_cache.get_armature()

    if not body or not arm:
        return

    bone_drivers = {}
    bone_names_done = []

    utils.object_mode_to(arm)

    # remove existing drivers
    for key_name in SHAPE_KEY_DRIVERS.keys():
        bone_names = SHAPE_KEY_DRIVERS[key_name]["bone"]
        for bone_name in bone_names:
            if bone_name in arm.pose.bones:
                if bone_name not in bone_names_done:
                    bone_names_done.append(bone_name)
                    pose_bone = arm.pose.bones[bone_name]
                    utils.log_info(f"Removing drivers for: {bone_name}")
                    pose_bone.driver_remove("location", 0)
                    pose_bone.driver_remove("location", 1)
                    pose_bone.driver_remove("location", 2)
                    pose_bone.driver_remove("rotation_euler", 0)
                    pose_bone.driver_remove("rotation_euler", 1)
                    pose_bone.driver_remove("rotation_euler", 2)
                    pose_bone.rotation_mode = "QUATERNION"

    # refactor shape key driver list by bone_name, property and array property index
    for key_name in SHAPE_KEY_DRIVERS.keys():
        bone_names = SHAPE_KEY_DRIVERS[key_name]["bone"]
        range = SHAPE_KEY_DRIVERS[key_name]["range"]
        translate = SHAPE_KEY_DRIVERS[key_name]["translate"]
        rotate = SHAPE_KEY_DRIVERS[key_name]["rotate"]

        if not meshutils.find_shape_key(body, key_name):
            utils.log_info(f"Shape-key: {key_name} not found, skipping.")
            continue

        if ((key_name.startswith("Jaw_") and not jaw) or
            (key_name.startswith("V_") and not jaw) or
            (key_name == "Ah" and not jaw) or
            (key_name == "Oh" and not jaw) or
            (key_name.startswith("Eye_") and not eye_look) or
            (key_name.startswith("Head_") and not head)):
            continue

        # find the bone specified by the shape_key driver def
        pose_bone_name = None
        for bone_name in bone_names:
            if bone_name in arm.pose.bones:
                pose_bone_name = bone_name

        if pose_bone_name:

            for i,v in enumerate(translate):
                if v != 0:
                    driver_id = pose_bone_name, "location", i
                    if driver_id not in bone_drivers.keys():
                        bone_drivers[driver_id] = { "bone_name": pose_bone_name,
                                                    "prop": "location",
                                                    "index": i,
                                                    "shape_keys": [] }
                    bone_drivers[driver_id]["shape_keys"].append({ "shape_key": key_name,
                                                                   "value": v,
                                                                   "range": range })

            for i,v in enumerate(rotate):
                if v != 0:
                    driver_id = pose_bone_name, "rotation_euler", i
                    if driver_id not in bone_drivers.keys():
                        bone_drivers[driver_id] = { "bone_name": pose_bone_name,
                                                    "prop": "rotation_euler",
                                                    "index": i,
                                                    "shape_keys": [] }
                    shape_key_def = { "shape_key": key_name,
                                      "value": v,
                                      "range": range }
                    bone_drivers[driver_id]["shape_keys"].append(shape_key_def)

    # create drivers for each (bone, property, index) driven by shape keys
    for driver_id in bone_drivers.keys():
        bone_driver_def = bone_drivers[driver_id]
        pose_bone_name = bone_driver_def["bone_name"]
        pose_bone : bpy.types.PoseBone
        pose_bone = arm.pose.bones[pose_bone_name]
        pose_bone.rotation_mode = "XYZ"
        prop = bone_driver_def["prop"]
        index = bone_driver_def["index"]
        shape_key_defs = bone_driver_def["shape_keys"]

        # build driver expression
        expr = "("
        for i, key_def in enumerate(shape_key_defs):
            var_name = f"var{i}"
            shape_key_name = key_def["shape_key"]
            fac_value = 100.0 * key_def["value"] / key_def["range"]
            if prop == "rotation_euler":
                fac_value *= 0.01745329
            fac = "{:.6f}".format(fac_value)
            if i > 0:
                expr += "+"
            expr += f"{var_name}*{fac}"
        expr += ")"
        #if len(shape_key_defs) > 1:
        #    expr += f"/{len(shape_key_defs)}"

        # make driver
        utils.log_info(f"Adding driver to {driver_id}: expr = {expr}")
        driver = make_driver(pose_bone, prop, "SCRIPTED", driver_expression=expr, index=index)

        # make driver vars
        if driver:
            for i, key_def in enumerate(shape_key_defs):
                var_name = f"var{i}"
                shape_key_name = key_def["shape_key"]
                data_path = f"shape_keys.key_blocks[\"{shape_key_name}\"].value"
                var = make_driver_var(driver,
                                        "SINGLE_PROP",
                                        var_name,
                                        body.data,
                                        target_type="MESH",
                                        data_path=data_path)


def clear_body_shape_key_drivers(chr_cache):
    body = chr_cache.get_body()
    arm = chr_cache.get_armature()

    if not body or not arm:
        return

    if utils.object_has_shape_keys(body):
        body_keys = [ key_block.name for key_block in body.data.shape_keys.key_blocks ]
        objects = utils.get_child_objects(arm)
        for obj in objects:
            if obj != body and utils.object_has_shape_keys(obj):
                obj_key : bpy.types.ShapeKey
                for obj_key in obj.data.shape_keys.key_blocks:
                    if obj_key.name in body_keys:
                        obj_key.driver_remove("value")


def add_body_shape_key_drivers(chr_cache, add_drivers, only_objects=None):
    """Drive all expression shape keys on non-body objects from the body shape keys.
    """

    body = chr_cache.get_body()
    arm = chr_cache.get_armature()

    if not body or not arm:
        return

    # collect all possible body objects together
    head_bones = [ "CC_Base_Head", "head", "spine.006" ]
    body_objects = {}
    body_objects[body] = meshutils.total_vertex_group_weight(body, head_bones)
    body_id = utils.get_rl_object_id(body)
    for child in arm.children:
        if child not in body_objects:
            if utils.get_rl_object_id(child) == body_id:
                body_objects[child] = meshutils.total_vertex_group_weight(child, head_bones)

    # try to find which one contains the head (contains the most weight to head bone)
    if body_objects:
        w = body_objects[body]
        for o in body_objects:
            if body_objects[o] > w:
                w = body_objects[o]
                body = o

    utils.log_info(f"Using head mesh: {body.name} for driver source")

    if utils.object_has_shape_keys(body):
        body_keys = [ key_block.name for key_block in body.data.shape_keys.key_blocks ]
        objects = utils.get_child_objects(arm)
        for obj in objects:
            if only_objects and obj not in only_objects:
                continue
            if obj != body and utils.object_has_shape_keys(obj):
                obj_key : bpy.types.ShapeKey
                for obj_key in obj.data.shape_keys.key_blocks:
                    if obj_key.name in body_keys:
                        obj_key.driver_remove("value")
                        if add_drivers:
                            # make driver
                            utils.log_info(f"Adding driver to {obj.name} for expression key: {obj_key.name}")
                            driver = make_driver(obj_key, "value", "SUM")
                            # make driver var
                            if driver:
                                data_path = f"shape_keys.key_blocks[\"{obj_key.name}\"].value"
                                make_driver_var(driver,
                                                "SINGLE_PROP",
                                                "key_value",
                                                body.data,
                                                target_type="MESH",
                                                data_path=data_path)

