import enum


class ApplicationStatus(enum.Enum):
    DRAFT = "draft"
    SUMITTED = "submitted"
    PROCESSING = "processing"
    REQUESTED_CHANGES = "requested_changes"
    PROCESSED = "processed"


REGIONS = (
    ("AHAFO", "AHAFO"),
    ("ASHANTI", "ASHANTI"),
    ("BONO EAST", "BONO EAST"),
    ("BRONG AHAFO", "BRONG AHAFO"),
    ("CENTRAL", "CENTRAL"),
    ("EASTERN", "EASTERN"),
    ("GREATER ACCRA", "GREATER ACCRA"),
    ("NORTH EAST", "NORTH EAST"),
    ("NORTHERN", "NORTHERN"),
    ("OTI", "OTI"),
    ("SAVANNAH", "SAVANNAH"),
    ("UPPER EAST", "UPPER EAST"),
    ("UPPER WEST", "UPPER WEST"),
    ("WESTERN", "WESTERN"),
    ("WESTERN NORTH", "WESTERN NORTH"),
    ("VOLTA", "VOLT"),
)
