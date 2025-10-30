import dspy


class TextGeneration(dspy.Signature):
    """Generate a coherent passage of 4 short paragraphs with given ending sentences."""

    ending_sentences = dspy.InputField(desc="List of 4 sentences that must be the ending sentences of each paragraph")
    passage = dspy.OutputField(desc="A coherent passage of 4 short paragraphs where each paragraph ends with one of the provided sentences")


class TextGenerationCoT(dspy.Signature):
    """Generate a coherent passage using chain-of-thought reasoning."""

    ending_sentences = dspy.InputField(desc="List of 4 sentences that must be the ending sentences of each paragraph")
    plan = dspy.OutputField(desc="A plan for creating a coherent passage")
    passage = dspy.OutputField(desc="A coherent passage of 4 short paragraphs where each paragraph ends with one of the provided sentences")


class TextEvaluation(dspy.Signature):
    """Evaluate the coherency of a text passage."""

    passage = dspy.InputField(desc="The text passage to evaluate")
    score = dspy.OutputField(desc="Coherency score from 1 to 10 (integer)")


class TextComparison(dspy.Signature):
    """Compare the coherency of two text passages."""

    passage1 = dspy.InputField(desc="First passage to compare")
    passage2 = dspy.InputField(desc="Second passage to compare")
    comparison = dspy.OutputField(desc="Analysis of which passage is more coherent: '1' if passage1 is better, '2' if passage2 is better, or 'equal' if they are similarly coherent")


class TextVoting(dspy.Signature):
    """Vote on the best passage among multiple candidates."""

    instruction = dspy.InputField(desc="The original task instruction")
    candidates = dspy.InputField(desc="List of candidate passages to choose from")
    analysis = dspy.OutputField(desc="Detailed analysis of each candidate")
    best_choice = dspy.OutputField(desc="The index (1-based) of the best candidate passage")


class PassageProposal(dspy.Signature):
    """Generate multiple possible next steps for building a passage."""

    current_passage = dspy.InputField(desc="The current partial passage")
    ending_sentences = dspy.InputField(desc="List of sentences that must end paragraphs")
    proposals = dspy.OutputField(desc="List of possible continuation proposals")


class GenerateContinuation(dspy.Signature):
    """Generate the next part of the answer using retrieved information."""

    query = dspy.InputField(desc="The question being answered")
    retrieved_info = dspy.InputField(desc="Relevant information retrieved")
    current_answer = dspy.InputField(desc="Current partial answer")
    continuation = dspy.OutputField(desc="Next continuation of the answer")
