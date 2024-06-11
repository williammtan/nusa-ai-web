import gradio as gr
import requests
import json
import time
import os

LANGS = ["en", "ban"]
LANG_DIRECTIONS = ["en-ban", "ban-en"]
LANG_DICT = {
    "en": "English",
    "ban": "Balinese"
}
VLLM_ENDPOINT = "https://polite-grapes-sort.loca.lt/" # TODO: specify this
MODEL_NAME = "nusa-7b-ban"

def greet(input_text, direction):
    src_lang, tgt_lang = direction.split('-')
    if input_text != "":
        json_body = {
            "model": MODEL_NAME,
            "prompt": f"Translate this from {src_lang} to {tgt_lang}:\n{src_lang}: {input_text}\n{tgt_lang}:",
            "max_tokens": 256,
            "temperature": 0
        }
        time_start = time.time()
        r = requests.post(os.path.join(VLLM_ENDPOINT, "v1", "completions"), json=json_body, headers={"bypass-tunnel-reminder": "blahblah"})
        
        if r.status_code == 200:
            time_taken = time.time()-time_start # display this
            output_text = r.json()["choices"][0]["text"]
            translated_text = output_text
        else:
            gr.Error(f"Error {r.status_code}: {r.json()['message']}")
        
    return translated_text

language_direction_strs = [LANG_DICT[l.split('-')[0]]+'->'+LANG_DICT[l.split('-')[1]] for l in LANG_DIRECTIONS]

with gr.Blocks() as demo:
    gr.Interface(
        fn=greet,
        inputs=[
            gr.Textbox(label="Source Sentence", lines=5),
            gr.Radio(
                language_direction_strs, label="Translation Direction", value=language_direction_strs[0]
            )
        ],
        outputs=[gr.Textbox(label="Translated Sentence", lines=5)],
        title="NusaAI Translator",
        examples=[
            ["Silang tersebut taler menandai tanggal hak tersangka mantuka ring diadili dengan cepat.", "Balinese->English"],
            ["Maroochydore ngalahang Caboolture ring final purwaka.", "Balinese->English"],
            # ["He recently lost against Raonic in the Brisbane Open.", "English->Balinese"],
            ["At 11:20, the police asked the protesters to move back on to the pavement, stating that they needed to balance the right to protest with the traffic building up.", "English->Balinese"]
            # ["Di hari Senin, para ilmuan saking Universitas Kedokteran Stanford mengumumkan sarana penemuan diagnosa baru sane nyilang mengurutkan tipe cells: sebuah chip kecil sane mudah dicetak sane nyilang dibuat nganggen standar inkjet printer sane mungking indik salah satu cent U.S.", "Balinese->English"],
            # ["The pilot was identified as Squadron Leader Dilokrit Pattavee.", "English->Balinese"]
        ],
        description="""
## Getting Started
To start using Nusa AI Translator, simply input your text in the text box and select the desired translation direction between Balinese and English.
""",
        article="""

## Features
- **Alpha Version (v0.1)**: Currently supports translation between Balinese and English.
- **Accurate Translations**: Leverages the power of fine-tuned LLMs to provide contextually appropriate translations.
        
## Benchmark
Performance comparison of Nusa AI Translator with other models in translating between Balinese (ban) and English (en) in the [BLEU metric](https://en.wikipedia.org/wiki/BLEU):

| Model                | Ban to En | En to Ban |
|----------------------|-----------|-----------|
| GPT-3.5-turbo-0125   | 18.28     | 7.20      |
| GPT-4o               | 24.04     | 5.24      |
| **Nusa-7b-ban**      | **28.69** | **8.09**  |

(more benchmarks coming soon!)

## Mission
Our goal is to provide a tool that gives 'no boundaries for all languages in Indonesia', ensuring that everyone, regardless of their linguistic background, can access and enjoy the benefits of the digital world.


## Future Updates
We are committed to expanding the capabilities of Nusa AI Translator. Future versions will include support for more Indonesian dialects, improving and enriching communication across different regions of Indonesia.

## Feedback
Your feedback is valuable to us! Please let us know how we can improve your experience by contacting us at [william.h.tan27@gmail.com](mailto:william.h.tan27@gmail.com).

Thank you for choosing Nusa AI Translator, where we strive to connect and empower communities through language.
"""
    )

demo.launch()