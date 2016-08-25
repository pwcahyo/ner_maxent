import operator

loc = {"bekasi":10,"jakarta":4,"tangerang":8,"barat":5,"utara":11,"daya":6,"dari":3,"jaya":9}

sort_loc = sorted(loc.items(), key=operator.itemgetter(1))


dist_loc = 0
arr_temp_loc = []
arr_loc = []
for loc_in_search in sort_loc:
	dist_loc = abs(dist_loc) - loc_in_search[1]
	abs_dist_loc = abs(dist_loc)
	if (not arr_loc) or abs_dist_loc==1:
		#apabila arr_loc kosong atau jarak indek kata lokasi = 1
		#maka arr_loc append index
	 	arr_loc.append(loc_in_search[0])
	 	#reset dist_location
	 	dist_loc = loc_in_search[1]
	 	if abs_dist_loc != 1:
	 		#apabila jarak != 1
	 		#append grup arr lokasi
	 		arr_temp_loc.append(arr_loc)
	 		#reset dist_location
	 		dist_loc = loc_in_search[1]
	else:
		#reset dist_location
		dist_loc = loc_in_search[1]
		#reset arr location
		arr_loc = []
		arr_loc.append(loc_in_search[0])
		arr_temp_loc.append(arr_loc)

print arr_temp_loc