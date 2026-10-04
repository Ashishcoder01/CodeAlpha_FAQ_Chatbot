from chatbot import FAQChatbot


bot = FAQChatbot(threshold=0.25)


test_questions = [
    "How much does Nexora cost?",
    "Can I change my card details?",
    "Someone may have accessed my account",
    "I can't sign in to my account",
    "Can Nexora connect with another software?",
    "What happens if my payment gets declined?",
    "I forgot my password",
    "How do I protect my account?",
    "What is the capital of France?",
    "Tell me something completely unrelated to Nexora"
]


print("\n" + "=" * 70)
print("NEXORA AI - NLP MATCHING TEST")
print("=" * 70)


for number, question in enumerate(test_questions, start=1):

    result = bot.get_response(question)

    print(f"\nTest {number}")
    print("-" * 70)

    print(f"Question       : {question}")
    print(f"Status         : {result['status']}")
    print(f"Confidence     : {result['score']:.2%}")
    print(f"Matched FAQ    : {result['matched_question']}")
    print(f"Category       : {result['category']}")
    print(f"Intent         : {result['intent']}")

    print(f"Answer         : {result['answer']}")


print("\n" + "=" * 70)
print("TEST COMPLETED")
print("=" * 70)