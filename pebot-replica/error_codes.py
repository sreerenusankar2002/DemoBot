# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class SearchDetails:
    def __init__(
        self,
        application: str = None,
        unsupported_airports = None
    ):
        
        if unsupported_airports is None:
            unsupported_airports = []
        self.unsupported_airports = unsupported_airports
        self.application = application
