from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router import SemanticRouter

encoder = HuggingFaceEncoder(model_name="sentence-transformers/all-MiniLM-L6-v2")

faq = Route(
    name="faq",
    utterances=[
        "what is the return policy of the products?",
        "Do i get discount with the HDFC credit card?",
        "How do I track my order?",
        "What payment methods are accepted?",
        "How lo does it take to process a refund?",
        "Can I return an item?",
        "How do I get my money back?",
        "What's your refund policy?",
        "Where is my package?",
        "How to check delivery status?",
        "Are there any special offers?",
        "Payment options available?",
        "How long for a refund?",
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs.3000?",
        "Do you have formal shoes in size 9?",
        "Are thre any Puma shoes on sale?",
        "What is the price of the Puma running shoes?",
        "Show me cheap shoes.",
        "Find shoes with high ratings.",
        "List all products by Adidas.",
        "What's the best selling shoe?",
        "Shoes under 1000 rupees.",
        "Products with more than 20% discount.",
    ]
)

routes = [faq, sql]
router = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")

# Explicitly add routes to the router.
router.add(routes) 

if __name__ == "__main__":
    test_queries = [
        "What is the return policy of the products?",
        "Pink Puma shoes in price range of 5000 to 1000",
        "Show me Nike shoes under Rs. 3000",
        "How can I track my order?",
        "Can I return this?", 
        "Are there any discounts?", 
    ]

    for query in test_queries:
        result = router(query)
        print(
            f"Query: '{query}' -> Route: {result.name if result else 'No route found'}"
        )
