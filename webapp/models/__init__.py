from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy
from sqlalchemy import create_engine

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
#from .mymodel import Base, organism, Features  # flake8: noqa
from .mlva import Base, plasmid, mst, TypingMeta, mlvaProfile, SampleMetadata
from .mlva_results import Base, ProductLength, FlankLength, RepeatSize, RepeatNumber
from .submission import Base, SubmissionTable, mlvaSubmission, mstSubmission, isolateSubmission
from .mst_results import Base, mstSpacerResult
from .signup import UserTable
from .is1111 import is1111Profile
from .adaA import adaAProfile
from .snp_hornstra import snpHornstra 
from .phylotree import NewickTable 
from .accesstable import accessTable
# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()

class DBFactory(object):

    def __init__(self, db_url, **kwargs):
        db_echo = kwargs.get('db_echo', False)
        self.engine = create_engine(db_url, echo=db_echo)

        self.DBSession = sessionmaker(autoflush=False)
        self.DBSession.configure(bind=self.engine)
        self.metadata = Base.metadata
        self.metadata.bind = self.engine

    def get_session(self):
        session = self.DBSession()
        return session
#def get_engine(settings, prefix='db1.'):
#    return engine_from_config(settings, prefix)
#
#
#def get_session_factory(engine):
#    factory = sessionmaker()
#    factory.configure(bind=engine)
#    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('webapp.models')``.

    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')

#    session_factory = get_session_factory(get_engine(settings))
#    config.registry['dbsession_factory'] = session_factory
    config.registry.db1_factory = DBFactory( db_url=settings['db1.url'] )
    config.registry.db2_factory = DBFactory( db_url=settings['db2.url'] )

    # make request.dbsession available for use in Pyramid
#    config.add_request_method(
#        # r.tm is the transaction manager used by pyramid_tm
#        lambda r: get_tm_session(session_factory, r.tm),
#        'dbsession',
#        reify=True
#    )
