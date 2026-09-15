import pandas as pd
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

df = pd.read_csv("../synthetic_rti.csv")
labels = ["PWD", "WATER", "EDU", "HEALTH", "RATION", "POLICE", "TRANSPORT", "ELEC", "MUNI", "REV"]
df["label"] = df["label"].map({l: i for i, l in enumerate(labels)})

tokenizer = AutoTokenizer.from_pretrained("l3cube-pune/indic-sentence-similarity-sbert")
ds = Dataset.from_pandas(df)

ds = ds.map(lambda b: tokenizer(b["text"], padding="max_length", truncation=True, max_length=128), batched=True).train_test_split(test_size=0.1)

model = AutoModelForSequenceClassification.from_pretrained("l3cube-pune/indic-sentence-similarity-sbert", num_labels=10)

Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./results",
        num_train_epochs=5,
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        fp16=torch.cuda.is_available(),
        save_strategy="no",
        logging_steps=2
    ),
    train_dataset=ds["train"],
    eval_dataset=ds["test"]
).train()

model.save_pretrained("../fine_tuned_rti")
tokenizer.save_pretrained("../fine_tuned_rti")