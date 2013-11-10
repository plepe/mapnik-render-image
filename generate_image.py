#!/usr/bin/env python

try:
    import mapnik2 as mapnik
except:
    import mapnik

import sys, os
import getopt

def usage():
    print('Usage: generate_image.py [<options>]')
    print
    print('Options:')
    print('    -m <file>, --map-file=<file>')
    print('        Use the specified file as mapnik map file')
    print('    -b <bounding box>, --bounds=<bounding box>')
    print('        Render the map from the specified bounding box as')
    print('        min_lon,min_lat,max_lon,max_lat, e.g.')
    print('        -6.5,49.5,2.1,59')
    print('    -s <size>, --bounds=<size>')
    print('        Set the resulting image size to <size>, e.g. 1024x1024')
    print('    -o <file>, --output=<file>')
    print('        Render the image into the specified file. The image type (png, svg, pdf)')
    print('        will be recognised from the specified extension,')
    print('        e.g. image.png (default)')
    print('    --aspect-fix-mode=[GROW_BBOX|GROW_CANVAS|SHRINK_BBOX|SHRINK_CANVAS]')
    print('        Mapnik internally will fix the aspect ratio of the bounding box to')
    print('        match the target image width and height but it can also change the')
    print('        target image size to match the bounding box. Default: GROW_BBOX')

# Set up projections
# spherical mercator (most common target map projection of osm data imported with osm2pgsql)
merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')

# long/lat in degrees, aka ESPG:4326 and "WGS 84" 
longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
# can also be constructed as:
#longlat = mapnik.Projection('+init=epsg:4326')

# ensure minimum mapnik version
if not hasattr(mapnik,'mapnik_version') and not mapnik.mapnik_version() >= 600:
    raise SystemExit('This script requires Mapnik >=0.6.0)')

if __name__ == "__main__":
# Default mapfile: osm.xml or read from env
    try:
        mapfile = os.environ['MAPNIK_MAP_FILE']
    except KeyError:
        mapfile = "osm.xml"

# Default bounding box
    bounds = (-6.5, 49.5, 2.1, 59)

# Default size
    imgx = 1024
    imgy = 1024

# Default output file name
    map_uri = "image.png"

# Aspect fix mode
    aspect_fix_mode = "GROW_BBOX"

    try:
	opts, args = getopt.getopt(sys.argv[1:], 'm:b:s:o:', ["map-file=", "bounds=", "size=", "output=","aspect-fix-mode="])
    except getopt.GetoptError as err:
	print(err)
	usage()
	sys.exit()

    for o, a in opts:
	if o in ("-m", "--map-file"):
	    mapfile = a;
	elif o in ("-b", "--bounds"):
	    bounds = map(float, a.split(","))
	elif o in ("-s", "--size"):
	    a = a.split("x");
	    imgx = int(a[0]);
	    imgy = int(a[1]);
	elif o in ("-o", "--output"):
	    map_uri = a;
	elif o in ("--aspect-fix-mode"):
	    if a in ("GROW_BBOX", "GROW_CANVAS", "SHRINK_BBOX", "SHRINK_CANVAS"):
		aspect_fix_mode = a;
	    else:
		usage()
		sys.exit()
	else:
	    usage()
	    sys.exit()

    print("Using map file: " + mapfile)
    print("Using bounds: " + repr(bounds))
    print("Render into file: " + map_uri)

    m = mapnik.Map(imgx,imgy)
    mapnik.load_map(m,mapfile)
    
    # ensure the target map projection is mercator
    m.srs = merc.params()

    if hasattr(mapnik,'Box2d'):
        bbox = mapnik.Box2d(*bounds)
    else:
        bbox = mapnik.Envelope(*bounds)

    # Our bounds above are in long/lat, but our map
    # is in spherical mercator, so we need to transform
    # the bounding box to mercator to properly position
    # the Map when we call `zoom_to_box()`
    transform = mapnik.ProjTransform(longlat,merc)
    merc_bbox = transform.forward(bbox)
    
    # Mapnik internally will fix the aspect ratio of the bounding box
    # to match the aspect ratio of the target image width and height
    # This behavior is controlled by setting the `m.aspect_fix_mode`
    # and defaults to GROW_BBOX, but you can also change it to alter
    # the target image size by setting aspect_fix_mode to GROW_CANVAS
    if aspect_fix_mode == "GROW_BBOX":
	m.aspect_fix_mode = mapnik.aspect_fix_mode.GROW_BBOX
    elif aspect_fix_mode == "GROW_CANVAS":
	m.aspect_fix_mode = mapnik.aspect_fix_mode.GROW_CANVAS
    elif aspect_fix_mode == "SHRINK_BBOX":
	m.aspect_fix_mode = mapnik.aspect_fix_mode.SHRINK_BBOX
    else:
	m.aspect_fix_mode = mapnik.aspect_fix_mode.SHRINK_CANVAS

    # Note: aspect_fix_mode is only available in Mapnik >= 0.6.0
    m.zoom_to_box(merc_bbox)
    
    ## render the map to an image
    #im = mapnik.Image(imgx,imgy)
    #mapnik.render(m, im)
    #im.save(map_uri,'png')

    # Render file with mapnik.render_to_file()
    mapnik.render_to_file(m, map_uri)
