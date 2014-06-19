import copy
import pdb

class frozendict(dict):
    def _blocked_attribute(obj):
        raise AttributeError, "A frozendict cannot be modified."
    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute

    def __new__(cls, *args, **kw):
        new = dict.__new__(cls)

        args_ = []
        for arg in args:
            if isinstance(arg, dict):
                arg = copy.copy(arg)
                for k, v in arg.items():
                    if isinstance(v, dict):
                        arg[k] = frozendict(v)
                    elif isinstance(v, list):
                        v_ = list()
                        for elm in v:
                            if isinstance(elm, dict):
                                v_.append( frozendict(elm) )
                            else:
                                v_.append( elm )
                        arg[k] = tuple(v_)
                args_.append( arg )
            else:
                args_.append( arg )

        dict.__init__(new, *args_, **kw)
        return new



        # frozenargs=[]
        # for arg in args:
        # 	if isinstance(arg, dict):
        #         arg = copy.copy(arg)
        # 		for key, value in arg.items():
        # 			if isinstance(value, dict):
        # 				arg[key] = frozendict(value)
        # 			elif isinstance(value, list):
        # 				freezevalue = list()
        # 				for element in value:
        # 					if isinstance(element, dict):
        # 						freezevalue.append(frozendict(element))
        # 					else:
        # 						freezevalue.append(element)
        # 				arg[key] = tuple(freezevalue)
        # 		frozenargs.append(arg)
        # 	else:
        # 		frozenargs.append(arg)

        #dict.__init__(new, *args, **kw)
        #return new


        dict.__init__(new, *args, **kw)
        return new

    def __init__(self, *args, **kw):
        pass

    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            h = self._cached_hash = hash(tuple(sorted(self.items())))
            return h

    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)