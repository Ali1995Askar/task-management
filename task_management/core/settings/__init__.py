import logging
from .base import WORKING_SETTINGS

logger = logging.getLogger(__name__)

if WORKING_SETTINGS == 'LOCAL':
    from .local import *


elif WORKING_SETTINGS == 'DOCKER':
    from .docker import *

elif WORKING_SETTINGS == 'STAGE':
    from .staging import *

    


else:
    raise ImportError("The settings specified are not available, check WORKING_SETTINGS is set correctly")

logger.info(f"Starting server with {WORKING_SETTINGS} settings ..")