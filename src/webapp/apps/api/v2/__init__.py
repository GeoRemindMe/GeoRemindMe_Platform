# coding=utf-8

import respite as respite_Views


old_views = respite_Views.Views
class monkey_Views(old_views):
    def _notfound(self, request):
       return self._render(
                           request = request,
                           status = 404
                           )
       
    def _forbidden(self, request):
        return self._render(
                           request = request,
                           status = 403
                           )
    
    def _badrequest(self, error):
        return self._render(
                           request = request,
                           context = {'error': error},
                           status = 406
                           )
respite_Views.Views = monkey_Views