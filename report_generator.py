#Previous code:

# import io
# import pandas as pd
# from azure.search.documents import SearchClient
# from azure.core.credentials import AzureKeyCredential
# from botbuilder.core import TurnContext, ActivityHandler
# from botbuilder.schema import Attachment, AttachmentData
# from botbuilder.core import MessageFactory
# import base64




# class ReportBot:
#     async def CreateReport(turn_context: TurnContext,search_results):
        
#         # Assuming intent and entities extraction happens here
       
#             tabular_text, df = generate_tabular_response(search_results)
#             # Send tabular data as a message
#             await turn_context.send_activity(f"Here is the report:\n'''\n{tabular_text}\n'''")

#             # Generate Excel and send as an attachment
#             excel_data = create_excel(df)
#             #excel_data = create_excel(search_results)
#             attachment = create_excel_attachment(excel_data)
#             message = MessageFactory.attachment(attachment)
#             await turn_context.send_activity(message)
            
   
        
# def create_excel_attachment(excel_data, filename="report.xlsx"):
#     base64_excel = base64.b64encode(excel_data.getvalue()).decode("utf-8")
    
#     attachment = Attachment(
#         name=filename,
#         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         content_url="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64," + base64_excel
#     )
#     return attachment
# def create_excel(df):
#     output = io.BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df.to_excel(writer, index=False)
#     output.seek(0)
#     return output
# def generate_tabular_response(search_results):
#     # Convert search results to a DataFrame
#     data = []
#     for result in search_results:
#         data.append(result)

#     df = pd.DataFrame(data)

#     # Generate a simple text table (for display in the chat)
#     tabular_text = df.to_string(index=False)
    
#     return tabular_text, df


#--------------------------------------------------------------------
#code for generating pdf


# import io
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# import base64
# from fpdf import FPDF
# from botbuilder.core import TurnContext, MessageFactory
# from botbuilder.schema import Attachment

# class ReportBot:
#     @staticmethod
#     async def CreateReport(turn_context: TurnContext, search_results):
#         tabular_text, df = generate_tabular_response(search_results)

#         # Send tabular data as a message
#         await turn_context.send_activity(f"Here is the report summary:\n'''\n{tabular_text}\n'''")

#         # Generate PDF and send as an attachment
#         pdf_data = create_pdf_report(df)
#         attachment = create_pdf_attachment(pdf_data)
#         message = MessageFactory.attachment(attachment)
#         await turn_context.send_activity(message)

# def create_pdf_attachment(pdf_data, filename="report.pdf"):
#     base64_pdf = base64.b64encode(pdf_data.getvalue()).decode("utf-8")
    
#     attachment = Attachment(
#         name=filename,
#         content_type="application/pdf",
#         content_url="data:application/pdf;base64," + base64_pdf
#     )
#     return attachment

# def create_pdf_report(df):
#     output = io.BytesIO()

#     # Create a PDF document
#     with PdfPages(output) as pdf:
#         # Page 1: Add a DataFrame summary
#         plt.figure(figsize=(12, 6))
#         plt.axis('off')
#         summary_table = plt.table(cellText=df.head().values, colLabels=df.columns, cellLoc='center', loc='center')
#         summary_table.auto_set_font_size(False)
#         summary_table.set_fontsize(8)  # Adjust font size for better readability
#         summary_table.scale(1.2, 1.2)
#         plt.title('DataFrame Summary (First 5 Rows)', fontsize=14)
#         pdf.savefig()
#         plt.close()

#         # Additional Pages: Plot each numeric column
#         numeric_cols = df.select_dtypes(include='number').columns
#         for col in numeric_cols:
#             plt.figure(figsize=(10, 6))
#             df[col].plot(kind='bar', title=f'Distribution of {col}')
#             plt.tight_layout()
#             pdf.savefig()
#             plt.close()

#     output.seek(0)
#     return output

# def generate_tabular_response(search_results):
#     # Convert search results to a DataFrame
#     df = pd.DataFrame(search_results)

#     # Generate a simple text table (for display in the chat)
#     tabular_text = df.to_string(index=False)
    
#     return tabular_text, df


#code for generating excel correct format
# import io
# import pandas as pd
# import base64
# from botbuilder.core import TurnContext, MessageFactory
# from botbuilder.schema import Attachment

# class ReportBot:
#     @staticmethod
#     async def CreateReport(turn_context: TurnContext, search_results):
#         tabular_text, df = generate_tabular_response(search_results)

#         # Send tabular data as a message
#         await turn_context.send_activity(f"Here is the report summary:\n'''\n{tabular_text}\n'''")

