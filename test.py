import os
import dspy
from dspy_tot import TreeOfThought, create_text_generator, create_text_evaluator

# Configure DSPy with OpenRouter - works with any model!
model_id = os.getenv("MODEL_ID", "anthropic/claude-3.5-sonnet")
api_key = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key  # DSPy compatibility

lm = dspy.LM(
    model_id,
    max_tokens=8000,
    temperature=0.7,
    api_base="https://openrouter.ai/api/v1"
)
dspy.configure(lm=lm)

# Create modules
generator = create_text_generator(use_cot=True)
evaluator = create_text_evaluator()

# Create tree-of-thought solver
tot = TreeOfThought(
    generate_module=generator,
    evaluate_module=evaluator,
    
    
)

# Solve a text generation task
ending_sentences = [
    "It caught him off guard that space smelled of seared steak.",
    "People keep telling me orange but I still prefer pink.",
    "Each person who knows you has a different perception of who you are."
]

result = tot.solve(
    ending_sentences=ending_sentences,
    steps=2,
    n_generate_sample=3,
    n_evaluate_sample=2,
    verbose=True
)

print("Generated passages:")
for passage in result['passages']:
    print(passage)

