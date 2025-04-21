Bake Textures is a Gimp Plugin used to batch bake textures.


It requires a main layer group where at least one group is located:

Ex:
-main_group
	-sub_group_1 ( filter )
		-layer1
		-layer2 
	-sub_group_2
		-layer1
		-layer2
	-sub_group_3
		-layer1
		-layer2

This plugin "applies" the filters of subgroups to each of its children.
Rename like so: (sub_group)_(layer)
And put the result in a group named "Baked Group".

the result applied to the example will be:

-Baked Group
	-sub_group_1_layer1 baked
	-sub_group_1_layer2 baked
	-sub_group_2_layer1 baked
	-sub_group_2_layer2 baked
	-sub_group_3_layer1 baked
	-sub_group_3_layer2 baked
-main_group
	-sub_group_1 ( filter )
		-layer1
		-layer2 
	-sub_group_2
		-layer1
		-layer2
	-sub_group_3
		-layer1
		-layer2

Notice here at the end of baked files the tag "baked".
This tag is used to ease the search of files from a batch export plugin, for example Batcher.

See : https://kamilburda.github.io/batcher/ 


