#in init
	5_style_dict={"soft":0, "mediumsoft":0, "medium":0, "mediumhard":0, "hard":0}
	5_style_list=["soft","mediumsoft","medium","mediumhard","hard"]
	3_style_dict={}
	3_style_list=[]
#in getaction
	while round_num<200:
		style_integer=random.randint(0,4)
		style=5_style_list[style_integer]
		if style=="soft":

		elif style=="mediumsoft":

		elif style=="medium":
			
		elif style=="mediumhard":
			
		elif style=="hard":

	
		for key in 5_style_dict:
				if key==style:
					5_style_dict[key]+=my_delta
		
	3_style_list.append(max(5_style_dict, key=lambda key: 5_style_dict[key]))
	5_style_dict.pop(max(5_style_dict, key=lambda key: 5_style_dict[key]))
	3_style_list.append(max(5_style_dict, key=lambda key: 5_style_dict[key]))
	5_style_dict.pop(max(5_style_dict, key=lambda key: 5_style_dict[key]))
	3_style_list.append(max(5_style_dict, key=lambda key: 5_style_dict[key]))
	5_style_dict.pop(max(5_style_dict, key=lambda key: 5_style_dict[key]))
	for key in 3_style_list:
		3_style_dict[key]=0
	while round number<400:
		style_integer=random.randint(0,3)
		style=3_style_list[style_integer]
		if style=="soft":

		elif style=="mediumsoft":

		elif style=="medium":
			
		elif style=="mediumhard":
			
		elif style=="hard":

	
		for key in 3_style_dict:
				if key==style:
					3_style_dict[key]+=my_delta
	style=max(3_style_dict, key=lambda key: 3_style_dict[key])
	if style=="soft":

	elif style=="mediumsoft":

	elif style=="medium":
			
	elif style=="mediumhard":
			
	elif style=="hard":

	

	

		#after 200 rounds, narrow it down to the three best
		#after 400, choose the best