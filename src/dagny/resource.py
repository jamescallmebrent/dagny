# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseNotAllowed
from djclsview import View

__all__ = ['Resource']


METHOD_ACTION_MAP = {
    'index': {
        'GET': 'index',
        'POST': 'create'
    },
    'show': {
        'GET': 'show',
        'POST': 'update',
        'PUT': 'update',
        'DELETE': 'destroy',
    },
    'new': {'GET': 'new'},
    'edit': {'GET': 'edit'},
}


class Resource(View):
    
    def __init__(self, request, *args, **params):
        self.request = request
        self.args = args
        self.params = params
    
    def __call__(self):
        """Dispatch to an action based on HTTP method + URL."""
        
        method = self.request.POST.get('method', self.request.method).upper()
        # The action to use if it were a GET request.
        get_action = self.params.pop('action')
        # The action to use for this particular request method.
        method_action = METHOD_ACTION_MAP[get_action][method]
        
        if hasattr(self, method_action):
            return getattr(self, method_action)()
        elif hasattr(self, get_action):
            allowed_methods = []
            for meth, action_name in METHOD_ACTION_MAP[get_action].items():
                if hasattr(self, action_name):
                    allowed_methods.append(meth)
            return HttpResponseNotAllowed(allowed_methods)
        else:
            raise Http404
    
    def _format(self):
        """Return a mimetype shortcode, in case there's no Accept header."""
        
        return self.request.GET.get('format')
