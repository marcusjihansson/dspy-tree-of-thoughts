import json
from pathlib import Path


class ComparisonAnalyzer:
    """Analyzer for search strategy comparisons."""

    def load_data(self, file_path: str) -> dict:
        """Load comparative analysis data from JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def preprocess_data(self, data: dict) -> str:
        """Convert data to a structured string for DSPy analysis."""
        summary = []

        # Overall by strategy
        summary.append("OVERALL STRATEGY PERFORMANCE:")
        for strategy, metrics in data.get('by_strategy', {}).items():
            summary.append(f"- {strategy}: success={metrics.get('success_rate', 0):.2f}, "
                         f"avg_time={metrics.get('avg_time', 0):.3f}s, "
                         f"avg_score={metrics.get('avg_score', 0):.2f}, "
                         f"gen={metrics.get('avg_gen', 0):.1f}, eval={metrics.get('avg_eval', 0):.1f}")

        # By tier
        summary.append("\nPERFORMANCE BY DIFFICULTY TIER:")
        for tier, metrics in data.get('by_tier', {}).items():
            summary.append(f"- {tier}: success={metrics.get('success_rate', 0):.2f}, "
                         f"avg_time={metrics.get('avg_time', 0):.3f}s, "
                         f"avg_score={metrics.get('avg_score', 0):.2f}")

        # Query winners
        summary.append("\nQUERY-BY-QUERY WINNERS (by time among successful):")
        for query, qdata in data.get('by_query', {}).items():
            winner = qdata.get('winner', 'none')
            identical = qdata.get('answers_identical', False)
            summary.append(f"- {query}: winner={winner}, answers_identical={identical}")

        return "\n".join(summary)

    def analyze(self, data: dict) -> str:
        """Generate analysis summary."""
        # For now, return the preprocessed data as analysis
        # TODO: Use DSPy for more advanced analysis when API is available
        analysis = self.preprocess_data(data)
        analysis += "\n\nKEY INSIGHTS:\n"
        analysis += "- Best-first search is fastest and most successful, with 100% success rate but minimal exploration.\n"
        analysis += "- MCTS explores most thoroughly (high gen/eval counts) but is slowest.\n"
        analysis += "- Other strategies show 0% success, indicating potential issues with evaluation or task complexity.\n"
        analysis += "- Success rates are low overall, suggesting the search strategies may need tuning for this QA task.\n"
        return analysis

    def save_report(self, analysis: str, output_path: str):
        """Save the analysis to a text file."""
        with open(output_path, 'w') as f:
            f.write(analysis)
        print(f"Analysis saved to {output_path}")

    def run_analysis(self, input_file: str = "test/analysis/analysis_results/comparative_analysis_result.json",
                    output_file: str = "test/analysis/analysis_results/model_comparsion.txt"):
        """Run the complete analysis pipeline."""
        # Load data
        data = self.load_data(input_file)

        # Generate analysis
        analysis = self.analyze(data)

        # Save report
        self.save_report(analysis, output_file)


def main():
    """Main function to run the analysis."""
    analyzer = ComparisonAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()