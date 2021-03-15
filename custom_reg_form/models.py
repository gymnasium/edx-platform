from django.conf import settings
from django.db import models

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class ExtraInfo(models.Model):
    """
    This model contains two extra fields that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """

    user = models.OneToOneField(USER_MODEL, null=True)
    MARKETS = (
        ("0", "N/A"),
        ("23", "Atlanta"),
        ("60", "Austin"),
        ("46", "Baltimore"),
        ("102", "Boise"),
        ("10", "Boston"),
        ("61", "Charlotte"),
        ("14", "Chicago"),
        ("34", "Connecticut"),
        ("22", "Dallas"),
        ("27", "Denver"),
        ("24", "Detroit"),
        ("826", "Houston"),
        ("58", "Indianapolis"),
        ("13", "Los Angeles"),
        ("33", "Miami"),
        ("20", "Minneapolis"),
        ("807", "Moline"),
        ("30", "New Jersey"),
        ("11", "New York City"),
        ("51", "Northern Virginia"),
        ("32", "Ohio"),
        ("19", "Orange County"),
        ("72", "Orlando"),
        ("18", "Philadelphia"),
        ("31", "Phoenix"),
        ("41", "Portland, OR"),
        ("803", "Raleigh/Durham"),
        ("73", "Rhode Island"),
        ("78", "Richmond"),
        ("16", "San Diego"),
        ("12", "San Francisco"),
        ("17", "Seattle"),
        ("15", "Silicon Valley"),
        ("37", "St. Louis"),
        ("68", "Tampa"),
        ("881", "Wisconsin"),
        ("40", "Toronto"),
        ("47", "Vancouver"),
        ("43", "Amsterdam"),
        ("29", "London"),
        ("36", "Melbourne"),
        ("39", "Sydney"),
        ("92", "Fukuoka"),
        ("79", "Nagoya"),
        ("64", "Osaka"),
        ("44", "Tokyo"),
    )
    market = models.CharField(
        verbose_name="Select Nearest Region",
        choices=MARKETS,
        blank=False,
        max_length=5,
    )
