# Tweetpix

A small script that gets CC images from flickr, pixellizes them and publishes them on your twitter.

Create a file called `keys.py` in the same folder as the rest of the scripts, then add the following lines
```{python}
keys = dict(
    consumer_key =          'STUB',
    consumer_secret =       'STUB',
    access_token =          'STUB',
    access_token_secret =   'STUB',
    flickr_key =            'STUB',
    flickr_secret =         'STUB',
)
```
(where you replace the STUBS with your API Keys obtained from flickr and twitter).

Then the usage is pretty simple:
```{bash}
./tweetpix.py SEARCH_STRING
```
where `SEARCH_STRING` is some string used as search on flickr. The script will download a CC licensed picture searching for `SEARCH_STRING`, save it locally, pixellize it and tweet it.

E.g. 
```
./tweetpix.py "london fireworks"
(1200, 630)
#pixellized version of www.flickr.com/photos/24101343@N08/6824713499. Search 'london fireworks', baseline 72px, long side 1200px
```
produced the following tweet https://twitter.com/marcelloseri/status/664914489230426112

## Pixellize
The pixellizer library can be used as a standalone cli application:

```{bash}
./pixellize.py
Pixellize
Generates a "pixellated" copy of IMAGEFILE.

Usage:
  pixellize.py [--length=L] [--pixels=P] IMAGEFILE
  pixellize.py -h | --help

Options:
  -h --help     Show this screen.
  --length=L    Lenght of the longest edge [default: 288].
  --pixels=P    Number of pixels to appear on the longest edge [default: 72].
```
