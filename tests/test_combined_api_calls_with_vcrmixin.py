import unittest
import openai
import google.generativeai as genai
from scope3ai.lib import Scope3AI
from vcr_unittest import VCRMixin  # Import VCRMixin

# Initialize API keys (replace with actual keys for the first run to generate cassettes)
openai.api_key = "your-openai-api-key"
genai.configure(api_key="your-google-api-key")


def fetch_combined_responses(initial_prompt):
    """Fetches a refined prompt from OpenAI and uses it to query Google's Generative AI."""
    openai_response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": initial_prompt}]
    )
    refined_prompt = openai_response["choices"][0]["message"]["content"]

    google_response = genai.generate_text(prompt=refined_prompt)
    return refined_prompt, google_response.candidates[0]["output"]


class TestCombinedAPICallsWithVCR(VCRMixin, unittest.TestCase):
    """Unit tests for combined OpenAI and Google Generative AI calls using VCRMixin."""

    def test_scope3_api(self):
        """Test Scope3AI integration along with nested OpenAI and Google API calls."""
        initial_prompt = "Explain why using AI for software development is beneficial."

        # Initialize Scope3AI session
        scope3 = Scope3AI.init(enable_debug_logging=True)
        with scope3.group(id="1", tag="session") as session:
            # Call the combined API function
            refined_prompt, google_response = fetch_combined_responses(initial_prompt)

            # Assertions for OpenAI and Google responses
            self.assertEqual(refined_prompt, "cassete response for OpenAi")
            self.assertEqual(google_response, "cassete response for Google")

            # Mocked response for Scope3AI impact
            impact = session.impact()  # Ensure .impact() returns a mocked value
            self.assertEqual(impact, 0.32)  # Expected value from cassette


if __name__ == "__main__":
    unittest.main()
