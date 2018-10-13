import googlemaps, geocoder

gmap_key = googlemaps.Client('AIzaSyD5fxC6_orK_rww6VBl3p5m2_OXO8lb_wU')

curr_loc = geocoder.ip('me').latlng