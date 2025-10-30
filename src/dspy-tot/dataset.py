import dspy
import os


class TextGenerationExample(dspy.Example):
    """Example for text generation task."""
    pass


class TextGenerationDataset:
    """Dataset for text generation task where we need to create coherent passages."""

    def __init__(self, data_file=None):
        if data_file is None:
            # Default path relative to this file
            data_file = os.path.join(os.path.dirname(__file__), 'data', 'text', 'data_100_random_text.txt')

        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """Load the text data from file."""
        with open(self.data_file, 'r') as f:
            lines = f.readlines()

        self.examples = []
        for line in lines:
            line = line.strip()
            if line:
                # Each line contains 4 sentences that should be the ending sentences
                # of 4 paragraphs in a coherent passage
                ending_sentences = [s.strip() for s in line.split('.') if s.strip()]
                if len(ending_sentences) >= 4:
                    ending_sentences = ending_sentences[:4]  # Take first 4 sentences

                    example = TextGenerationExample(
                        ending_sentences=ending_sentences,
                        input_text=line  # Store original line for reference
                    )
                    self.examples.append(example)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]

    def train_split(self, n=None):
        """Get training split."""
        if n is None:
            n = len(self.examples) // 2
        return self.examples[:n]

    def dev_split(self, n=None):
        """Get development split."""
        if n is None:
            n = len(self.examples) // 4
        start_idx = len(self.examples) // 2
        return self.examples[start_idx:start_idx + n]

    def test_split(self, n=None):
        """Get test split."""
        if n is None:
            n = len(self.examples) // 4
        start_idx = len(self.examples) - n
        return self.examples[start_idx:]


# Create a global dataset instance
text_dataset = TextGenerationDataset()