# coding: utf-8


# examples/entity.py

import uuid

# Example of enitity


class Event:
    pass


class DomainEvent:
    pass


class Entity(abc.ABC):
    """
    The base class of all entities.

    Attributes:
        id: A unique identifier
        instance_id: A value unique among instances of this entity.
        version: An integer version
        discarded: True if this entity should or not longer be used.
    """

    _instance_id_generator = uuid.uuid1()

    class CreatedData(DomainEvent):
        pass

    class Discarted(DomainEvent):
        pass

    @abc.abstractmethod
    def __init__(self, entity_id, entity_version):
        self._id = entity_id
        self._version = entity_version
        self._discarded = False
        self._instalce_id = uuid.uuid1()

    def _increment_version(self):
        self._version += 1

    @property
    def instance_id(self):
        """ A value unique among instances of this entity """
        return self._instalce_id

    @property
    def id(self):
        """ A string unique identifier for the entity. """
        self._check_not_discarded()
        return self._id

    @property
    def version(self):
        """ An integer version for the entity. """
        self._check_not_discarded()
        return self._version

    @property
    def discarded(self):
        """ True if this entity is marked as discarded, otherwise False. """
        return self._discarded

    def _check_not_discarded(self):
        if self._discarded:
            raise DiscardedEntityError(f"Attempt to use {self}")


class DiscardedEntityError(Exception):
    """ Raised when an attempt is made to use a discarded Entity. """

    pass
 