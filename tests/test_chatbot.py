import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from chatbot import FAQChatbot


def test_pricing_question():

    bot = FAQChatbot()

    result = bot.get_response(
        "How much does Nexora cost?"
    )

    assert result["category"] == "Pricing"
    assert result["intent"] == "pricing_plans"
    assert result["status"] == "matched"


def test_billing_question():

    bot = FAQChatbot()

    result = bot.get_response(
        "Can I change my card details?"
    )

    assert result["category"] == "Billing"
    assert result["intent"] == "update_payment"


def test_suspicious_account_activity():

    bot = FAQChatbot()

    result = bot.get_response(
        "Someone may have accessed my account"
    )

    assert result["category"] == "Security"
    assert result["intent"] == "suspicious_activity"
    assert result["status"] == "intent"


def test_login_problem():

    bot = FAQChatbot()

    result = bot.get_response(
        "I can't sign in to my account"
    )

    assert result["category"] == "Troubleshooting"
    assert result["intent"] == "login_problem"


def test_integration_question():

    bot = FAQChatbot()

    result = bot.get_response(
        "Can Nexora connect with another software?"
    )

    assert result["category"] == "Integrations"
    assert result["intent"] == "connect_application"


def test_payment_failure():

    bot = FAQChatbot()

    result = bot.get_response(
        "What happens if my payment gets declined?"
    )

    assert result["category"] == "Billing"
    assert result["intent"] == "payment_failed"


def test_password_reset():

    bot = FAQChatbot()

    result = bot.get_response(
        "I forgot my password"
    )

    assert result["category"] == "Account"
    assert result["intent"] == "password_reset"


def test_security_question():

    bot = FAQChatbot()

    result = bot.get_response(
        "How do I protect my account?"
    )

    assert result["category"] == "Security"


def test_empty_question():

    bot = FAQChatbot()

    result = bot.get_response("")

    assert result["status"] == "empty"


def test_unknown_question():

    bot = FAQChatbot()

    result = bot.get_response(
        "What is the capital of France?"
    )

    assert result["status"] == "fallback"


def test_unrelated_question():

    bot = FAQChatbot()

    result = bot.get_response(
        "Tell me something completely unrelated to Nexora"
    )

    assert result["status"] == "fallback"


def test_categories():

    bot = FAQChatbot()

    categories = bot.get_categories()

    assert len(categories) == 12
    assert "Pricing" in categories
    assert "Security" in categories
    assert "Billing" in categories
    assert "Support" in categories