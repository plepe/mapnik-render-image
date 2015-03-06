#!/usr/bin/env python

import sys, os
import getopt

try:
    import mapnik
except:
    try:
	import mapnik2 as mapnik
    except:
	print('Error: Need to have Mapnik installed, with python bindings enabled.')
	sys.exit()

def usage():
    print('Usage: mapnik-render-image [<options>] <map-file>')
    print
    print('Uses Mapnik to render an image using the specified map file.')
    print
    print('Options:')
    print('    -b <bounding box>, --bounds=<bounding box>')
    print('        Render the map from the specified bounding box as')
    print('        min_lon,min_lat,max_lon,max_lat, e.g.')
    print('        -6.5,49.5,2.1,59')
    print('    -s <size>, --size=<size>')
    print('        Set the resulting image size to <size>, e.g. 1024x1024')
    print('    --size-unit=[px|cm]')
    print('        Unit for the --size parameter. Defaults to \'px\'.')
    print('    -o <file>, --output=<file>')
    print('        Render the image into the specified file. The image type (png, svg, pdf)')
    print('        will be recognised from the specified extension,')
    print('        e.g. image.png (default)')
    print('    --aspect-fix-mode=[GROW_BBOX|GROW_CANVAS|SHRINK_BBOX|SHRINK_CANVAS]')
    print('        Mapnik internally will fix the aspect ratio of the bounding box to')
    print('        match the target image width and height but it can also change the')
    print('        target image size to match the bounding box. Default: GROW_BBOX')
    print('    --scale=<scale_denominator>|z<zoom>')
    print('        Render image at a specified scale denominator. If z<zoom> syntax')
    print('        (e.g. "z15") is used, the zoom levels of projection 900913 are used.')
    print('        This setting has precedence over the image target size.')
    print('    --buffer=<buffer size>')
    print('        Add a buffer around the image. (default: 0)')
    print('    --image-type=<type>')
    print('        Specify a specific image type, e.g. "jpeg85" or "png8:c=128".')
    print('        See https://github.com/mapnik/mapnik/wiki/Image-IO for a list')
    print('        of available formats.')
    print('    -h, --help')
    print('        Show usage information')

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
# Default bounding box
    bounds = (-6.5, 49.5, 2.1, 59)

# Default size
    imgx = 1024
    imgy = 1024

# Default output file name
    map_uri = "image.png"

# Aspect fix mode
    aspect_fix_mode = "GROW_BBOX"

# Adapt scale denominator
    scale_denom = 0

# Buffer size
    buffer_size = 0

# Image type
    image_type = None

# Size Unit
    size_unit = 'px'
    size_units = {
        'px': 1.0,
        'cm': 0.0353,
    }
#
# Process parameters
#
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'b:s:o:h', ["bounds=", "size=", "size-unit=", "output=","aspect-fix-mode=","scale=","buffer=","image-type=","help"])
    except getopt.GetoptError as err:
	print(err)
	usage()
	sys.exit()

    for o, a in opts:
	if o in ("-b", "--bounds"):
	    bounds = map(float, a.split(","))
	elif o in ("-s", "--size"):
	    a = a.split("x");
	    imgx = float(a[0]);
	    imgy = float(a[1]);
	elif o in ("--size-unit"):
            if not a in size_units:
                print('Size unit "{}" not known!'.format(a))
                sys.exit

	    size_unit = a
	elif o in ("-o", "--output"):
	    map_uri = a;
	elif o in ("--aspect-fix-mode"):
	    if a in ("GROW_BBOX", "GROW_CANVAS", "SHRINK_BBOX", "SHRINK_CANVAS"):
		aspect_fix_mode = a;
	    else:
		usage()
		sys.exit()
	elif o in ("--scale"):
            if a[0] == 'z':
                scale_denom = 559082264.028 / (2 ** int(a[1:]))
            else:
                scale_denom = float(a)
	elif o in ("--buffer"):
	    buffer_size = int(a)
	elif o in ("--image-type"):
	    image_type = a
	elif o in ("-h", "--help"):
	    usage()
	    sys.exit()
	else:
	    usage()
	    sys.exit()

    imgx = int(round(float(imgx) / size_units[size_unit]))
    imgy = int(round(float(imgy) / size_units[size_unit]))

# check if a map file has been specified
    if len(args):
	mapfile = args[0]
    else:
	print('Error: No map file specified')
	usage()
	sys.exit()

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
    
    # If a scale denominator is specified
    if scale_denom:
        # Get current scale denom, calculate necessary change
        scale_change = scale_denom / m.scale_denominator()
        # Resize image size
        m.zoom(scale_change)

    # Set the buffer size
    m.buffer_size = buffer_size;

    ## render the map to an image
    #im = mapnik.Image(imgx,imgy)
    #mapnik.render(m, im)
    #im.save(map_uri,'png')

    # Render file with mapnik.render_to_file()
    if image_type == None:
	mapnik.render_to_file(m, map_uri)
    else:
	mapnik.render_to_file(m, map_uri, image_type)

    # Print stats
    print("Stats:")
    print("  Mapnik version: " + mapnik.mapnik_version_string())
    print("  Using map file: " + mapfile)
    print("  Using bounds: " + repr(bounds))
    print("  Scale Denominator: " + str(m.scale_denominator()))
    print("  Render into file: " + map_uri)
    print("  Image size: " + str(m.width) + "x" + str(m.height))
