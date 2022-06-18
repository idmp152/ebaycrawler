from pkg_resources import get_distribution

__distribution = get_distribution("ebaycrawler")
__metadata = __distribution.get_metadata('METADATA')


#Does not really contain all the metadata because Requires-Dist is a repeating key
__metadata_dict = {k[0].strip(): k[1].strip() for k in [i.split(
                                ':') for i in __metadata.split('\n') if len(i.split(':')) == 2]}

__version__ = __distribution.version
__author__ = __metadata_dict["Author"]
__author_email__ = __metadata_dict["Author-email"]
