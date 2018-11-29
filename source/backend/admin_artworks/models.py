from django.db import models

from django.conf import settings


"""
Artwork title
"""
class ArtworkTitle(models.Model):
    title = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)
    
    # Connect data to user
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        )
    
    def __str__(self):
        return (
            str('Title: ') 
            + self.title + str(' ID: ') 
            + str(self.id) + str(' Owner: ') 
            + str(self.owner)
            )


"""
Artwork details
"""
class ArtworkDetails(models.Model):
    title_id = models.ForeignKey(
        ArtworkTitle,
        on_delete = models.CASCADE,
    )
    height = models.FloatField()
    width = models.FloatField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return (
            str('Description: ') 
            + self.description + str(' ID: ') 
            + str(self.title_id.id) 
            + str(' Owner: ') 
            + str(self.title_id.owner)
            )





# """
# Artwork images
# """
# class ArtworkImages(models.Model):
#     title_id = models.ForeignKey(ArtworkTitle, on_delete=models.CASCADE)
#     images = models.ImageField(upload_to='images')
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.images)