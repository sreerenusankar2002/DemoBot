# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class ReportDetails:
    def __init__(
        self,
        reporttype: str = None,
        timeperiod: str = None,
        reportformat = None
    ):
        
        # if unsupported_airports is None:
        #     unsupported_airports = []
        self.reporttype = reporttype
        self.timeperiod = timeperiod
        self.reportformat = reportformat
