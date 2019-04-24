import sys
import json
import logging
import argparse
import daemonocle
import logbook
from raven.handlers.logbook import SentryHandler

from . import data
from .reddit import RedditStreamingEvents
from .tagtrain import TagTrain

_logger = logging.getLogger(__name__)


def get_config(path):
    with open(path, encoding='utf-8', mode='r') as f:
        raw = f.read()
    return json.loads(raw)


def config_logging(args):
    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("prawcore").setLevel(logging.INFO)
    logging.getLogger("peewee").setLevel(logging.INFO)
    logbook.set_datetime_format('local')
    logbook.compat.redirect_logging()

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
                           ' : {record.message}'),
            bubble=True
        ).push_application()
        config_sentry(args)


def config_sentry(args):
    # Configure the default client
    config = get_config(args.config_file)
    if 'sentry_dsn' not in config or not config['sentry_dsn']:
        return

    handler = SentryHandler(
        config['sentry_dsn'],
        level='INFO',
        bubble=True
    ).push_application()


def cb_shutdown(message, code):
    _logger.info(f'Shutdown signal triggered: {code} - {message}')


def create_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', type=str, choices=['start', 'stop', 'restart', 'status', 'cli'])
    parser.add_argument('--pid-file', type=str, default='./tagtrain.pid')
    parser.add_argument('--log-file', type=str, default='./tagtrain.log')
    parser.add_argument('--db-file', type=str, default='./tagtrain.db')
    parser.add_argument('--config-file', type=str, default='./config.json')

    return parser.parse_args()


def bootstrap():
    args = create_args()
    config = get_config(args.config_file)

    data.init(args.db_file)
    tag_train = TagTrain(config)

    reddit = RedditStreamingEvents(config, tag_train)

    while True:
        try:
            reddit.run()
        except KeyboardInterrupt:
            _logger.info('Shutdown signal received, stopping...')
            return
        except Exception as e:
            _logger.exception(f'Exception: {e}')


def main():
    args = create_args()
    config_logging(args)

    if args.action != 'cli':
        daemon = daemonocle.Daemon(
            worker=bootstrap,
            shutdown_callback=cb_shutdown,
            pidfile=args.pid_file,
            workdir='.'
        )
        daemon.do_action(args.action)
    else:
        bootstrap()


if __name__ == '__main__':
    sys.exit(main())
