mapnik-render-image
===================
Use Mapnik to render an image file. It is being developed on Github:
https://github.com/plepe/mapnik-render-image

This is an improved version of generate_image.py from the OpenStreetMap SVN:
http://svn.openstreetmap.org/applications/rendering/mapnik/generate_image.py

Feel invited to fork the repository, improve the code base and finally
contribute back. This is free software!

Installation
------------
```sh
make install
```

Usage
-----
```
Usage: mapnik-render-image [<options>] <map-file>

Uses Mapnik to render an image using the specified map file.

Options:
    -b <bounding box>, --bounds=<bounding box>
        Render the map from the specified bounding box as
        min_lon,min_lat,max_lon,max_lat, e.g.
        -6.5,49.5,2.1,59
    -s <size>, --size=<size>
        Set the resulting image size to <size>, e.g. 1024x1024
    -o <file>, --output=<file>
        Render the image into the specified file. The image type (png, svg, pdf)
        will be recognised from the specified extension,
        e.g. image.png (default)
    --aspect-fix-mode=[GROW_BBOX|GROW_CANVAS|SHRINK_BBOX|SHRINK_CANVAS]
        Mapnik internally will fix the aspect ratio of the bounding box to
        match the target image width and height but it can also change the
        target image size to match the bounding box. Default: GROW_BBOX
    --scale=<scale_denominator>|z<zoom>
        Render image at a specified scale denominator. If z<zoom> syntax
        (e.g. "z15") is used, the zoom levels of projection 900913 are used.
        This setting has precedence over the image target size.
    --buffer=<buffer size>
        Add a buffer around the image. (default: 0)
    --image-type=<type>
        Specify a specific image type, e.g. "jpeg85" or "png8:c=128".
        See https://github.com/mapnik/mapnik/wiki/Image-IO for a list
        of available formats.
    -h, --help
        Show usage information
```
