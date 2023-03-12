import logging
import os

logger = logging.getLogger("FAST_API")

current_dir = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename=current_dir + '/../../log/'+"JARVIS_SERVER_AGENT"+'.log', level=logging.DEBUG, format='[%(asctime)s %(levelname)s %(message)s]', filemode='a',)