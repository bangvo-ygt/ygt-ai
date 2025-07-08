from dotenv import load_dotenv

load_dotenv()
# ruff: noqa: E402

from typing import Optional

from google.api_core.client_options import ClientOptions
# from google.cloud import documentai
from google.cloud import documentai_v1beta3 as documentai
from google.cloud.documentai_v1beta3.services.document_service import pagers


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    with open(file_path, "rb") as file:
        file_content = file.read()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=file_content, mime_type=mime_type),
        process_options=process_options,
    )

    result = client.process_document(request=request)

    return result.document


def get_document(
    project_id: str, location: str, processor: str, doc_id: documentai.DocumentId
) -> documentai.GetDocumentResponse:
    """It will fetch data for individual sample/document present in dataset

    Args:
        project_id (str): Project ID
        location (str): Processor Location
        processor (str): Document AI Processor ID
        doc_id (documentai.DocumentId): Document identifier

    Returns:
        documentai.GetDocumentResponse: Returns data related to doc_id
    """

    client = documentai.DocumentServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )
    dataset = (
        f"projects/{project_id}/locations/{location}/processors/{processor}/dataset"
    )
    request = documentai.GetDocumentRequest(dataset=dataset, document_id=doc_id)
    operation = client.get_document(request)
    return operation


def list_documents(
    project_id: str,
    location: str,
    processor: str,
    page_size: Optional[int] = 100,
    page_token: Optional[str] = "",
) -> pagers.ListDocumentsPager:
    """This function helps to list the samples present in processor dataset

    Args:
        project_id (str): Project ID
        location (str): Processor Location
        processor (str): DocumentAI Processor ID
        page_size (Optional[int], optional): The maximum number of documents to return. Defaults to 100.
        page_token (Optional[str], optional): A page token, received from a previous ListDocuments call. Defaults to "".

    Returns:
        pagers.ListDocumentsPager: Returns all details about documents present in Processor Dataset
    """
    client = documentai.DocumentServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )
    dataset = (
        f"projects/{project_id}/locations/{location}/processors/{processor}/dataset"
    )
    request = documentai.types.ListDocumentsRequest(
        dataset=dataset,
        page_token=page_token,
        page_size=page_size,
        return_total_size=True,
    )
    operation = client.list_documents(request)
    return operation


def get_dataset_schema(
    project_id: str, processor_id: str, location: str
) -> documentai.DatasetSchema:
    """It helps to fetch processor schema

    Args:
        project_id (str): Project ID
        processor_id (str): DocumentAI Processor ID
        location (str): Processor Location

    Returns:
        documentai.DatasetSchema: Return deails about Processor Dataset Schema
    """

    # Create a client
    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )
    client = documentai.DocumentServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )
    request = documentai.GetDatasetSchemaRequest(
        name=processor_name + "/dataset/datasetSchema"
    )
    # Make the request
    response = client.get_dataset_schema(request=request)
    return response


if __name__ == "__main__":
    project_id = "staging-servers-157416"
    location = "eu"
    processor_id = "cf1645a6dce688ee"
    processor_version = "rc"
    file_path = "./YGT Cost/YGT Sample Invoices/BF0003944130.pdf"
    mime_type = "application/pdf"

    res = process_document(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
        file_path=file_path,
        mime_type=mime_type,
    )
