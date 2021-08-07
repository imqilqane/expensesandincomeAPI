from rest_framework import renderers
import json
class UserRenserer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type, renderer_context):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps({'data':data})

        return response