#Dict objects
#stats : pwr : power; ms : movement speed; rvvt : revive_time (seconds); hitbox : ([x1:0,y1:0,x2,y2])
#scale : True or False, True indique un changement de taille (proportionnel) - alors déterminé en tuple, dans une autre variable.
#call : goomba['lvl1']["n1"]["scale"]

letter_number_list = ["zero","one","two","three","four","five","six","seven","eight","nine","ten"]




goomba = {'lvl3' : {"tot_number":[4],
"n_one":{"max_coords":{"xmin":15,"xmax":240},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":220,"ypos":55}},
"n_two":{"max_coords":{"xmin":5,"xmax":240},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":160,"ypos":115}},
"n_three":{"max_coords":{"xmin":5,"xmax":205},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":100,"ypos":175}},
"n_four":{"max_coords":{"xmin":270,"xmax":498},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":300,"ypos":295}},
},
'lvl1' :{"tot_number":[1],
"n_one":{"max_coords":{"xmin":550,"xmax":650},"scale":False,"can_take_dmg":False,"temp_color":[255,0,0],"base_pos":{"xpos":500,"ypos":660}},
},
'lvl4' :{"tot_number":[3],
"n_one":{"max_coords":{"xmin":142,"xmax":163},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":150,"ypos":583}},
"n_two":{"max_coords":{"xmin":142,"xmax":163},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":150,"ypos":462}},
"n_three":{"max_coords":{"xmin":142,"xmax":316},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":200,"ypos":337}},
},
'lvl2' : {"tot_number":[2],
"n_one":{"max_coords":{"xmin":654,"xmax":703},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":675,"ypos":265}},
"n_two":{"max_coords":{"xmin":814,"xmax":863},"scale":False,"can_take_dmg":True,"temp_color":[255,255,0],"base_pos":{"xpos":834,"ypos":238}},
},
'lvl5' : {"tot_number":[0]
},
'lvl7' : {"tot_number":[0]
},
'lvl6' : {"tot_number":[0]
},
'stats' :{"pwr":1,"ms":1,"rvvt":40,"hitbox":[5],"hp":1},
'kind':"goomba"
}

koopa = {'lvl3' : {"tot_number":[4],
"n_one":{"max_coords":{"xmin":510,"xmax":940},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":550,"ypos":94}},
"n_two":{"max_coords":{"xmin":510,"xmax":940},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":900,"ypos":94}},
"n_three":{"max_coords":{"xmin":5,"xmax":195},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":100,"ypos":333}},
"n_four":{"max_coords":{"xmin":100,"xmax":1100},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":1100,"ypos":665}},
},
'lvl4' :{"tot_number":[1],
"n_one":{"max_coords":{"xmin":5,"xmax":130},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":67,"ypos":661}},
},
'lvl1' :{"tot_number":[0]
},
'lvl2' :{"tot_number":[2],
"n_one":{"max_coords":{"xmin":337,"xmax":337+180},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":357,"ypos":231}},
"n_two":{"max_coords":{"xmin":540,"xmax":640},"scale":False,"can_take_dmg":True,"temp_color":[0,255,0],"base_pos":{"xpos":555,"ypos":376}},
},
'lvl5' : {"tot_number":[0]
},
'lvl7' : {"tot_number":[0]
},
'lvl6' : {"tot_number":[0]
},
'stats' :{"pwr":1,"ms":2,"rvvt":40,"hitbox":[5],"hp":1},
'kind':"koopa"
}

donkey_kong_jr = {'lvl3' : {"tot_number":[1],
"n_one":{"max_coords":{"xmin":590,"xmax":610},"scale":False,"can_take_dmg":True,"temp_color":[255,50,100],"base_pos":{"xpos":600,"ypos":60}},
},
'lvl4' :{"tot_number":[0]
},
'lvl1' :{"tot_number":[0]
},
'lvl2' :{"tot_number":[1],
'n_one':{"max_coords":{"xmin":500,"xmax":560},"scale":False,"can_take_dmg": True,"temp_color":[255,50,100],"base_pos":{"xpos":550,"ypos":361}}
},
'lvl5' : {"tot_number":[0]
},
'lvl7' : {"tot_number":[0]
},
'lvl6' : {"tot_number":[2],

'n_one':{"max_coords":{"xmin":696,"xmax":778},"scale":False,"can_take_dmg": True,"temp_color":[255,50,100],"base_pos":{"xpos":738,"ypos":627}},

'n_two':{"max_coords":{"xmin":880,"xmax":965},"scale":False,"can_take_dmg": True,"temp_color":[255,50,100],"base_pos":{"xpos":924,"ypos":618}}
},
'stats' :{"pwr":1,"ms":1,"rvvt":40,"hitbox":[5],"hp":1},
'kind':"donkey_kong_jr"
}