# DSL-LLaDA Website

Paper website and frozen generation-trace replay for
[DSL-LLaDA](https://github.com/fengsxy/DSL-LLaDA).

The published demo compares DSL-LLaDA with LLaDA using matched generation
protocols on:

- XSum summarization at NFE 8
- Three-day Shanghai trip planning at NFE 32
- AESLC subject generation at NFE 8

All displayed generations and intermediate states are frozen traces produced
by the public
[DSL-LLaDA Beta1 checkpoint](https://huggingface.co/liddlefish/DSL-LLaDA-Beta1).
The site does not load a model or require a GPU.

## Run Locally

```bash
bash demo/run_demo.sh
```

Then open <http://localhost:7860>.

## Published Scope

The repository includes the two static pages, the selected trace artifact, and
a Python standard-library replay server. Checkpoints, candidate pools, logs,
and online inference dependencies are intentionally excluded.
