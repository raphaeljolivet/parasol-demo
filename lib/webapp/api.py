
from tornado.web import Application, RequestHandler, HTTPError
from tornado.routing import Rule, PathMatches
import gc
import streamlit as st

from lib.common import Model
from lib.settings import settings
from lib.webapp.utils import load_model


@st.cache_resource()
def setup_api_handler(uri, handler):
    print("Setup Tornado. Should be called only once")

    # Get instance of Tornado
    tornado_app = next(o for o in gc.get_referrers(Application) if o.__class__ is Application)

    # Setup custom handler
    tornado_app.wildcard_router.rules.insert(0, Rule(PathMatches(uri), handler))


# Setup API
class ComputeImpactHandler(RequestHandler):


    def get(self):

        model = load_model()

        method_name = self.get_mandatory_arg('method')

        if not method_name in model.impacts:
            raise HTTPError(status_code=400, reason=f"Bad method name {method_name} should be one of {list(model.impacts.keys())}")


        fu_name = self.get_mandatory_arg('functional_unit')
        if not fu_name in model.functional_units:
            raise HTTPError(status_code=400, reason=f"Bad function unit {fu_name} should be one of {list(model.functional_units.keys())}")


        # Optional axis
        axis = self.get_argument('axis', "total")
        if axis != "total":
            if not axis in settings.axes:
                raise HTTPError(status_code=400, reason=f"Bad axis {axis} should be one of {settings.axes}")

        params = self.fetch_parameters(model)

        value, unit = model.evaluate(
            impact=method_name,
            functional_unit=fu_name,
            axis=axis,
            **params)


        return self.write(dict(value=value, unit=unit))


    def fetch_parameters(self, model:Model):

        res = dict()

        for key in model.params :
            value = self.get_argument(key, None)
            if value is None:
                continue

            # Try to parse it as float
            try:
                value = float(value)
            except ValueError:
                value = str(value)

            res[key] = value
        return res





    def get_mandatory_arg(self, name):
        value = self.get_argument(name, None)
        if value is None or value.strip() == "":
            raise HTTPError(status_code=400, reason=f"Missing required query parameter: '{name}'")
        return value




def setup_api():
    setup_api_handler('/api/compute_impacts', ComputeImpactHandler)