#         # Generate Excel and send as an attachment
#         excel_data = create_excel_report(df)
#         attachment = create_excel_attachment(excel_data)
#         message = MessageFactory.attachment(attachment)
#         await turn_context.send_activity(message)

# def create_excel_report(df):
#     output = io.BytesIO()

#     # Select the first 5 rows of the DataFrame
#     df_summary = df.head()

#     # Save the DataFrame summary to an Excel file
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df_summary.to_excel(writer, index=False, sheet_name='Summary')
    
#     output.seek(0)
#     return output

# def create_excel_attachment(excel_data, filename="report.xlsx"):
#     base64_excel = base64.b64encode(excel_data.getvalue()).decode("utf-8")
    
#     attachment = Attachment(
#         name=filename,
#         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         content_url="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64," + base64_excel
#     )
#     return attachment

# def generate_tabular_response(search_results):
#     # Convert search results to a DataFrame
#     df = pd.DataFrame(search_results)

#     # Generate a simple text table (for display in the chat)
#     tabular_text = df.to_string(index=False)
    
#     return tabular_text, df




#-----------------------------------------------------------------
# code for new pdf generator
from fpdf import FPDF
import pandas as pd
import base64
import io
from botbuilder.core import TurnContext, MessageFactory
from botbuilder.schema import Attachment

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Generated Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Generated by ReportBot', 0, 1, 'C')
        self.ln(10)

    def add_table(self, data, col_widths=None):
        # Table headers
        self.set_font('Arial', 'B', 12)
        for header in data.columns:
            self.cell(col_widths[header], 10, header, border=1, align='C')
        self.ln()

        # Table rows
        self.set_font('Arial', '', 10)
        for _, row in data.iterrows():
            max_row_height = 10  # Start with a base height
            line_counts = []
            for item, header in zip(row, data.columns):
                text = str(item)
                lines = self.get_lines_for_text(text, col_widths[header])
                max_row_height = max(max_row_height, lines * 10)
                line_counts.append(lines)

            for count, (item, header) in enumerate(zip(row, data.columns)):
                x_before = self.get_x()
                y_before = self.get_y()
                self.multi_cell(col_widths[header], max_row_height / line_counts[count], str(item), border=1, align='C')
                self.set_xy(x_before + col_widths[header], y_before)

            self.ln(max_row_height)

    def get_lines_for_text(self, text, col_width):
        # Calculate the number of lines needed for the given column width
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if self.get_string_width(current_line + word + " ") > col_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line += word + " "
        lines.append(current_line)  # Add the last line
        return len(lines)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


def create_pdf_report(dataframe):
    pdf = PDFReport()
    pdf.add_page()

    # Adding title and introduction
    pdf.chapter_title("Summary")
    pdf.chapter_body("This report contains an analysis based on GPT response.")

    # Calculate column widths dynamically
    max_width = pdf.w - 20  # Page width minus margins
    min_col_width = 30
    col_widths = {}
    
    for col in dataframe.columns:
        max_text_width = max(pdf.get_string_width(str(item)) for item in dataframe[col])
        col_width = min(max(max_text_width + 10, min_col_width), max_width / len(dataframe.columns))
        col_widths[col] = col_width

    # Adding table
    pdf.add_table(dataframe, col_widths=col_widths)

    # Saving PDF to a byte stream
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return pdf_output

class ReportBot:
    @staticmethod
    async def CreateReport(turn_context: TurnContext, gpt_response):
        # Parse the GPT response into a structured format
        structured_response = parse_gpt_response(gpt_response)
        
        # Convert the structured response to a DataFrame
        df = pd.DataFrame(structured_response)

        # Generate PDF and send as an attachment
        pdf_data = create_pdf_report(df)
        attachment = create_pdf_attachment(pdf_data)
        message = MessageFactory.attachment(attachment)
        await turn_context.send_activity(message)

def create_pdf_attachment(pdf_data, filename="report.pdf"):
    base64_pdf = base64.b64encode(pdf_data.getvalue()).decode("utf-8")
    
    attachment = Attachment(
        name=filename,
        content_type="application/pdf",
        content_url="data:application/pdf;base64," + base64_pdf
    )
    return attachment

def parse_gpt_response(gpt_response):
    """
    Parses a GPT response that contains key-value pairs into a structured format.
    Modify this function based on the actual structure of the GPT response.
    :param gpt_response: str - The GPT response string.
    :return: list of dict - Structured data that can be converted into a DataFrame.
    """
    lines = gpt_response.strip().split('\n')
    
    response_dict = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            response_dict[key.strip()] = value.strip()
    
    return [response_dict]
