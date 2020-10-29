

class MyType(type):
    def __new__(mcs, name, bases, attrs):

        newattrs = {}
        for attrname, attrvalue in attrs.iteritems():
            if getattr(attrvalue, 'is_hook', 0):
                newattrs['__%s__' % attrname] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super(MyType, mcs).__new__(mcs, name, bases, newattrs)


class MyObject:
    __metaclass__ = MyType


class NoneSample(MyObject):
    pass

# Will print "NoneType None"
print(type(NoneSample), repr(NoneSample))