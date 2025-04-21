#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   gimp-bake-textures.py
#   plug-in to batch bake textures from groups with filters on them
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful.


DEBUG_MESSAGE = False
DEBUG_UNDO = False

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
gi.require_version('Gegl', '0.4')
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gtk
import sys

class Bake_textures (Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "jb-bake-textures" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("Bakeing Textures")
        procedure.add_menu_path('<Image>/File/Baking/')

        procedure.set_documentation("Bakeing Textures Plugin",
                                    "Batch bake textures from groups within a group with filters on them",
                                    name)
        procedure.set_attribution("pingoo04", "pingoo04", "2025")

        return procedure



    def run(self, procedure, run_mode, image, drawables, config, run_data):

        group = is_group_of_group(drawables)
        if group == None: return procedure.new_return_values(Gimp.PDBStatusType.CANCEL  , GLib.Error())

        if not DEBUG_UNDO : image.undo_group_start() # start the undo group

        baked_group = Gimp.GroupLayer.new(image, "Baked Group") # Creation du layer group "Baked Group"
        image.insert_layer(baked_group, drawables[0].get_parent(), 0) # Attachement du groupe à la racine

        for i in group: # for all groups in group 
            temp_group = i.copy() # copy the group
            apply_filers(temp_group, baked_group, image) # and apply its filters to its layers 

        if not DEBUG_UNDO : image.undo_group_end() # end the undo group
        #GLib.free(group)
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

def apply_filers(parent_group, baked_group, image): # apply the (parent_group) filters to his layers and put them into (baked_group)

    parent_list = parent_group.get_children() # get the list of (parent_group)

    for i in parent_list: # for all layers(i) in (parent_list)
        
        
        copy_parent_group = parent_group.copy() # copy of (parent_group)
        copy_parent_list = copy_parent_group.get_children() # get list of (copy_parent_group)
        for j in copy_parent_list:       # do for all layer in (copy_parent_group)
            if is_same_layer(j, i):        # check if i an j are the copy of one an other
                j.set_visible(True)        # if yes set j visible
            else:
                j.set_visible(False)

        image.insert_layer(copy_parent_group, baked_group, 0) # insert the layer into the (baked_group)
        rename(copy_parent_group) # rename the group 
        layer = copy_parent_group.merge() # merge the layer with the group (apply the filter)
        #GLib.free(copy_parent_list) # free the list
        
    
    #Gimp.message(str(len(parent_list)))
    #GLib.free(parent_list) # free the list
    
def is_same_layer(layer1, layer2):
    #_bool = layer1.get_tattoo() == layer2.get_tattoo()
    _bool = layer1.get_name() == layer2.get_name() # marche ? / use tattoo sinon
    return _bool

def rename(group): # rename the group like so: (group_name)_(layer_name)
    list_group = group.get_children()
    #Gimp.message(str(len(list_group)))
    for layer in list_group:
        if layer.get_visible() == True:
            group_name = slice_from_suffix(group.get_name(), " copy")
            group_name = slice_from_suffix(group_name, " #")
            layer_name = slice_from_suffix(layer.get_name(), ".png")
            new_name = group_name+"_"+layer_name+" baked"
            group.set_name(new_name)

def slice_from_suffix(name, suffix):
    name = name.strip()         # remove spaces from start and end
    name_i = name.find(suffix) # get the begining (index) of the suffix
    return name[0:name_i]       # slice the suffix

def is_group_of_group(drawables):

    
    if drawables[0].is_group_layer() == True:
        if DEBUG_MESSAGE:
            Gimp.message("[GOOD] first layer is a group") 
    else:
        Gimp.message("[BAD] Please select a layer group")
        return None

    is_group_of_group = False

    l = drawables[0].get_children()
    for i in l:
        temp_bool = i.is_group_layer()
        is_group_of_group = is_group_of_group or temp_bool
        if temp_bool == False:
            l.remove(i)


    if is_group_of_group:
        if DEBUG_MESSAGE:
            Gimp.message("[GOOD] the group as at least one group")
    else:
        Gimp.message("[BAD] Please select a layer group of at least one layer group")
        return None

    return l


    


Gimp.main(Bake_textures.__gtype__, sys.argv)
