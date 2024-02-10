from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = conversation({'question': user_question})
    chat_history = response['chat_history'][::-1]  # Reverse the chat history
    output = []
    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            print(message.content)

    return output

# Example array of conversations
conversation_array = [
    "Karan: Hi, how are you?\nAryan: I'm good, thanks!",
    "Karan: What's your favorite movie?\nAryan: I love 'Inception.'",
    "Karan: Have you been on any vacations lately?\nAryan: Yes, I went to the beach last month.",
    "Karan: That sounds fantastic! What beach did you visit?\nAryan: I went to Malibu Beach. The scenery was breathtaking!",
    "Karan: Malibu is beautiful! Did you try any water sports?\nAryan: I tried surfing for the first time. It was challenging but so much fun!",
    "Karan: Impressive! I've always wanted to learn surfing. Any tips for beginners?\nAryan: Patience is key and don't be afraid to wipeout. It's part of the learning process.",
    "Karan: Thanks for the advice. By the way, have you seen any good movies lately?\nAryan: Yes, I watched 'The Shawshank Redemption.' It's a classic and highly recommended.",
    "Karan: I love that movie! The plot is incredible. What other classics do you enjoy?\nAryan: 'The Godfather' trilogy is another favorite of mine. The storytelling is exceptional.",
    "Karan: Great choices! Speaking of storytelling, do you enjoy reading books?\nAryan: Absolutely! I'm currently reading 'To Kill a Mockingbird.' It's a timeless novel with a powerful message.",
    "Karan: 'To Kill a Mockingbird' is a masterpiece. Harper Lee did an amazing job. Do you have any other book recommendations?\nAryan: '1984' by George Orwell is a thought-provoking dystopian novel that I highly recommend.",
    "Karan: I've heard a lot about '1984.' It's on my reading list. Shifting gears, do you have any favorite hobbies?\nAryan: I enjoy photography. Capturing moments and creating memories is truly fulfilling for me.",
    "Karan: That's awesome! Photography is a wonderful way to express creativity. Have you exhibited your work anywhere?\nAryan: I've participated in a few local exhibitions. It's a great way to connect with other artists and receive feedback.",
    "Karan: Connecting with the artistic community is important. Do you have any upcoming projects?\nAryan: I'm working on a series of nature photographs to highlight environmental conservation. It's a cause close to my heart.",
    # Add more conversations as needed
]

text = "\n".join(conversation_array)
text_chunks = get_text_chunks(text)
vectorstore = get_vectorstore(text_chunks)
conversation = get_conversation_chain(vectorstore)

user_question = input("Ask a question about your documents:")
if user_question:
    output = handle_userinput(user_question)
    for message in output:
        print(message)