# This file is kept around for the commented lines which contain an example of saving flows. 

import random
import sys
from mitmproxy import io, http
from mitmproxy import ctx
import typing  # noqa

class CspScannerAddon:
    # def __init__(self):
    #     self.w = None

    def load(self, loader):
        ctx.log.info("Registering option 'generate_csp_reports'")
        loader.add_option( 
            name = "generate_csp_reports", 
            typespec = bool, 
            default = True, 
            help = "Add csp-report-only header and respond to report flows")

    # def configure(self, updated: typing.Set[str]):
    #     if "csp_reports_file" in updated:
    #         if self.f:
    #             self.f.close()
 
    #         if ctx.options.csp_reports_file:
    #             self.f: typing.IO[bytes] = open(ctx.options.csp_reports_file, "wb")
    #             self.w = io.FlowWriter(self.f)

    #         ctx.log.info("csp_reports_file value: %s" % ctx.options.csp_reports_file)

    def request(self, flow:http.HTTPFlow):
        if ctx.options.generate_csp_reports and flow.request.path == "/cspscannerreport":
            flow.response = http.HTTPResponse.make(200)


    def response(self, flow: http.HTTPFlow) -> None:
        if ctx.options.generate_csp_reports:
            flow.response.headers["Content-Security-Policy-Report-Only"] = \
                "script-src 'none'; style-src 'none'; img-src 'none'; connect-src 'none'; font-src 'none'; object-src 'none'; media-src 'none'; frame-src 'none'; child-src 'none'; frame-ancestors 'none'; default-src 'none'; report-uri /cspscannerreport"

    # def done(self):
    #     self.f.close()

addons = [
    CspScannerAddon()
]