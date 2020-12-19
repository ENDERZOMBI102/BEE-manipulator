import sqlalchemy as sqla
from sqlalchemy import create_engine, text

from srctools.logger import get_logger

logger = get_logger()

engine: sqla.engine.Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


class Database:

	def setup( self ):
		if not engine.has_table('BEEPACKAGES'):
			with engine.connect() as conn:
				conn.execute( text('CREATE TABLE BEEPACKAGES (identifier)') )
				conn.commit()
