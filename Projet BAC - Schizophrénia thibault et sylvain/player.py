#!/usr/bin/python3.5
#-*- conding: utf-8 -*-

suits = {
"normal" : {'speed' : 2,'jump_height' : 10,'fall_dmg':125, "temp_color": [10,10,200]},
"flee" : {'speed' : 2,'jump_height' : 11,'fall_dmg':75, "temp_color": [0,255,30]},
"strong" : {'speed' : 1,'jump_height' : 8,'fall_dmg':None, "temp_color": [255,100,20]}
}

player = {
"lvl1" : {"base_pos": {"x" :75 ,"y": 654},"base_suit":"normal"},
"lvl3" : {"base_pos": {"x" :10 ,"y": 45},"base_suit":"normal"},
"lvl2" : {"base_pos": {"x" :10 ,"y": 310},"base_suit":"flee"},
"lvl4" : {"base_pos": {"x" :10 ,"y": 200},"base_suit":"flee"},
"lvl5" : {"base_pos": {"x" :120 ,"y": 590},"base_suit":"normal"},
"lvl7" : {"base_pos": {"x" :20 ,"y": 570},"base_suit":"flee"},
"lvl6" : {"base_pos": {"x" :9 ,"y": 545},"base_suit":"normal"},
'hitbox':[1,1]
} 


#winmerg