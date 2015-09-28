import os

from qubell.api.testing import *

@environment({
    "default": {}
})
class LogstashComponentTestCase(BaseComponentTestCase):
    name = "component-logstash"
    apps = [{
        "name": name,
        "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name))
    }]
    @classmethod
    def timeout(cls):
        return 60

    @instance(byApplication=name)
    def test_logstash_url(self, instance):
        import requests    
        url  = instance.returnValues['logger.kibana-dashboard']
        resp = requests.get(url, verify=False)
        assert resp.status_code == 200
