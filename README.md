## memories

Repository containing example code how to parse Memories van Successie through the Google Gemini API. Requires enabled billing since we're using Gemini 2.5 Pro, the best model. 

`gemini_query_sample.py` contains the code used to query the API. It implements a pydantic schema for the Memories van Successie.  `response_{ex1, ex2}.txt` contains the output. 

The output is then parsed to .csv using code in `parse_response_to_csv.py`. The latter can be used via the command line:

```{bash}
python parse-response_to_csv.py response_ex1.txt
```

- To do:
    - For the research internship, create a database with batches of memories
    - Upload them somewhere and link to them in this readme.md
    - Let student assistants upload the annotations to these batches here
    
- Model: Gemma 3N 4b Multimodal fintuning + inference
    - Google Colab Notebook
