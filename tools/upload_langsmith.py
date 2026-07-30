from langsmith import Client
from dotenv import load_dotenv
import json

load_dotenv()

client = Client()

dataset = client.read_dataset(dataset_name="my_golden_dataset")

with open("golden_dataset_pe.json") as f:
    golden_data = json.load(f)

for name, case in golden_data.items():
    client.create_example(
        inputs=case["input"],
        outputs=case["expected_output"],
        dataset_id=dataset.id,
        metadata={"case_name": name}
    )

print("Uploaded", len(golden_data), "examples to dataset:", dataset.name)