
import random
import sys
from mitmproxy import io, http
from mitmproxy import ctx
import typing  # noqa

class CspScannerAddon:
    def __init__(self):
        self.w = None

    # def load(self, loader):
    #     ctx.log.info("Registering option 'csp_reports_file'")
    #     loader.add_option( 
    #         "csp_reports_file", 
    #         str, 
    #         "", 
    #         "A file where the CSP report will be saved")

    # def configure(self, updated: typing.Set[str]):
    #     if "csp_reports_file" in updated:
    #         if self.f:
    #             self.f.close()
 
    #         if ctx.options.csp_reports_file:
    #             self.f: typing.IO[bytes] = open(ctx.options.csp_reports_file, "wb")
    #             self.w = io.FlowWriter(self.f)

    #         ctx.log.info("csp_reports_file value: %s" % ctx.options.csp_reports_file)

    def request(self, flow:http.HTTPFlow):
        if flow.request.path == "/cspscannerreport":
            flow.response = http.HTTPResponse.make(200)


    def response(self, flow: http.HTTPFlow) -> None:
        flow.response.headers["Content-Security-Policy-Report-Only"] = \
            "script-src 'none'; style-src 'none'; img-src 'none'; connect-src 'none'; font-src 'none'; object-src 'none'; media-src 'none'; frame-src 'none'; child-src 'none'; frame-ancestors 'none'; default-src 'none'; report-uri /cspscannerreport"

    def done(self):
        self.f.close()

addons = [
    CspScannerAddon()
]