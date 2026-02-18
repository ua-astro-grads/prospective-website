# Website Code for Prospective Grad Visit

## Gaining Access

The first step is to open a ticket with the computer support group and request access to the prospective 
graduate website hosted at as.arizona.edu/~prospective. _This is the most important step because the 
remained of these instructions are more or less a year old and Kiriaki will be able to give you any
relevant updates_.

On the machine where the website is hosted, the code is in `/containers/lavinia/users/prospective`. In
that directory you will see
1. A `prospective-website` directory: This is a local copy of this github repository
2. A `public_html` directory: This should be a soft link to `prospective-website/public_html`. This is needed because the website is actually deployed from `/containers/lavinia/users/prospective/public_html`
3. Various other directories labelled as "old" that you can ignore

## Installation and Deployment

I would strongly recommend doing your development locally. To do this:
1. Clone this repository to your desktop to `$prospective-website-path`
2. rsync the remote `/containers/lavinia/users/prospective/prospective-website/public_html/images` directory to `$prospective-website-path/public_html/images`. The images are too large to store on github so they are stored remotely on the server.
3. Then you can open the website using (on linux) `xdg-open $prospective-website-path/public_html/index.html`
4. Make your relevant changes, commit, and push to github

To deploy these changes that you made locally
1. ssh into the remote server
2. Navigate to `/containers/lavinia/users/prospective/prospective-website/` and `git pull`
3. See below if you made updates to the images

### To update images
After receiving new images from graduate students you should download them locally and add them to either
`$prospective-website-path/public_html/images/gallery_gradlife` (for images of grad students living their life) 
or `$prospective-website-path/public_html/images/gallery_steward` (for images of facilities).

Previously, it was necessary to add all of these images to the HTML by hand. I've attempted to automate this with
javascript. All you need to do after adding new images is execute the `$prospective-website-path/public_html/pre-img-dir.sh` script
and it should generate a file recognized by the javascript/HTML. *Note:* No spaces in the image names and no HEIC files!

After running this script, push to github, pull on the server, and rsync the images directory to the server. The
production deployment of the website should then update to match your local copy.
