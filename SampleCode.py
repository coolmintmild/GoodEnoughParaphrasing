from openai import OpenAI
import pandas as pd
import time

api_key = 'your_api_key'
client = OpenAI(api_key=api_key)


data = pd.DataFrame()
df = pd.read_excel("your_file_path")

# Set the number of iterations you want to perform.
num_iterations = 10  # Change this to your desired number of iterations.

# Iterate the designated number of times.
for i in range(num_iterations):
    # Iterate over the models.
    for model in ['gpt-3.5-turbo', 'gpt-4']:
        ppsents = []
        # Create a copy of the df for this iteration to avoid altering the original df.
        temp_df = df.copy()
        temp_df["model"] = model  # Add a column for the model.
        temp_df["iteration"] = i + 1  # Add a column for the iteration number.

        # Iterate over sentences in the df.
        for sent in temp_df.sent:
            # Generate the paraphrased sentences using the OpenAI API.
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": "Read the sentence and paraphrase it. But do not simply repeat the sentence. It is recommended to use synonyms."},
                    {"role": "user", "content": sent}
                ]
            )
            # "Paraphrase the sentence. But do not simply repeat the sentence. It is recommended to use synonyms."
            ppsent = completion.choices[0].message.content
            ppsents.append(ppsent)
            time.sleep(0.1)  # Sleep to prevent hitting API rate limits.

        # Assign the paraphrased sentences to the temp DataFrame.
        temp_df["ppsent"] = ppsents

        # Append the results to the main DataFrame.
        data = pd.concat([data, temp_df], ignore_index=True)

# Now 'data' contains the combined data for both models and all iterations.
data.to_excel("your_output_file_path")