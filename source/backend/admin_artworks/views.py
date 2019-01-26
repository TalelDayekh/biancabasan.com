from .api import(
    list_artworks_endpoints,
    create_artworks_endpoints
)


# Views for listing artworks
def artworks_list(request):
    all_artworks = list_artworks_endpoints.artworks_list(request)
    return all_artworks


# Views for adding new artworks
def create_artwork_info(request):
    create_info = create_artworks_endpoints.create_artwork_info(request)
    return create_info

def add_artwork_images(request):
    add_image = create_artworks_endpoints.add_artwork_images(request)
    return add_image