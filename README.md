# Bedrock Contact Center Tasks Evaluation

This repository provides a comprehensive framework for evaluating foundation models from leading model providers (such as Anthropic, Cohere and others) available within [Amazon Bedrock](https://aws.amazon.com/bedrock/) on contact center tasks such as generating summaries containing reasons for a call.

It includes scripts for processing raw transcript data, generating summaries using different models, and comparing these summaries against golden summaries to evaluate their effectiveness. Here, users can feel flexible in performing multiple tasks, such as generating extracted questions from meetings, action items, summaries, based on specific prompts that you may want to experiment with.

## Prerequisites

Before you start, ensure the following prerequisites are met:

1. Raw Transcripts: Add your raw transcript files in the [`data/raw`](data/raw/) directory.

1. Labels File: Create a [`labels.txt`](data/raw/labels.txt) file in the [`data/raw`](data/raw/) directory. This file contains the name of each transcript file followed by its corresponding golden summary. The format should be `file_name | golden_summary_content`. Here is an example:

    ```
    call_center_transcript_0 | <output> Here are the action items I gathered for each person: A: - Document any other user entry concerns to provide to B B: - Work with James from another team to simplify additional forms and sign up workflow C:  - Work on landing page to make product more discoverable </output>

    call_center_transcript_1 |  Here are the action items I gathered for each person from the conversation: <output> A: - Set up a follow-up meeting to brainstorm ideas for where generative AI could be applicable in our products - Outline high-level ideas for where generative AI could drive automation or enhance user experience in our products B: - Research current generative AI initiatives at other tech companies to analyze the competitive landscape C: - Develop a validation framework to rigorously assess accuracy, ethics and safety of any generative AI applications we develop </output>
    ```

## Step-by-Step Guide: Notebook executions

1. `Set Up the Environment`: [`0_setup.ipynb`](./0_setup.ipynb): This notebook prepares the environment for processing. It initializes account settings and tracks files for summaries and raw transcripts. You'll need to configure your SageMaker execution role and model offerings in the [`config.yaml`](config.yaml) file.


1. `Generate Summaries`: [`1_summarize.ipynb`](./1_summarize.ipynb): Run this notebook to generate summaries. It accesses foundation models (like Cohere, Anthropic, and Titan) configured in your [`config.yaml`](config.yaml) file. Each model will process the transcripts to create summaries, which are stored in the completions folder. The execution time of the last cell depends on the number of transcripts and the model offerings you use.


1. `Analyze Results`: [`2_results.ipynb`](./2_results.ipynb): This notebook calculates metrics and generates a CSV file with a side-by-side comparison of the golden summaries (as ground truth) and the model-generated summaries. The results are stored in the metrics folder for easy review and comparison.

## Analysis: Metrics | Ground truth comparison with Model Summaries

You can view the results of the comparison of model summaries with respective ground truth/golden summaries in the [`golden_summary_model_comparison.csv`](./golden_summary_model_comparison.csv) file and the metrics within the [`metrics.csv`](./data/metrics/model_metrics.csv) file. These files will contain an in-depth metric evaluation walkthrough and a comparison of each model output against the prompt and the actual golden/target summary for your specific use case using cosine similarity and rouge score. You can change these tables and the metrics as need be, but these lay a strong foundation in terms of not only evaluating model responses but effectively comparing and selecting the best model, in terms of performance and cost, for your specific use case.

## Conclusion

By following these steps, you can efficiently evaluate various foundation models on their ability to summarize contact center transcripts. This process provides a structured approach to understand model performance and helps in making informed decisions about deploying AI models in a contact center environment.

## Security

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

See the [LICENSE](./LICENSE) file.
