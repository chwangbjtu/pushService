import sys
sys.path.append('.')
import traceback
from tornado import log
from service.dispatch_service import CrawlerDispatcher
class EpisodeThumb(object):

    def start(self):
        try:
            print "episode thumb crawler start..."
            log.app_log.debug('episode thumb crawler start...') 
            crawler_dispatcher = CrawlerDispatcher()
            crawler_dispatcher.start()
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        
if __name__ == "__main__":
    episode_thumb = EpisodeThumb()
    episode_thumb.start()
        
