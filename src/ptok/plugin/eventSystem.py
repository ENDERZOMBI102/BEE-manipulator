import srctools.logger


__logger = srctools.logger.get_logger( 'eventSystem' )


def emit( evt: str, *args, **kwargs ) -> None:
	__logger.debug( f'invoked {evt} with args={args} and kwargs={kwargs}' )
