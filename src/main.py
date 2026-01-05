"""
Marketing Slogan Generator - Main Application
==============================================
This module demonstrates how reusable prompt templates from the prompt library
connect to the OpenAI API to generate marketing content.

Key Concepts Demonstrated:
1. Variable injection into prompt templates
2. Clean separation of prompt logic from API integration
3. Professional API call structure with error handling
4. Practical usage patterns for prompt engineering
"""

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from prompt_library import (
    professional_slogan_prompt,
    creative_slogan_prompt,
    audience_focused_prompt
)

# Load environment variables from .env file
# This looks for .env in the project root (parent of src folder)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def generate_slogan(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Send a prompt to OpenAI's Chat Completion API and retrieve the response.

    This function demonstrates the critical connection between prompt engineering
    and API implementation. The carefully crafted prompt from our library is
    passed as the user message to the API.

    Args:
        prompt: The complete prompt string from our prompt library
        model: OpenAI model to use (default: gpt-3.5-turbo)

    Returns:
        Generated slogan text from the API

    Connection Point: This is where prompt engineering meets execution.
    The quality of the output directly depends on the prompt structure
    defined in our prompt library.
    """
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")

    # Check if API key is loaded
    if not api_key:
        return "ERROR: OPENAI_API_KEY not found. Please check your .env file is in the project root."

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        # Make API call with our engineered prompt
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional marketing expert who creates concise, impactful slogans."
                },
                {
                    "role": "user",
                    "content": prompt  # Our engineered prompt is injected here
                }
            ],
            temperature=0.8,  # Slightly creative but controlled
            max_tokens=300,   # Sufficient for 3 slogans and explanation
            top_p=0.9
        )

        # Extract and return the generated content
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating slogan: {str(e)}"


def demonstrate_prompt_usage():
    """
    Demonstration of the complete workflow: variable injection → prompt
    generation → API call → result output.

    This function shows how the system works end-to-end in a real scenario.
    """
    print("=" * 70)
    print("MARKETING SLOGAN GENERATOR - DEMONSTRATION")
    print("=" * 70)
    print()

    # Step 1: Define variables (these could come from user input, database, etc.)
    product_name = "EcoBottle Pro"
    target_audience = "environmentally conscious millennials"
    tone = "friendly"

    print("INPUT VARIABLES:")
    print(f"  Product: {product_name}")
    print(f"  Target Audience: {target_audience}")
    print(f"  Tone: {tone}")
    print()

    # Step 2: Generate prompts using variable injection
    print("=" * 70)
    print("DEMONSTRATION 1: PROFESSIONAL APPROACH")
    print("=" * 70)

    # Variables are dynamically injected into the prompt template
    professional_prompt = professional_slogan_prompt(
        product_name=product_name,
        target_audience=target_audience,
        tone=tone
    )

    print("\nGenerated Prompt (first 300 characters):")
    print(f"{professional_prompt[:300]}...\n")

    print("Sending to OpenAI API...")
    result_1 = generate_slogan(professional_prompt)
    print("\nAPI Response:")
    print(result_1)
    print()

    # Step 3: Demonstrate with different prompt style
    print("=" * 70)
    print("DEMONSTRATION 2: CREATIVE APPROACH")
    print("=" * 70)

    creative_prompt = creative_slogan_prompt(
        product_name=product_name,
        target_audience=target_audience,
        tone="bold"  # Different tone for variety
    )

    print("\nGenerated Prompt (first 300 characters):")
    print(f"{creative_prompt[:300]}...\n")

    print("Sending to OpenAI API...")
    result_2 = generate_slogan(creative_prompt)
    print("\nAPI Response:")
    print(result_2)
    print()

    # Step 4: Show audience-focused approach
    print("=" * 70)
    print("DEMONSTRATION 3: AUDIENCE-FOCUSED APPROACH")
    print("=" * 70)

    audience_prompt = audience_focused_prompt(
        product_name=product_name,
        target_audience=target_audience,
        tone=tone
    )

    print("\nGenerated Prompt (first 300 characters):")
    print(f"{audience_prompt[:300]}...\n")

    print("Sending to OpenAI API...")
    result_3 = generate_slogan(audience_prompt)
    print("\nAPI Response:")
    print(result_3)
    print()


def interactive_mode():
    """
    Interactive mode allowing users to input their own variables.

    This demonstrates the reusability of our prompt templates - the same
    templates work for any product, audience, or tone combination.
    """
    print("=" * 70)
    print("INTERACTIVE SLOGAN GENERATOR")
    print("=" * 70)
    print()

    # Collect user input
    product_name = input("Enter product name: ").strip()
    target_audience = input("Enter target audience: ").strip()

    print("\nAvailable tones: professional, friendly, bold, playful")
    tone = input("Enter desired tone: ").strip() or "professional"

    print("\nAvailable prompt styles:")
    print("  1. Professional (strategic and polished)")
    print("  2. Creative (bold and innovative)")
    print("  3. Audience-Focused (empathetic and relatable)")

    choice = input("\nSelect prompt style (1-3): ").strip()

    # Select appropriate prompt based on user choice
    if choice == "1":
        prompt = professional_slogan_prompt(product_name, target_audience, tone)
        style = "Professional"
    elif choice == "2":
        prompt = creative_slogan_prompt(product_name, target_audience, tone)
        style = "Creative"
    elif choice == "3":
        prompt = audience_focused_prompt(product_name, target_audience, tone)
        style = "Audience-Focused"
    else:
        print("Invalid choice. Using Professional style.")
        prompt = professional_slogan_prompt(product_name, target_audience, tone)
        style = "Professional"

    print(f"\n{'-' * 70}")
    print(f"GENERATING {style.upper()} SLOGANS...")
    print(f"{'-' * 70}\n")

    # Generate and display results
    result = generate_slogan(prompt)
    print(result)
    print()


if __name__ == "__main__":
    """
    Main execution block - demonstrates both automated and interactive modes.
    
    Comment/uncomment the desired mode for testing.
    """

    # Run automated demonstration
    demonstrate_prompt_usage()

    # Uncomment below for interactive mode
    # interactive_mode()

    print("=" * 70)
    print("ASSIGNMENT COMPLETE")
    print("=" * 70)