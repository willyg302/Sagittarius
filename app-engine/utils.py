#!/usr/local/bin/python
# coding: utf-8

from google.appengine.ext import ndb

 
class DynamicPropertyMixin(object):
    """ Facilitates creating dynamic properties on ndb.Expando entities. Any
    keyword args specified are passed onto the underlying ndb___Property() class.

    Note: getattr() works absolutely fine. However any update of a property that has
    been created using this class MUST use the method again, not setattr().
    """
 
    def is_prop(self, name):
        return name in self._properties
 
    def set_dynamic_prop(self, cls, name, value, **kwds):
        prop = cls(name, **kwds)
        prop._code_name = name
        self._properties[name] = prop
        prop._set_value(self, value)

    #--- Generic unindexed property (blob properties use the ones below)
 
    def set_unindexed_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.GenericProperty, name, value, indexed=False, **kwds)
 
    #--- The blob properties ---
 
    def set_blob_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.BlobProperty, name, value, **kwds)
 
    def set_text_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.TextProperty, name, value, **kwds)
 
    def set_pickle_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.PickleProperty, name, value, **kwds)
 
    def set_json_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.JsonProperty, name, value, **kwds)
 
    #--- Useful non-blob properties ---
 
    def set_string_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.StringProperty, name, value, **kwds)
 
    def set_integer_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.IntegerProperty, name, value, **kwds)
 
    def set_float_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.FloatProperty, name, value, **kwds)
 
    def set_datetime_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.DateTimeProperty, name, value, **kwds)
 
    def set_key_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.KeyProperty, name, value, **kwds)
 
    #--- Less useful non-blob properties ---
 
    def set_generic_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.GenericProperty, name, value, **kwds)
 
    def set_boolean_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.BooleanProperty, name, value, **kwds)
 
    def set_date_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.DateProperty, name, value, **kwds)
 
    def set_time_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.TimeProperty, name, value, **kwds)
 
    def set_user_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.UserProperty, name, value, **kwds)
 
    def set_geopt_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.GeoPtProperty, name, value, **kwds)
 
    def set_blobkey_prop(self, name, value, **kwds):
        self.set_dynamic_prop(ndb.BlobKeyProperty, name, value, **kwds)