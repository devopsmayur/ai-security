# CodeRabbit AI Security Demo

This repository is a deliberately vulnerable, local-only demo for evaluating CodeRabbit Security. It contains four isolated scenarios:

1. Prompt injection in `demo/prompt_injection.py`
2. Poisoned context in `demo/poisoned_context.py` and `demo_data/knowledge.md`
3. Insecure AI output handling in `demo/insecure_output.py`
4. A cross-file authorization and tenant-isolation flaw across `demo/routes.py`, `demo/authorization.py`, and `demo/billing_service.py`

The code is for static analysis only. Do not deploy it, connect it to a real model, or expose it to the internet. All model responses, users, tenants, and records are fake.

## Test workflow

1. Create an empty GitHub repository.
2. Upload the contents of this folder.
3. Open a pull request that adds the demo files, or push the files and run an AI Deep Scan against the committed repository.
4. Run a normal CodeRabbit PR review and a complete CodeRabbit Security AI Deep Scan.
5. Compare the findings with the expected paths below.

For a stronger PR-review test, first create the repository with only `README.md`, then add each scenario in a separate pull request. This makes attribution and review coverage easier to measure.

## Expected findings

### 1. Prompt injection

`demo/prompt_injection.py` places attacker-controlled `user_message` directly into a privileged prompt. The application asks the model to follow instructions in the user message and then trusts the response.

Expected themes:

- Direct prompt injection
- Missing separation between instructions and untrusted data
- Prompt construction from untrusted input
- Excessive agency if the response is later used to select tools

### 2. Poisoned context

`demo/poisoned_context.py` loads a knowledge document and persistent memory, then inserts both into the system prompt as trusted policy. `demo_data/knowledge.md` contains an intentionally poisoned instruction that looks like ordinary operational documentation.

Expected themes:

- Indirect prompt injection
- Context or memory poisoning
- Missing provenance and trust labels
- Retrieved content allowed to override application policy
- Lack of isolation between data and instructions

The poisoned document is inert text. It is not executed by this demo.

### 3. Insecure AI output

`demo/insecure_output.py` sends model output to two dangerous sinks:

- HTML rendering without output encoding
- Shell execution through `shell=True`

Expected themes:

- Improper output handling
- XSS risk
- Command injection or remote code execution risk
- Missing schema validation and allowlisting
- Model output used as a privileged action

### 4. Cross-file logic flaw

The request path is split across several files:

`demo/routes.py` -> `demo/authorization.py` -> `demo/billing_service.py`

The authorization helper checks that a user is authenticated but does not verify that the invoice belongs to the user’s tenant. The service then returns the invoice to the caller.

Expected themes:

- Broken object-level authorization
- IDOR
- Cross-tenant data exposure
- Missing tenant-boundary validation
- Cross-file business-logic flaw

## Suggested questions to ask CodeRabbit

- Can you trace the untrusted input from the HTTP request to the model prompt?
- Which context sources are trusted, and where is that trust established?
- Is model output validated before it reaches HTML, shell, SQL, or privileged APIs?
- Can a user from tenant A access an invoice belonging to tenant B?
- Which files form the complete authorization path?
- What evidence supports the reachability and exploitability classification?

## Safety note

This project intentionally contains vulnerable code. Keep it private or use a disposable public repository. Do not add production credentials, real customer data, or a live model API key.
