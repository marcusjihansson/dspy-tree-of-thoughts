import json
import os
import sys
import time
from pathlib import Path

import dspy
import pytest

# Add src and test to path
sys.path.append('src/dspy-tot')
sys.path.append('test')

from methods.factory import create_search_strategy
from evaluation import TextEvaluatorDSPy
from signatures import GenerateContinuation
from common import load_knowledge_base, SimpleRetriever, load_queries, get_profile, PROFILE_PARAMS

# Configure DSPy
dspy.configure(
    lm=dspy.LM(
        model="openrouter/openai/gpt-oss-120b",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
    )
)

KB = load_knowledge_base()
retriever = SimpleRetriever(KB)

evaluator = TextEvaluatorDSPy()

generate_module = dspy.Predict(GenerateContinuation)


class TestBeam:
    STRATEGY = 'beam'

    def generate_fn(self, question):
        def _fn(current_state, n_samples):
            retrieved = retriever.retrieve(question + " " + current_state, top_k=3)
            retrieved_text = '\n'.join(retrieved)
            outs = []
            for _ in range(n_samples):
                r = generate_module(
                    query=question,
                    retrieved_info=retrieved_text,
                    current_answer=current_state
                )
                outs.append((current_state + " " + r.continuation).strip())
            return outs
        return _fn

    def evaluate_fn(self, states):
        scores = []
        for s in states:
            er = evaluator.evaluate_passage(s)
            scores.append(er['score'])
        return scores

    def is_goal_fn(self, state):
        return 'DSPy' in state and len(state.split()) > 80

    @pytest.mark.skipif(not os.getenv('OPENROUTER_API_KEY'), reason='OPENROUTER_API_KEY not set')
    @pytest.mark.parametrize('query', load_queries(get_profile()))
    def test_run_queries(self, query):
        strategy = create_search_strategy(self.STRATEGY)
        question = query['text']
        profile = query['tier']
        params = PROFILE_PARAMS.get(profile, {'max_steps': 5, 'n_select': 2})

        start_time = time.time()
        result = strategy.search(
            initial_state="",
            generate_fn=self.generate_fn(question),
            evaluate_fn=self.evaluate_fn,
            is_goal_fn=self.is_goal_fn,
            max_steps=params['max_steps'],
            n_select=params['n_select']
        )
        end_time = time.time()

        execution_time = end_time - start_time

        if result['final_states']:
            final_answer = result['final_states'][0]
            eval_result = evaluator.evaluate_passage(final_answer)
            eval_score = eval_result['score']
            ind_scores = eval_result.get('individual_scores', [])
            n_evals = eval_result.get('n_evaluations', 0)
        else:
            final_answer = ""
            eval_score, ind_scores, n_evals = 0.0, [], 0

        output = {
            'query_id': query['id'],
            'tier': query['tier'],
            'strategy': self.STRATEGY,
            'question': question,
            'execution_time': execution_time,
            'success': result['success'],
            'steps_taken': result['steps_taken'],
            'final_answer': final_answer,
            'evaluation_score': eval_score,
            'individual_scores': ind_scores,
            'n_evaluations': n_evals
        }

        Path('test/results').mkdir(parents=True, exist_ok=True)
        with open(f"test/results/{self.STRATEGY}_{query['id']}.json", 'w') as f:
            json.dump(output, f, indent=2)
