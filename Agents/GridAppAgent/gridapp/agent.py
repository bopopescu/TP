# -*- coding: utf-8 -*- {{{
from datetime import datetime
import logging
import sys

from volttron.platform.agent import BaseAgent, PublishMixin, periodic
from volttron.platform.agent import utils, matching
from volttron.platform.messaging import headers as headers_mod
import settings
import json
import datetime
import random

utils.setup_logging()
_log = logging.getLogger(__name__)

OFFPEAK_RATE = 2.6369
PEAK_RATE = 5.7982

publish_periodic = 5

class GridAppAgent(PublishMixin, BaseAgent):
    '''Listens to everything and publishes a heartbeat according to the
    heartbeat period specified in the settings module.
    '''

    def __init__(self, config_path, **kwargs):
        super(GridAppAgent, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)

    def setup(self):
        # Demonstrate accessing a value from the config file
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']
        # Always call the base class setup()
        super(GridAppAgent, self).setup()

    # @matching.match_all
    # def on_match(self, topic, headers, message, match):
    #     '''Use match_all to receive all messages and print them out.'''
    #     _log.debug("Topic: {topic}, Headers: {headers}, "
    #                      "Message: {message}".format(
    #                      topic=topic, headers=headers, message=message))
    #     print("")

    # @matching.match_start("/ui/agent/")
    # def on_match(self, topic, headers, message, match):
    #     '''Use match_all to receive all messages and print them out.'''
    #     _log.debug("Topic: {topic}, Headers: {headers}, "
    #                      "Message: {message}".format(
    #                      topic=topic, headers=headers, message=message))
    #     print("")

    # Demonstrate periodic decorator and settings access
    @periodic(publish_periodic)
    def publish_heartbeat(self):
        '''Send heartbeat message every HEARTBEAT_PERIOD seconds.

        HEARTBEAT_PERIOD is set and can be adjusted in the settings module.
        '''
        topic = "/agent/ui/dashboard"
        now = datetime.datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
            'data_source': "gridApp"
        }
        # ***** algorithm here ******
        time_now = datetime.datetime.now()
        weekday = time_now.weekday()
        start_peak_period = time_now.replace(hour=9, minute=0, second=0, microsecond=1)
        end_peak_period = time_now.replace(hour=22, minute=0, second=0, microsecond=0)

        if (weekday == 5) | (weekday == 6) | (weekday == 7):
            current_electricity_price = round(OFFPEAK_RATE, 2)
        else:
            if (time_now >= start_peak_period) & (time_now <= end_peak_period):
                current_electricity_price = round(PEAK_RATE, 2)
            else:
                current_electricity_price = round(OFFPEAK_RATE, 2)

        message = json.dumps({'current_electricity_price': current_electricity_price})
        self.publish(topic, headers, message)
        print ("{} published topic: {}, message: {}").format(self._agent_id, topic, message)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.default_main(GridAppAgent,
                           description='Agent to feed information from grid to UI and other agents',
                           argv=argv)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
