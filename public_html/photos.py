#!/usr/bin/env python

# This code formats all of the images and syncs to the website. 

# Packages
import os
import math
import shutil
import numpy as np
from PIL import Image,ExifTags

np.random.seed(10)

imdirs = ['images/gallery_gradlife/','images/gallery_steward/']
splits = ['<!-- Grad Life Photos -->','<!-- Astro Photos -->']

def resize_photos(imdir,target_width=500):

    # Directories
    indir = imdir[:-1] + '_orig/'
    outdir = imdir
    # if os.path.isdir(outdir):
    #     shutil.rmtree(outdir)
    # os.mkdir(outdir)

    # Images
    images = [x for x in os.listdir(indir) if (('.png' in x) or ('.jpg' in x) or ('.jpeg' in x)\
              or ('.JPG' in x)  or ('.JPEG' in x) or ('.PNG' in x))]

    images_exist = [x for x in os.listdir(outdir) if (('.png' in x) or ('.jpg' in x) or ('.jpeg' in x)\
              or ('.JPG' in x)  or ('.JPEG' in x) or ('.PNG' in x))]
    
    # Keep track of heights
    heights = [0] * len(images)

    # Iterate over images
    for i,image in enumerate(images):

        # Open images
        img = Image.open(indir+image)

        # Get width and height
        width, height = img.size

        # Need to resize
        if width > target_width:
            # Get new height
            height = int(height*target_width/width)
            width = target_width

        # Keep track of height
        heights[i] = height
        
        if image not in images_exist:
            # Resize
            out = img.resize((width,height))

            # If Get Orientation if exif
            if "exif" in img.info.keys():
                exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
                }
                if 'Orientation' in exif.keys():
                    orientation = exif['Orientation']
                    if orientation == 2: out = out.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 3: out = out.rotate(180,expand=True)
                    elif orientation == 4: out = out.rotate(180,expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 5: out = out.rotate(-90,expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 6: out = out.rotate(-90,expand=True)
                    elif orientation == 7: out = out.rotate(90,expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 8: out = out.rotate(90,expand=True)

            # Save image
            out.save(outdir+image)

    return heights

def split3(array):

    height_total = np.sum(array)
    inds = np.arange(len(array))
    height_limit = height_total / 3
    
    height_cumsum = np.cumsum(array)
    indx = np.argmin( np.abs(height_cumsum - height_limit) ) + 1
    indy = np.argmin( np.abs(height_cumsum - height_cumsum[indx-1] - height_limit) ) + 1

    return inds[:indx],inds[indx:indy],inds[indy:]


def fill_photos(imdir,split,heights=[]):

    # Images
    images = [x for x in os.listdir(imdir) if (('.png' in x) or ('.jpg' in x) or ('.jpeg' in x)\
              or ('.JPG' in x)  or ('.JPEG' in x) or ('.PNG' in x))]

    # Columns 
    indicess = split3(heights)
    print(indicess)
    for indices in indicess: np.random.shuffle(indices)
    print(indicess)
    columns = [np.array(images)[indices] for indices in indicess]
    # print(columns)
    if len(images) == 0: image_string = ''
    else:
        # HTML string
        image_string = '<div class="row">\n'

        # Iterate over columns
        for column in columns:
            
            image_string += '<div class="column">\n'

            # Iterate over images
            for img in column:
                
                caption = img.split('.')[0]
                caption = caption.replace('_',' ')
                caption = caption.replace('-',' ')
                caption = caption.title()

                # Add in image
                image_string += '<div class="item">\n' +\
                                '<a href="' + imdir[:-1] + '_orig/' + str(img) + '" target="_blank">\n' +\
                                '<img src="' + imdir + str(img) + '">\n' +\
                                '<span class="caption">'+caption+'</span></a>\n</div>\n'
            
            image_string += '</div>\n'

        # Finish
        image_string += '</div>\n'

    with open('gallery.html','r+') as f: 
        html = f.read()
        html = html.split(split)
        html[1] = image_string
        f.seek(0)
        f.write(split.join(html))
        f.truncate()

check = True
for imdir,split in zip(imdirs,splits):
    heights = resize_photos(imdir)
    fill_photos(imdir,split,heights=heights)
        
os.system("rsync -avr ../public_html/ steward:/users/prospective/public_html")
