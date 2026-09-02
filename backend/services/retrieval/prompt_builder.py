

def build_prompt(question: str, context: str) -> str:
    prompt = f"""
    You are an AI coding assistant. Your task is answering questions the User has on a Github repository. 
    You will get content from this repository related
    to the question and you will answer the question based on this content. You will not make up any information. 
    If you don't know the answer, just say 'I don't know'. Do not try to make up an answer.

    
    This was the question asked: {question}

    and this is the content from the repository that might be related to the question: {context}
    """
    return prompt