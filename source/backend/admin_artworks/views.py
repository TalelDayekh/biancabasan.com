from .api import (
    artworks_list_api,
    artworks_create_api,
    artworks_edit_api
)


# Artworks list
def artworks_list(request):

    all_artworks = artworks_list_api.artworks_list(request)
    return all_artworks


# Artworks create
# Create title
def artwork_create_title(request):

    create_title = artworks_create_api.artwork_create_title(request)
    return create_title

# Create details
def artwork_create_details(request):

    create_details = artworks_create_api.artwork_create_details(request)
    return create_details

# Add images
def artwork_add_images(request):

    add_image = artworks_create_api.artwork_add_images(request)
    return add_image


# Artworks edit
# Edit title
def artwork_edit_title(request, id):

    edit_title = artworks_edit_api.artwork_edit_title(request, id)
    return edit_title

# Edit details
def artwork_edit_details(request, id):

    edit_details = artworks_edit_api.artwork_edit_details(request, id)
    return edit_details