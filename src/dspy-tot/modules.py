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


class TextGenerator(dspy.Module):
    """Module for generating coherent text passages."""

    def __init__(self, use_cot=False):
        super().__init__()
        self.use_cot = use_cot
        if use_cot:
            self.generate = dspy.ChainOfThought(TextGenerationCoT)
        else:
            self.generate = dspy.Predict(TextGeneration)

    def forward(self, ending_sentences):
        # Format ending sentences as a readable string
        ending_text = " ".join(ending_sentences)
        result = self.generate(ending_sentences=ending_sentences)
        return result


class TextEvaluator(dspy.Module):
    """Module for evaluating text passage coherency."""

    def __init__(self):
        super().__init__()
        self.evaluate = dspy.Predict(TextEvaluation)

    def forward(self, passage):
        result = self.evaluate(passage=passage)
        return result


class TextVoter(dspy.Module):
    """Module for voting on the best passage among candidates."""

    def __init__(self):
        super().__init__()
        self.vote = dspy.ChainOfThought(TextVoting)

    def forward(self, instruction, candidates):
        # Format candidates as a readable list
        candidates_text = "\n".join(f"{i+1}. {candidate}"
                                   for i, candidate in enumerate(candidates))
        result = self.vote(instruction=instruction, candidates=candidates_text)
        return result


class TextComparator(dspy.Module):
    """Module for comparing coherency of two passages."""

    def __init__(self):
        super().__init__()
        self.compare = dspy.Predict(TextComparison)

    def forward(self, passage1, passage2):
        result = self.compare(passage1=passage1, passage2=passage2)
        return result


class PassageProposer(dspy.Module):
    """Module for proposing continuation steps in passage generation."""

    def __init__(self):
        super().__init__()
        self.propose = dspy.Predict(PassageProposal)

    def forward(self, current_passage, ending_sentences):
        result = self.propose(
            current_passage=current_passage,
            ending_sentences=ending_sentences
        )
        return result


# Convenience functions to create configured modules
def create_text_generator(use_cot=False):
    """Create a text generator module."""
    return TextGenerator(use_cot=use_cot)


def create_text_evaluator():
    """Create a text evaluator module."""
    return TextEvaluator()


def create_text_voter():
    """Create a text voting module."""
    return TextVoter()


def create_text_comparator():
    """Create a text comparison module."""
    return TextComparator()


def create_passage_proposer():
    """Create a passage proposer module."""
    return PassageProposer()