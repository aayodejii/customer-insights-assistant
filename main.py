import gradio as gr
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Initialize the model
model = OllamaLLM(model="llama3.2")

# Define the template
template = """
You are a helpful assistant analyzing customer reviews for TaskFlow Pro, a project management SaaS tool.

Here are some relevant customer reviews: {reviews}

Here is the question to answer: {question}

Provide a clear and helpful answer based on what customers are saying in the reviews. 
If relevant, mention specific details like ratings, user roles, or company sizes.
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def answer_question(question, history):
    """
    Process the user's question and return an answer.

    Args:
        question: The user's question
        history: Chat history (for Gradio ChatInterface)

    Returns:
        The model's response
    """
    if not question.strip():
        return "Please ask a question about TaskFlow Pro."

    try:
        # Retrieve relevant reviews
        reviews = retriever.invoke(question)

        # Generate answer
        result = chain.invoke({"reviews": reviews, "question": question})

        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Create the Gradio interface
demo = gr.ChatInterface(
    fn=answer_question,
    title="Customer Support Assistant",
    description="Ask me anything about the product. I'll search through customer reviews to help answer your questions about features, pricing, support, and more.",
    examples=[
        "What do customers say about the pricing?",
        "How is the customer support rated?",
        "What integrations do users mention?",
        "Are there complaints about the mobile app?",
        "What do enterprise customers think?",
        "How easy is the onboarding process?",
        "What features do Project Managers like most?",
    ],
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
