# Unit Test
from django.test import TestCase
# Local imports
# Models
from ..models import(
    ArtworkDetails
)


class ArtworkDetailsTest(TestCase):
    # Call setUpTestData() for objects that are not
    # going to be modified or changed in any of the
    # test methods.
    @classmethod
    def setUpTestData(cls):
        """
        Create an ArtworkDetails object and set
        details to be used in all test methods.
        """

        ArtworkDetails.objects.create(
            title='Starry Night',
            from_year=1889,
            to_year=1889
        )

    def test_title(self):
        """
        Test that title has a label of title, is of
        type CharField and has a max_length of 200.
        """

        artwork_details = ArtworkDetails.objects.get(id=1)

        # _meta provides access to meta-information about the model
        title_label = artwork_details._meta.get_field('title').name
        title_type = (artwork_details
                        ._meta.get_field('title')
                        .get_internal_type())
        title_length = artwork_details._meta.get_field('title').max_length

        self.assertEqual(title_label, 'title')
        self.assertEqual(title_type, 'CharField')
        self.assertEqual(title_length, 200)
    
    def test_years(self):
        """
        Test that years have a label of from_year
        and to_year and are of type IntegerField.
        """

        artwork_details = ArtworkDetails.objects.get(id=1)

        from_year_label = artwork_details._meta.get_field('from_year').name
        from_year_type = (artwork_details
                            ._meta.get_field('from_year')
                            .get_internal_type())
        to_year_label = artwork_details._meta.get_field('to_year').name
        to_year_type = (artwork_details
                            ._meta.get_field('to_year')
                            .get_internal_type())

        self.assertEqual(from_year_label, 'from_year')
        self.assertEqual(to_year_label, 'to_year')
        self.assertEqual((from_year_type and to_year_type), 'IntegerField')