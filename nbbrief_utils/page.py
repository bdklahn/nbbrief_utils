from dataclasses import dataclass

@dataclass
class Page():
    """Bind together some information about a nbbrief site
    page."""
    name: str
    title: str
    nb_location: str = './'
    enabled: bool = True
