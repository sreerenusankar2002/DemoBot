# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class ReportDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(ReportDialog, self).__init__(dialog_id or ReportDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.reporttype_step,
                    self.timeperiod_type,
                    self.reportformat_type,
                    self.confirm_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def reporttype_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        report_details = step_context.options

        if report_details.reporttype is None:
            message_text = "For which report you like to get the results?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(report_details.reporttype)
    
    async def timeperiod_type(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If a error code has not been given, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        report_details = step_context.options
        report_details.reporttype = step_context.result

        if report_details.timeperiod is None:
            message_text = "For which timeperiod you want this report?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(report_details.timeperiod)
    
    async def reportformat_type(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If a error code has not been given, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        report_details = step_context.options
        report_details.timeperiod = step_context.result

        if report_details.reportformat is None:
            message_text = "In which format do you want this report?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(report_details.reportformat)
    
    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        report_details = step_context.options

        # Capture the results of the previous step
        report_details.reportformat = step_context.result
        message_text = (
            f"Please confirm, you want { report_details.reporttype } for a { report_details.timeperiod } in { report_details.reportformat} format"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            report_details = step_context.options

            return await step_context.end_dialog(report_details)
        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
