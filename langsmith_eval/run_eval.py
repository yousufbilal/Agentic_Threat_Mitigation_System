import asyncio
from langsmith.evaluation import aevaluate
from langsmith_eval.target_function import target
from langsmith_eval.evaluators import action_correct, target_correct, severity_correct
from dotenv import load_dotenv
load_dotenv()

async def main():
    results = await aevaluate(
        target,
        data="my_golden_dataset",
        evaluators=[action_correct, target_correct, severity_correct],
        experiment_prefix="baseline",
    )

if __name__ == "__main__":
    asyncio.run(main())