import gradio as gr
from src.querying import query_document
from src.preprocess import pipeline_transcripts
from argparse import ArgumentParser

# create the argument parser
parser = ArgumentParser(description="This script will run the gradio interface for the chatbot")
# query the pipeline for the retriever are of any type
parser.add_argument("--doc_files", help="path to the documents to index", required=True, type=str)
parser.add_argument("--num_results", help="number of results to return", required=True, default=10, type=int)
args = parser.parse_args()

querying_object = pipeline_transcripts(args.doc_files)

def gradio_interface(text, history):
    history = history or []
    reponse = query_document(querying_object = querying_object, query = text, k_results = args.num_results)
    history.append((text, reponse))
    return history, history

Chatbot = gr.Chatbot().style(color_map=("green", "black"))

interface2 = gr.Interface(gradio_interface,
                            inputs = ['text', 'state'],
                            outputs = [Chatbot, 'state'],
                            allow_flagging=False,
                            description = 'Ask the chatbot anything about the documents')

# launch the interface
interface2.launch(share = True)
