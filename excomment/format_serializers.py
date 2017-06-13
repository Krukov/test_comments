# -*- coding: utf-8 -*-

from lxml.etree import tostring
from lxml.builder import E

_serializers = {}


def serializer(cls):
    _serializers[cls.format] = cls
    return cls


def serialize(format, *args, **kwargs):
    if format not in _serializers:
        return None, None
    return _serializers[format].serialize(*args, **kwargs)


class BaseSerializer:
    format = None
    content_type = None

    def __init__(self, qs):
        self.qs = qs

    @classmethod
    def serialize(cls, qs):
        self = cls(qs)
        return self, self.content_type

    def __iter__(self):
        yield self.header
        for item in self.qs:
            yield self.serialize_item(item)
        yield self.footer

    @property
    def header(self):
        return ''

    @property
    def footer(self):
        return ''

    def serialize_item(self, item):
        raise NotImplementedError


@serializer
class XMLSerializer(BaseSerializer):
    format = 'xml'
    content_type = 'application/xml'
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<comments>'

    def serialize_item(self, item):
        return tostring(E.Comment(
            item.body,
            author=item.author.username,
            created=str(item.created),
            content_object=str(item.content_object),
        ), pretty_print=True, xml_declaration=False, encoding='UTF-8')

    footer = '</comments>'


@serializer
class HTMLSerializer(BaseSerializer):
    format = 'html'
    content_type = 'application/xml'
    header = '<html5><head></head><body><ul>'

    def serialize_item(self, item):
        return tostring(E.li(
            item.body,
            author=item.author.username,
            created=str(item.created),
            content_object=str(item.content_object),
        ), pretty_print=True, xml_declaration=False, encoding='UTF-8')

    footer = '</ul></body></html>'
