# -*- coding: utf-8 -*-
'''
author: Lin Peng
create_time:2018.12.08 21:30
organization:Fudan University
introduction: create kml file for Google Earth through existing path
'''
path = [(90, 14, 100), (89, 13, 99), (88, 12, 98), (87, 11, 97), (86, 10, 96),
       (85, 9, 95), (84, 8, 94), (83, 7, 93), (82, 6, 92), (81, 5, 91), (80, 4, 90),
        (79, 3, 89), (78, 2, 88), (77, 1, 87), (76, 1, 86), (75, 1, 85), (74, 1, 84), (73, 1, 83),
        (72, 1, 82), (71, 1, 81), (70, 1, 80), (69, 1, 79), (68, 1, 78), (67, 1, 77), (66, 1, 76),
        (65, 1, 75), (64, 1, 74), (63, 1, 73), (62, 1, 72), (61, 1, 71), (60, 1, 70), (59, 1, 69),
        (58, 1, 68), (57, 1, 67), (56, 1, 66), (55, 1, 65), (54, 1, 64), (53, 1, 63), (52, 1, 62),
        (51, 1, 61), (50, 1, 60), (49, 1, 59), (48, 1, 58), (47, 1, 57), (46, 1, 56), (45, 1, 55),
        (44, 1, 54), (43, 1, 53), (42, 1, 52), (41, 1, 51), (40, 1, 50), (39, 1, 49), (38, 1, 48),
        (37, 1, 47), (36, 1, 46), (35, 1, 45), (34, 1, 44), (33, 1, 43), (32, 1, 42), (31, 1, 41),
        (30, 1, 40), (29, 1, 39), (28, 1, 38), (27, 1, 37), (26, 1, 36), (25, 1, 35), (24, 1, 34),
        (23, 1, 33), (22, 1, 32), (21, 1, 31), (20, 1, 30), (19, 1, 29), (18, 1, 28), (17, 1, 27),
        (16, 1, 26), (15, 1, 25), (14, 1, 24), (13, 1, 23), (12, 1, 22), (11, 1, 21), (10, 1, 20),
        (9, 1, 19), (8, 1, 18), (7, 1, 17), (6, 1, 16), (5, 1, 15), (4, 1, 14), (3, 1, 13), (2, 1, 12),
        (1, 1, 11), (1, 1, 10), (1, 1, 9), (1, 1, 8), (1, 1, 7), (1, 1, 6), (1, 1, 5)]

lon_yuan = 121.500045-5*0.000292/29.3087+5*0.000149/43.6147
lat_yuan = 31.301513-5*0.000085/29.3087-5*0.000371/43.6147
alt_yuan = 5

path_lon = [0 for i in range(len(path))]
path_lat = [0 for i in range(len(path))]
path_alt = [0 for i in range(len(path))]

for i in range(len(path)):
    path_lon[i] = lon_yuan + path[i][0]*0.000292/29.3087 - path[i][1]*0.000149/43.6147
    path_lat[i] = lat_yuan + path[i][0]*0.000085/29.3087 + path[i][1]*0.000371/43.6147
    path_alt[i] = alt_yuan + path[i][2]

f = open('C:\Users\Dell-13\Desktop\\test1.kml', 'a')

f.truncate()

f.write('<?xml version="1.0" encoding="UTF-8"?>\n\
<kml xmlns="http://www.opengis.net/kml/2.2" \
xmlns:gx="http://www.google.com/kml/ext/2.2" \
xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n\
<Document>\n\
	<name>测试路径.kml</name>\n\
	<Placemark>\n\
		<name>未命名路径</name>\n\
		<Style>\n\
			<LineStyle>\n\
				<color>ffff1600</color>\n\
				<width>6</width>\n\
			</LineStyle>\n\
		</Style>\n\
		<LineString>\n\
			<altitudeMode>relativeToGround</altitudeMode>\n\
			<coordinates>\n')
for i in range(len(path)):
    f.write('				' + str(path_lon[i]) + ',' + str(path_lat[i]) + ',' + str(path_alt[i])+'\n')

f.write('			</coordinates>\n\
		</LineString>\n\
	</Placemark>\n\
</Document>\n\
</kml>')

f.close()
