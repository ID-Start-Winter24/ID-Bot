import os
import time
import gradio as gr
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


path_modulhandbuch = "./modulhandbuch"
path_persist = os.path.join(path_modulhandbuch, "persist")

Settings.llm = OpenAI(temperature=0.1, model="gpt-4o-mini")

if not os.path.exists(path_persist):
    documents = SimpleDirectoryReader("./modulhandbuch/").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=path_persist)
else:
    storage_context = StorageContext.from_defaults(persist_dir=path_persist)
    index = load_index_from_storage(storage_context)


def response(message, history):
    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(message)

    answer = ""
    for text in streaming_response.response_gen:
        time.sleep(0.05)
        answer += text
        yield answer


def main():
    chatbot = gr.ChatInterface(
        fn=response,
        retry_btn=None,
        undo_btn=None,
    )

    chatbot.launch(inbrowser=True)


if __name__ == "__main__":
    main()