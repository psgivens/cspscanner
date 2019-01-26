
import random
import sys
from mitmproxy import io, http
from mitmproxy import ctx
import typing  # noqa

class CspScannerAddon:

    def load(self, loader):
        ctx.log.info("Registering option 'generate_csp_reports'")
        loader.add_option( 
            name = "csp_reports_policy", 
            typespec = typing.Optional[str], 
            default = "script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; font-src 'self'; object-src 'self'; media-src 'self'; frame-src 'self'; child-src 'self'; frame-ancestors 'self'; default-src 'self'; report-uri /cspscannerreport", 
            help = "Specify the content security policy")

        loader.add_option( 
            name = "csp_reports_allow_none", 
            typespec = bool, 
            default = False, 
            help = "Configure CSP to disallow all to get report for all things which need configured.")

    def request(self, flow:http.HTTPFlow):
        if flow.request.path == "/cspscannerreport":
            flow.response = http.HTTPResponse.make(200)

    def response(self, flow: http.HTTPFlow) -> None:
        if ctx.options.csp_reports_allow_none:
            flow.response.headers["Content-Security-Policy-Report-Only"] = \
                "script-src 'none'; style-src 'none'; img-src 'none'; connect-src 'none'; font-src 'none'; object-src 'none'; media-src 'none'; frame-src 'none'; child-src 'none'; frame-ancestors 'none'; default-src 'none'; report-uri /cspscannerreport"
        else: 
            flow.response.headers["Content-Security-Policy-Report-Only"] = \
                ctx.options.csp_reports_policy

addons = [
    CspScannerAddon()
]