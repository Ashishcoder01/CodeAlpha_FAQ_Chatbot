import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text


class FAQChatbot:

    def __init__(self, faq_file="data/faqs.json", threshold=0.35):

        self.threshold = threshold

        with open(faq_file, "r", encoding="utf-8") as file:
            self.faqs = json.load(file)

        self.search_items = []

        for faq_index, faq in enumerate(self.faqs):

            questions = [faq["question"]]
            questions.extend(faq.get("variations", []))

            for question in questions:

                self.search_items.append({
                    "faq_index": faq_index,
                    "question": question,
                    "processed": preprocess_text(question)
                })

        self.search_texts = [
            item["processed"]
            for item in self.search_items
        ]

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        self.question_vectors = self.vectorizer.fit_transform(
            self.search_texts
        )

    def get_categories(self):

        return sorted(
            set(
                faq["category"]
                for faq in self.faqs
            )
        )

    def get_faqs_by_category(self, category):

        return [
            faq
            for faq in self.faqs
            if faq["category"] == category
        ]

    def _build_result(
        self,
        faq,
        score,
        matched_question,
        status
    ):

        return {
            "answer": faq["answer"],
            "score": float(score),
            "matched_question": matched_question,
            "category": faq["category"],
            "intent": faq["intent"],
            "related_questions": faq.get(
                "related_questions",
                []
            ),
            "status": status
        }

    def _fallback_response(self, score=0.0):

        return {
            "answer": (
                "I couldn't find a reliable answer "
                "for that question. Try asking about "
                "pricing, accounts, security, billing, "
                "products, support, or enterprise features."
            ),
            "score": float(score),
            "matched_question": None,
            "category": None,
            "intent": None,
            "related_questions": [
                "What pricing plans are available?",
                "How do I create an account?",
                "Is my data secure?",
                "How can I contact support?"
            ],
            "status": "fallback"
        }

    def _detect_priority_intent(self, question):

        text = question.lower()

        security_patterns = [
            r"\baccessed\b",
            r"\bcompromised\b",
            r"\bhacked\b",
            r"\bsuspicious\b",
            r"\bunauthorized\b",
            r"\bunusual activity\b",
            r"\bsomeone logged\b",
            r"\bsomeone accessed\b",
            r"\bsomeone got into\b"
        ]

        login_patterns = [
            r"\bcan't sign in\b",
            r"\bcannot sign in\b",
            r"\bcan't login\b",
            r"\bcannot login\b",
            r"\bcan't log in\b",
            r"\bcannot log in\b",
            r"\blogin is not working\b",
            r"\bunable to log in\b",
            r"\bunable to login\b",
            r"\bcan't access my account\b",
            r"\bcannot access my account\b"
        ]

        password_patterns = [
            r"\bforgot my password\b",
            r"\bforgot password\b",
            r"\breset my password\b",
            r"\bchange my password\b",
            r"\bpassword reset\b"
        ]

        billing_patterns = [
            r"\bpayment\b",
            r"\bcard\b",
            r"\bbilling\b",
            r"\binvoice\b",
            r"\bsubscription\b"
        ]

        pricing_patterns = [
            r"\bprice\b",
            r"\bpricing\b",
            r"\bcost\b",
            r"\bplans?\b",
            r"\bsubscription price\b"
        ]

        if any(
            re.search(pattern, text)
            for pattern in security_patterns
        ):
            return "suspicious_activity"

        if any(
            re.search(pattern, text)
            for pattern in login_patterns
        ):
            return "login_problem"

        if any(
            re.search(pattern, text)
            for pattern in password_patterns
        ):
            return "password_reset"

        if any(
            re.search(pattern, text)
            for pattern in billing_patterns
        ):
            return "billing"

        if any(
            re.search(pattern, text)
            for pattern in pricing_patterns
        ):
            return "pricing"

        return None

    def _find_intent_faq(self, intent):

        for faq in self.faqs:

            if faq.get("intent") == intent:
                return faq

        return None

    def get_response(self, user_question):

        processed_question = preprocess_text(
            user_question
        )

        if not processed_question.strip():

            return {
                "answer": "Please enter a question.",
                "score": 0.0,
                "matched_question": None,
                "category": None,
                "intent": None,
                "related_questions": [],
                "status": "empty"
            }

        detected_intent = self._detect_priority_intent(
            user_question
        )

        if detected_intent:

            priority_faq = self._find_intent_faq(
                detected_intent
            )

            if priority_faq:

                user_words = set(
                    processed_question.split()
                )

                faq_text = " ".join([
                    priority_faq["question"],
                    *priority_faq.get(
                        "variations",
                        []
                    ),
                    *priority_faq.get(
                        "keywords",
                        []
                    )
                ])

                faq_words = set(
                    preprocess_text(
                        faq_text
                    ).split()
                )

                overlap = (
                    len(user_words & faq_words)
                    / max(len(user_words), 1)
                )

                if overlap >= 0.20:

                    return self._build_result(
                        faq=priority_faq,
                        score=max(0.90, overlap),
                        matched_question=priority_faq[
                            "question"
                        ],
                        status="intent"
                    )

        for item in self.search_items:

            if processed_question == item["processed"]:

                faq = self.faqs[
                    item["faq_index"]
                ]

                return self._build_result(
                    faq=faq,
                    score=1.0,
                    matched_question=faq[
                        "question"
                    ],
                    status="exact"
                )

        user_vector = self.vectorizer.transform(
            [processed_question]
        )

        similarities = cosine_similarity(
            user_vector,
            self.question_vectors
        )[0]

        ranked_indices = similarities.argsort()[::-1]

        best_index = ranked_indices[0]

        best_score = float(
            similarities[best_index]
        )

        faq_index = self.search_items[
            best_index
        ]["faq_index"]

        faq = self.faqs[faq_index]

        matched_text = self.search_items[
            best_index
        ]["processed"]

        user_tokens = set(
            processed_question.split()
        )

        matched_tokens = set(
            matched_text.split()
        )

        common_tokens = (
            user_tokens & matched_tokens
        )

        overlap_ratio = (
            len(common_tokens)
            / max(len(user_tokens), 1)
        )

        if best_score < 0.50:

            return self._fallback_response(
                score=best_score
            )

        if (
            best_score < self.threshold
            or (
                best_score < 0.60
                and overlap_ratio < 0.40
            )
        ):

            return self._fallback_response(
                score=best_score
            )

        return self._build_result(
            faq=faq,
            score=best_score,
            matched_question=faq["question"],
            status="matched"
        )