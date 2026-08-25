# DSL-LLaDA Website

Paper website and frozen generation-trace replay for
[DSL-LLaDA](https://github.com/fengsxy/DSL-LLaDA).

Live site: <https://fengsxy.github.io/DSL-LLaDA-Website/>

Paper: <https://arxiv.org/abs/2606.01024>

Accepted to Findings of EMNLP 2026.

The unified project page presents the paper, method, results, resources, and an
interactive replay that compares DSL-LLaDA with LLaDA using matched generation
protocols on:

- XSum summarization at NFE 8
- Three-day Shanghai trip planning at NFE 32

All displayed generations and intermediate states are frozen traces produced
by the public
[DSL-LLaDA checkpoint](https://huggingface.co/liddlefish/DSL-LLaDA-Beta1).
The site does not load a model or require a GPU.

## Run Locally

```bash
bash demo/run_demo.sh
```

Then open <http://localhost:7860>.

## Published Scope

The repository includes the unified static homepage, a compatibility redirect
for the former paper-details page, paper figures, the selected trace artifact,
and a Python standard-library replay server. Checkpoints, candidate pools,
logs, and online inference dependencies are intentionally excluded.
