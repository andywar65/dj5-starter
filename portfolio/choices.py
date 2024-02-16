from django.utils.translation import gettext_lazy as _

CATEGORY = [
    ("ALT", _("Other category")),
    ("RES", _("Residential")),
    ("TER", _("Offices")),
    ("SAN", _("Healthcare")),
    ("PRO", _("Production")),
    ("SCO", _("Instruction")),
    ("ACC", _("Accommodation")),
]

TYPE = [
    ("ALT", _("Other intervention")),
    ("ARR", _("Furniture")),
    ("RIS", _("Refurbishment")),
    ("RES", _("Restoration")),
    ("AMP", _("Extension")),
    ("COS", _("Construction")),
    ("DEM", _("Demolition")),
]

STATUS = [
    ("ALT", _("Status unknown")),
    ("PRO", _("Designed")),
    ("COR", _("Under construction")),
    ("REA", _("Done")),
]

COST = [
    ("ALT", _("Other")),
    ("1K", "1K"),
    ("2K", "2K"),
    ("5K", "5K"),
    ("10K", "10K"),
    ("20K", "20K"),
    ("50K", "50K"),
    ("100K", "100K"),
    ("200K", "200K"),
    ("500K", "500K"),
    ("1M", "1M"),
    ("2M", "2M"),
    ("5M", "5M"),
    ("10M", "10M"),
    ("20M", "20M"),
    ("50M", "50M"),
]

ACTIVITY = [
    ("LP0", _("Other activity")),
    ("LP1", _("Feasibility study")),
    ("LP2", _("Preliminary design")),
    ("LP3", _("Definitive design")),
    ("LP4", _("Authoring")),
    ("LP5", _("Construction design")),
    ("LP6", _("Tender design")),
    ("LP7", _("Project management")),
    ("LP8", _("Construction supervision")),
    ("LP9", _("Maintenance design")),
    ("LPA", _("All activities")),
]
