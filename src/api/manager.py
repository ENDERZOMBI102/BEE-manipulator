from abc import ABCMeta, abstractmethod


class Manager(metaclass=ABCMeta):

	@abstractmethod
	def init( self ) -> None:
		""" Initialize a manager object, may be called to reset a manager """
		pass

	@abstractmethod
	def stop( self ) -> None:
		""" Finalize a manager object, must be called before destruction """
		pass
