from log_manager import LogManager

#log_manager = LogManager()
log_manager = LogManager('log_manager_config.json')
log_manager.info('test')
log_manager.error('test')
log_manager.warning('test')
log_manager.debug('test')
log_manager.critical('test')