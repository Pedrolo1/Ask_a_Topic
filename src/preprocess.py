# THIS FILE WILL HAVE THE FUCTIONS RELATED TO THE PREPROCESSING OF THE TRANSCRIPTS USING HAYSTACK
# LETS START MAKING A PIPELINE TO PROCESS THE TRANSCRIPTS AND SELECT THE MAIN ONES

import os
from haystack.document_stores import InMemoryDocumentStore
from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor
from haystack.nodes import BM25Retriever


def pipeline_transcripts(path_transcripts: str):
    # create the document store
    document_store = InMemoryDocumentStore(use_bm25=True)
    
    # create the pipeline
    indexing_pipeline = Pipeline()
    
    # add the nodes to the pipeline
    text_converter = TextConverter()
    preprocessor = PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="word",
        split_length=200,
        split_overlap=20,
        split_respect_sentence_boundary=True,
    )
    
    # creation of the preprocessor pipeline
    indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
    indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
    indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])
    
    files_to_index = [path_transcripts + "/" + f for f in os.listdir(path_transcripts)]
    indexing_pipeline.run_batch(file_paths=files_to_index)
    
    # one time we have all documents in the document store we can create the retriever
    retriever = BM25Retriever(document_store=document_store)
    
    # create the pipeline only for the retriever
    querying_pipeline = Pipeline()
    querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    
    # return the pipeline for the retriever, and this could be used to query the documents
    # using querying_pipeline.run(query="what is the meaning of life?") # FOR EXAMPLE
    return querying_pipeline