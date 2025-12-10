# RoB 2 Automation

Tools and notebooks for automating Risk of Bias (RoB 2) assessments across study PDFs. The repo wraps domain-specific logic (randomization, adherence, missing data, measurement, reporting) and a processing notebook to generate per-study Excel responses.

## Contents
- `pdf_to_text.ipynb` — main notebook: uploads PDFs from `studies/`, walks domain signalling questions, and writes `outputs/<pdf_stem>_responses.xlsx`.
- `rob2/` — domain logic, shared enums/helpers, and a registry (`rob2.domains`) exposing questions, question flow, and evaluators for each domain.
- `prompts/` — prompt text for signalling questions.
- `studies/` — place PDFs to process; outputs land in `outputs/`.

## Setup
1) Install dependencies (Python 3.10+ recommended):
   ```bash
   pip install -r requirements.txt
   ```
   or ensure `openai`, `pandas`, `openpyxl` are available.
2) Provide your API key via `.env` (`API_KEY=...`) or environment.

## Running the notebook
1) Add PDFs to `studies/`.
2) Open `pdf_to_text.ipynb` and run the cells. The notebook:
   - Loads domain specs from `rob2.domains.get_domain_specs()`.
   - Iterates PDFs one at a time.
   - For each domain, fetches prompts from `prompts/`, calls the model, and saves an Excel file named after the input PDF.

## Domain registry
- Domains implement the shared `BaseDomain` interface (`rob2/common.py`).
- Registry (`rob2/domains.py`) maps domain keys to implementations and exposes `get_domain_specs()` for consumers.
- Each domain module also exports `QUESTIONS` and compatibility helpers for legacy imports.

## Attribution and licensing for RoB 2 content
- The signalling questions are obtained verbatim from the Cochrane Risk of Bias 2 (RoB 2) tool and are provided under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0). See `NOTICE` and `LICENSES/CC-BY-NC-ND-4.0.txt`.
- This codebase is licensed separately; use of the RoB 2 content must comply with the CC BY-NC-ND terms (non-commercial, no derivatives, attribution required).

## Notes
- Outputs are stored under `outputs/`.
- Prompt files must exist for each signalling question; missing prompts are reported in the notebook output.
