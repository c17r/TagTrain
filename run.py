import sys
import json
import logging
import argparse
import daemonocle
import logbook

from tagtrain.tagtrain import TagTrain
from tagtrain.reddit import RedditStreamingEvents


_logger = logging.getLogger(__name__)


def get_config(path):
    with open(path, encoding='utf-8', mode='r') as f:
        raw = f.read()
    return json.loads(raw)


def config_logging():
    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("prawcore").setLevel(logging.INFO)
    logging.getLogger("peewee").setLevel(logging.INFO)
    logbook.set_datetime_format('local')
    logbook.compat.redirect_logging()

    args = create_args()
    if args.action == 'cli':
        logbook.StreamHandler(sys.stdout).push_application()
    else:
        logbook.TimedRotatingFileHandler(
            args.log_file,
            backup_count=52,
            level='INFO',
            format_string=('{record.time:%Y-%m-%d %H:%M:%S.%f}'
                           ' : {record.level_name}'
                           ' : {record.channel}'
                           ' : {record.message}')
        ).push_application()


def cb_shutdown(message, code):
    _logger.info(f'Shutdown signal triggered: {code} - {message}')


def create_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', type=str, choices=['start', 'stop', 'restart', 'status', 'cli'])
    parser.add_argument('--pid-file', type=str, default='./tagtrain.pid')
    parser.add_argument('--log-file', type=str, default='./tagtrain.log')
    parser.add_argument('--db-file', type=str, default='./tagtrain.db')
    parser.add_argument('--config-file', type=str, default='./secrets.json')

    return parser.parse_args()


def main():
    args = create_args()
    config = get_config(args.config_file)
    tagtrain = TagTrain(args.db_file)
    reddit = RedditStreamingEvents(config, tagtrain)

    while True:
        try:
            reddit.run()
        except KeyboardInterrupt:
            _logger.info('Shutdown signal received, stopping...')
            return
        except Exception as e:
            _logger.exception(f'Exception: {e}')


if __name__ == '__main__':
    args = create_args()
    config_logging()

    if args.action != 'cli':
        daemon = daemonocle.Daemon(
            worker=main,
            shutdown_callback=cb_shutdown,
            pidfile=args.pid_file,
            workdir='.'
        )
        daemon.do_action(args.action)
    else:
        main()
