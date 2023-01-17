# THIS FILE FUCUSES ON THE QUERYING OF THE DOCUMENTS USING HAYSTACK AND OPENAI API

import os
import openai

# for the funcion we will need a queying object that will be the pipeline for the retriever
# and the openai api key
# take the api key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_document(querying_object, query: str, k_results: int = 10) -> str:
    '''
    This function will query the documents using the pipeline for the retriever to
    out perform the GPT-3 model query.

    Parameters
    ----------
    querying_object : Pipeline
        The pipeline for the retriever.
    query : str
        The query to search in the documents.
        
    k_results : int, optional
        The number of documents to return. The default is 10.
        
    Returns
    -------
    str
    
    '''
    
    # the document object return by the retriever pipeline is a dictionary
    preliminary_results = querying_object.run(query=query, params={"top_k": k_results})
    
    raw_text = ''
    # lets iterate over the dictionary and get the text of the documents
    for i, pred in enumerate(preliminary_results['documents']):
        # print(str(i) + '. ' + pred.content)
        raw_text += str(i) + '. ' + pred.content + '\n'
        
    # we have to prepare the text for the openai api (prompt engeniering)
    prepared_text = f'''Base on the following documents, answer the following question:\n\n
                    {raw_text}\n
                    Question: {query} \n
                    Answer:'''
    
    # now we can query the openai api
    answers = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prepared_text,
        max_tokens=200,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    
    return answers.choices[0].text
        