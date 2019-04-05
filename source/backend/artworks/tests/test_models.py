# Unit Test
from django.test import TestCase
# Local imports
# Models
from ..models import(
    ArtworkDetails
)


class ArtworkDetailsTest(TestCase):

    def setUp(self):
        ArtworkDetails.objects.create(
            title='Starry Night',
            from_year=1889,
            to_year=1889,
            materials='Oil on canvas'
        )

        self.artwork_details = ArtworkDetails.objects.get(id=1)

    def test_title_and_materials(self):
        """
        Test for CharField. Test that title has a label of title and a
        max_length of 200, that materials has a label of materials and
        a max_length of 500. Test that both are of type CharField.
        """

        # _meta provides access to meta-information about the model
        title_label = self.artwork_details._meta.get_field('title').name
        title_type = (self.artwork_details
                        ._meta.get_field('title')
                        .get_internal_type())
        title_length = self.artwork_details._meta.get_field('title').max_length

        materials_label = self.artwork_details._meta.get_field('materials').name
        materials_type = (self.artwork_details
                            ._meta.get_field('materials')
                            .get_internal_type())
        materials_length = (self.artwork_details
                            ._meta.get_field('materials')
                            .max_length)

        self.assertEqual(title_label, 'title')
        self.assertEqual(title_length, 200)

        self.assertEqual(materials_label, 'materials')
        self.assertEqual(materials_length, 500)

        self.assertEqual((title_type and materials_type), 'CharField')
    
    def test_years(self):
        """
        Test for IntegerField. Test that years have
        a label of from_year and to_year and are of
        type IntegerField.
        """

        from_year_label = self.artwork_details._meta.get_field('from_year').name
        from_year_type = (self.artwork_details
                            ._meta.get_field('from_year')
                            .get_internal_type())
        to_year_label = self.artwork_details._meta.get_field('to_year').name
        to_year_type = (self.artwork_details
                            ._meta.get_field('to_year')
                            .get_internal_type())

        self.assertEqual(from_year_label, 'from_year')
        self.assertEqual(to_year_label, 'to_year')
        self.assertEqual((from_year_type and to_year_type), 'IntegerField')