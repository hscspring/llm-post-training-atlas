# LLM Post-Training Atlas / 大模型后训练图谱

> **An opinionated map of post-R1 LLM post-training — RL, reward, alignment, distillation, agents, and the connections between them.**
> Every work is read, classified, and cross-linked; most are connected back to a Chinese deep-dive by [hscspring](https://yam.gift).

**Scope: post-R1 LLM post-training · continuously updated**

[Verdicts](#7-tracks--the-authors-verdicts) · [Papers](#papers) · [Timeline](#chronological-blog-timeline) · [Scope](#scope--inclusion-policy)

This repository maps the **post-R1 LLM post-training** landscape. RL is its intellectual spine, not its boundary: the real question is how a model's policy is shaped — through reward, preference, demonstration, distillation, context, experience, or interaction.

## Scope & Inclusion Policy

- **Core scope**: post-R1 LLM post-training — RL/RLVR, policy optimization, reward and verifiers, alignment, SFT/DPO, on-policy distillation, agent learning, and post-training stability.
- **Adjacent methods are included when they clarify the same mechanism**: Training-Free RL, activation/context steering, real-time adaptation, and policy-diff learning belong here when they illuminate how behavior or policy changes.
- **Cross-domain work is selective**: multimodal, diffusion, flow, and embodied papers are included only when their mechanism transfers back to the shared post-training picture.
- **Pure pre-training is excluded**: scaling laws, NTP, continual pre-training, and base-model construction stay out unless they are necessary context inside a post-training analysis.
- **The boundary is conceptual, not terminological**: a paper does not need to call itself “RL”; it needs to contribute a meaningful signal, objective, estimator, or feedback loop for shaping policy.

## Why this repo (and not another Awesome list)

Awesome lists are *retrievers*. This repo is a *curator*.

- **Has a verdict, not a vote.** Each of the 7 tracks ends with the author's bottom-line judgment ("data sets the ceiling, algorithms approach it"; "most RL is sampling polish, not extrapolation"; "all internal-feedback methods compress entropy → exploration crisis"), not a paper summary.
- **Cross-links across papers.** RLOO ≡ GRPO with Fnorm=1 (derived in GiGPO); REINFORCE + IS → CISPO loss (extended in CISPO); Activation Steering & Context Engineering are the *upstream signals* of Training-Free RL. These connections only surface when one person reads everything.
- **A narrative, not a database.** The Chronological Blog Timeline reads as a year-and-a-half *editorial arc*: R1 → GRPO family → Reward modeling → MoE stability → Training-Free RL → policy diff → OPD × RL.
- **Personal historical anchors.** Pre-R1 works (RL4LMs, FTHP, Quark, DT) live in their own corner with a one-line *why I personally cared*, not as bibliography filler.

**Core coverage**: RL reasoning · GRPO and policy optimization · reward/verifiers · data and scaling · MoE stability · Agentic RL · Training-Free behavior shaping · SFT/RL unification · OPD and policy-diff learning.

---

## 7 Tracks · The Author's Verdicts

Blog posts on [yam.gift](https://yam.gift) are grouped into 7 tracks. Each verdict below is the author's own bottom-line judgment, not a paper summary.

### Track 01 — R1 Full-Chain (2025)

> Parsing the original report, then digging into the data / paradigm / experiment side.

- **Core thesis**: data sets the ceiling, algorithms only approach it. Pure rule-based RL is finally validated as a viable path.
- **The frame that survived**: "Base+SFT / Base+RL / SFT+RL" can absorb almost all subsequent variations.
- **Loose ends still being chased**: R1-Zero behavior differs sharply across base models (SimpleRL-Zoo, Yarz-Logic); LIMO/s1 confirm "less is more on *activation*, not on *teaching*".

### Track 02 — GRPO Family & Engineering Refinements (2025–2026)

> Every GRPO variant — DAPO / Dr.GRPO / VAPO / CISPO / GSPO / GMPO / GTPO / Reinforce++ / industry showcases — plus the TRPO → FiberPO theoretical spine.

- **Core thesis**: every variant is paying off the *same* engineering debt — token vs. sequence-level, clip tighter/wider, length normalization, KL choice (k2 vs k3), advantage global-normalization.
- **Convergence**: the GRPO objective increasingly looks like a "people's edition" of PPO with global advantage and no critic.
- **Sub-thread — clip**: clip is not just a stability knob — it directly *shapes* the explore/exploit boundary. Spurious Rewards, Clip-Higher (DAPO), Clip-Wider (GMPO) are all moves on the same axis. SIS breaks the axis itself: token-level rejection sampling turns 60–80% of off-policy tokens *back into* on-policy ones (weight = 1, zero bias) instead of suppressing their gradients — stability without sacrificing signal.
- **Sub-thread spun off — Agentic RL**: GiGPO / COPO / GAGPO grew out of GRPO's grouping idea, but step-level credit assignment is its own problem axis — now Track 07 below.
- **Sub-thread — TRPO foundation**: TRPO is the theoretical bedrock (IS + Trust Region + Advantage). FiberPO's vanishing theorem shows γ must be 1 in LLM RL, collapsing TRPO's trust region radius to zero — PPO/GRPO clip is an empirical δ-relaxation of this collapsed bound.
- **Sub-thread — advantage shaping for exploration** (2025-H2 red ocean): the fix for GRPO's exploitation collapse is increasingly to reshape the *advantage scalar itself* (zero-touch the loss), not the clip. Pass@k training dynamically weakens negative-sample penalties by the global correct-count (harder problems get more tolerance); AAPO adds a frozen-reference margin; ProGRPO folds in generative confidence (difficulty × certainty); GRPOEA/EMPG modulate advantage by entropy; BAPO/ASPO push the same idea down to token-level asymmetric clipping. The common realization: over-penalizing negatives is what kills exploration, and the negative-advantage term matters as much as the positive.
- **Cross-architecture warning — DLM RL**: JustGRPO shows that a more flexible generation order can *reduce* exploration by postponing high-entropy branch points until bidirectional context has already collapsed the option set. Flexibility at inference time is not automatically useful flexibility during policy optimization.

### Track 03 — Reward Modeling, Data & Verifiers (2025–2026)

> RM / RM-Data / Verifier-Free / Self-Verified / Verify-Free RL / Reward Philosophy.

- **Drift 1 (modeling)**: from single scalar → "principles + critique + self-verification" (DeepSeek-GRM → DeepSeekMath-V2).
- **Drift 2 (data)**: good reward data is more like *unlocking* the base model's existing capabilities than *teaching* new ones (Skywork-Reward-V2, Spurious Rewards).
- **Drift 3 (Verify-Free)**: when no external verifier exists, all internal-feedback methods (TTRL / EM / RENT / EMPO / Intuitor) end up *compressing* entropy. Long-term, an exploration crisis is inevitable — ETTRL / Darling / EVOL-RL / RESTRAIN are all band-aids on the same wound.
- **Drift 4 (philosophy)**: a reward is a *lossy compression* of preference, and always lossy. Reward hacking is therefore structural, not a bug — RMs provably memorize surface heuristics (length, tone, sycophancy). The reframe: treat reward as a *prior to be revised*, not ground truth; the "Reward is Enough" vs "Scalar reward is not enough" debate is really about whether one scalar can carry a vector of incommensurable preferences.

### Track 04 — MoE RL Stability (2026)

> R3 / IcePop / TIS / KAT-Coder.

- **Surface diagnosis**: train-infer router mismatch is what everyone first noticed.
- **Deeper cause**: logprob estimation noise on MoE is not neutral; even *recomputing* logprobs drifts. The importance ratio (π_new/π_old) — heart of GRPO — is silently diluted on MoE.
- **Open bet**: GSPO/GMPO's sequence-level + geometric-mean might be MoE-RL-friendly; not yet validated at production scale.

### Track 05 — Paradigm Frontier (2025–2026)

> Training-Free / Experiential / Real-time / Planning / RL Boundary.

- **Boundary realization**: most RL is just sampling polish (Yue), *not* true pass@k extrapolation.
- **Counter-evidence**: ProRL / DELTA show extrapolation is possible — but only with edge data + process reward + avoiding "all-zero pass@k" cold start.
- **Upstream signals (already in 2025 H2)**: "Activation Steering" and "Context Engineering" both pointed in this direction *before* Training-Free RL had a name — behavior can be shaped without touching weights.
- **New paradigm A — Training-Free RL**: advantage lives in text/context, not in weight space (TRT, Training-Free GRPO, MemAPO, Update-Free Steering).
- **New paradigm B — Experience-as-RL**: the loop becomes "trajectory → information gain → re-supervision". Reflection, meta-search and open-ended learning are all data-construction tricks in disguise.
- **Constraint alignment**: instruction following becomes RLVR once a complex instruction is decomposed into checkable constraints. The hard part moves from inventing a new optimizer to engineering verifiers and preference pairs that preserve every constraint.
- **Higher-level question**: "reasoning" should be studied as a *data format*, not as an RL task (Think-Strategy / LEPA).
- **Forward extrapolation of this track** (cited anchor, not a paper deep-dive): [从持续学习到下一代 AI 方向探讨](https://yam.gift/2026/08/08/AI/2026-08-08-Next-AI/) argues the next-gen learning unit is *experience*, not token — with RL as the self-evolution core (Sutton's continual backprop, experience-based learning, In-Place TTT, PEFT-scaling). It is the forward-looking companion to the Pre-R1 reflection anchor [AI-Future-Framework](https://yam.gift/2026/01/25/AI/2026-01-25-AI-Future-Framework/).

### Track 06 — Unified Theory of Post-Training (2026)

> SFT × RL interplay, distillation × RL, forgetting dynamics, distribution alignment — the search for one theory behind all post-training methods.

- **Core thesis**: SFT is a special case of RL (single-path, 1/π_θ-weighted). The question is not "can SFT generalize?" but "which layer is activating vs. memorizing?"
- **Forgetting law**: on-policy RL stays closer to base (KL-minimal path → less forgetting, RL's Razor); SFT can drift arbitrarily far.
- **One estimator**: HPT/GFT unify SFT/RL into one policy gradient estimator, differing only in data source and stabilizer.
- **Distribution alignment lens**: SVM / DPO / RLHF / SFT all reduce to aligning a policy distribution to target anchors via log density-ratio rewards (r = log d⁺/d⁻). Differences lie in three axes: anchor count (one vs two), KL direction (forward = mode-covering SFT, reverse = mode-seeking RL/DPO — the same axis as MiniLLM's reverse-KL distillation), and anchor observability (explicit classifier vs implicit optimal policy). SFT's "pure pull, no push" (only d⁺, no d⁻) explains its instability on low-probability tokens (GFT's 1/π_θ explosion).
- **Distillation–RL bridge**: OPD first isolates a teacher's *capability direction* as policy diff instead of copying its raw output; when that diff comes from an RL-trained teacher, it is also an implicit reward. The same directional signal can reconstruct a target policy (OPD), become a dense reward (Direct-OPD), or reshape verifier gradients without changing their stationary points (OPRD).

### Track 07 — Agentic RL (2025–2026)

> Step-level credit assignment for multi-turn agent tasks: GiGPO / COPO / GAGPO / SVM. Spun off from Track 02's grouping idea — now its own problem axis.

- **What makes it different**: agent tasks have *real* steps — physically meaningful, often near-deterministic transitions — unlike the pseudo-steps of token-level reasoning. That stability is an exploitable "anchor".
- **The arc is one question** — how to get per-step advantage without a critic: GiGPO (hierarchical group-in-group advantage) → COPO (cognitive-mode step reweighting) → GAGPO (group-based V estimation + GAE, pulling back toward PPO+GAE) → SVM (success/failure visitation classifier turns sparse outcome reward into dense process reward).
- **Direction**: sparse → dense; each method differs only in *which anchor it trusts* (group statistics / cognitive modes / historical visitation). SVM's log density-ratio reward connects this thread straight into Track 06's distribution-alignment lens.

---

## Papers

Notation for the **My Notes** column:
- `[short title](url)` — full Chinese deep-dive available (yam.gift blog or book chapter)
- `(omnibus → ...)` — covered as a main thread in a survey/overview blog
- `(<verb: derived/extended/contrasted/described/framed/criticized/...> in [blog]: ...)` — touched on as a sub-topic inside another deep-dive, with a one-line pointer; multiple pointers can be chained with `;`
- *to-write* — not yet written
- `(shelved: ...)` — deliberately *not* written; the one-line reason is itself the verdict

Track-to-index map: **01** → R1 reproduction + data/scaling · **02** → GRPO + exploration + optimization foundations · **03** → reward + verifier-free · **04** → MoE stability · **05** → frontier + behavior shaping + instruction following · **06** → SFT/RL + policy diff · **07** → Agentic RL.

### RL Reasoning Reproduction (R1 and Beyond)

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| R1 | DeepSeek-R1: Incentivizing Reasoning Capability via RL | DeepSeek | 2025 | [paper](https://github.com/deepseek-ai/DeepSeek-R1) | [DeepSeek R1 深度技术解析及其影响](https://yam.gift/2025/02/17/NLP/LLM-Training/2025-02-17-DeepSeek-R1/) |
| LIMO | LIMO: Less Is More for Reasoning | SJTU | 2025 | [paper](https://arxiv.org/abs/2502.03387) | [少量高质量数据 SFT 激活推理](https://yam.gift/2025/02/18/NLP/LLM-Training/2025-02-18-LLM-PostTrain-SFT-Data/) |
| s1 | s1: Simple test-time scaling | Stanford | 2025 | [paper](https://arxiv.org/abs/2501.19393) | (omnibus → [SFT-Data](https://yam.gift/2025/02/18/NLP/LLM-Training/2025-02-18-LLM-PostTrain-SFT-Data/)) |
| R1 Survey | The R1-era LLM new paradigm | — | 2025 | — | [DeepSeek R1 后 LLM 新范式](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/) |
| R1-Zero+ | Further understanding of R1-Zero | — | 2025 | — | [R1-Zero 的进一步理解和探索](https://yam.gift/2025/04/10/NLP/LLM-Training/2025-04-10-Think-More-about-R1-Zero/) |
| SimpleRL-Zoo | SimpleRL-Zoo: R1-Zero RL across diverse base models | HKUST | 2025 | [paper](https://arxiv.org/abs/2503.18892) | (omnibus → [Think-More-about-R1-Zero](https://yam.gift/2025/04/10/NLP/LLM-Training/2025-04-10-Think-More-about-R1-Zero/)) |
| FastCuRL | FastCuRL: Curriculum RL with Stage-wise Context Scaling | — | 2025 | [paper](https://arxiv.org/abs/2503.17287) | (omnibus → [Think-More-about-R1-Zero](https://yam.gift/2025/04/10/NLP/LLM-Training/2025-04-10-Think-More-about-R1-Zero/)) |
| Logic-RL | Logic-RL: Unleashing LLM Reasoning with Rule-Based RL | — | 2025 | [paper](https://arxiv.org/abs/2502.14768) | [Yarz-Logic：R1-Zero 相关实验报告](https://yam.gift/2025/04/26/NLP/LLM-Training/2025-04-26-R1-Zero-Lab-Yarz-Logic/) |
| Seed-Thinking | Seed-Thinking-v1.5: Advancing Superb Reasoning | ByteDance | 2025 | [paper](https://arxiv.org/abs/2504.13914) | [R1 后范式最佳实践：Seed-Thinking 和 Qwen3](https://yam.gift/2025/05/01/NLP/LLM-Training/2025-05-01-Seed-Thinking-Qwen3/) |
| Qwen3 | Qwen3 Technical Report | Qwen | 2025 | [paper](https://arxiv.org/abs/2505.09388) | (omnibus → [Seed-Thinking-Qwen3](https://yam.gift/2025/05/01/NLP/LLM-Training/2025-05-01-Seed-Thinking-Qwen3/)) |

### RL Data Selection & Scaling

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| LIMR | LIMR: Less is More for RL Scaling | GAIR-NLP | 2025 | [paper](https://arxiv.org/abs/2502.11886), [GitHub](https://github.com/GAIR-NLP/LIMR) | [R1 相关：RL 数据选择与 Scaling](https://yam.gift/2025/02/27/NLP/LLM-Training/2025-02-27-LLM-PostTrain-PPO-Data/) |
| ORZ | Open-Reasoner-Zero | StepFun | 2025 | [paper](https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero/blob/main/ORZ_paper.pdf), [GitHub](https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero) | (omnibus → [PPO-Data](https://yam.gift/2025/02/27/NLP/LLM-Training/2025-02-27-LLM-PostTrain-PPO-Data/)) |
| Online-DPO-R1 | Online-DPO-R1: Effective Reasoning Without the PPO Overhead | Salesforce | 2025 | [paper](https://efficient-unicorn-451.notion.site/Online-DPO-R1-Unlocking-Effective-Reasoning-Without-the-PPO-Overhead-1908b9a70e7b80c3bc83f4cf04b2f175), [GitHub](https://github.com/RLHFlow/Online-DPO-R1) | [R1 相关：DPO 数据选择与 DPO 等 RL 算法](https://yam.gift/2025/03/02/NLP/LLM-Training/2025-03-02-LLM-PostTrain-DPO-Data/) |
| LIMD | LIMD: Less is More on DPO Data | — | 2025 | — | (omnibus → [DPO-Data](https://yam.gift/2025/03/02/NLP/LLM-Training/2025-03-02-LLM-PostTrain-DPO-Data/)) |
| OREAL | Exploring the Limit of Outcome Reward for Math Reasoning | InternLM | 2025 | [paper](https://arxiv.org/abs/2502.06781), [GitHub](https://github.com/InternLM/OREAL) | (shelved: the "limit of outcome reward" question got absorbed by the process/dense-reward thread — DELTA / SVM — and RM-Data's "unlocking" view) |
| DeepScaleR | DeepScaleR: Surpassing O1-Preview with a 1.5B Model by Scaling RL | Agentica | 2025 | [paper](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2), [GitHub](https://github.com/agentica-project/deepscaler) | (omnibus → [R1-New-Paradigm](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/)) |
| L1 / LCPO | Controlling How Long A Reasoning Model Thinks With RL | CMU | 2025 | [paper](http://arxiv.org/abs/2503.04697), [GitHub](https://github.com/cmu-l3/l1) | (omnibus → [R1-New-Paradigm](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/)) |
| MRT | Optimizing Test-Time Compute via Meta RL Fine-Tuning | CMU | 2025 | [paper](http://arxiv.org/abs/2503.07572), [GitHub](https://github.com/CMU-AIRe/MRT) | (shelved: budget control already covered by L1/LCPO in [R1-New-Paradigm](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/); its dense progress reward is the same sparse→dense move as Track 07) |
| ScalingLaw | Value-Based Deep RL Scales Predictably | Berkeley | 2025 | [paper](https://arxiv.org/abs/2502.04327) | *to-write* (as the pre-LLM anchor of a future "RL Scaling Law" post — ScaleRL-era work as the main thread; RL compute scaling is currently the index's blind spot) |

### Reward Model (modeling / data / verifier)

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| GRM | Inference-Time Scaling for Generalist Reward Modeling | DeepSeek | 2025 | [paper](https://arxiv.org/abs/2504.02495) | [Reward Model 建模](https://yam.gift/2025/06/09/NLP/LLM-Training/2025-06-09-RM-Modeling/) |
| Skywork-Reward-V2 | Skywork-Reward-V2 | Skywork | 2025 | [paper](https://arxiv.org/abs/2507.01352) | [Reward 数据如何塑造与激发推理策略](https://yam.gift/2025/07/13/NLP/LLM-Training/2025-07-13-RM-Data/) |
| Spurious Rewards | Spurious Rewards: Rethinking Training Signals in RLVR | Allen | 2025 | [paper](https://arxiv.org/abs/2506.10947) | (omnibus → [RM-Data](https://yam.gift/2025/07/13/NLP/LLM-Training/2025-07-13-RM-Data/) / [GRPO-Clip](https://yam.gift/2025/09/12/NLP/LLM-Training/2025-09-12-GRPO-Clip/)) |
| ICM | Anthropic Internal Coherence Maximization | Anthropic | 2025 | [blog](https://www.anthropic.com/research) | (omnibus → [RM-Data](https://yam.gift/2025/07/13/NLP/LLM-Training/2025-07-13-RM-Data/)) |
| DeepSeekMath-V2 | Towards Self-Verifiable Mathematical Reasoning | DeepSeek | 2025 | [paper](https://github.com/deepseek-ai/DeepSeek-Math-V2), [GitHub](https://github.com/deepseek-ai/DeepSeek-Math-V2) | [DeepSeekMath-V2 自我验证：搞数据的风吹到了 RM](https://yam.gift/2025/11/29/NLP/LLM-Training/2025-11-29-Reward-Data-Self-Verified/) |

### Reward Philosophy & Foundations

> What a reward *is*, why reward hacking is structural, and whether one scalar can carry intelligence. All covered in one blog: [Reward 设计的本质：从 hack 到 hard](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/).

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| RM-Memorize | What do Reward Models Memorize? | DeepMind | 2026 | [paper](https://arxiv.org/abs/2607.24484) | [Reward 设计的本质：从 hack 到 hard](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/) (RMs memorize surface heuristics → reward hack is structural) |
| Reward is Enough | Reward is Enough | DeepMind (Silver, Singh, Precup, Sutton) | 2021 | [paper](https://www.sciencedirect.com/science/article/pii/S0004370221000862) | (omnibus → [Reward-Design](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/): a single scalar reward can drive all of intelligence — AlphaZero as proof) |
| Scalar Reward not Enough | Scalar Reward is not Enough | Vamplew et al. | 2021 | [paper](https://arxiv.org/abs/2112.15422) | (omnibus → [Reward-Design](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/): rebuttal — intelligence needs vector/multi-objective rewards) |
| Era of Experience | Welcome to the Era of Experience | Sutton & Silver | 2025 | [paper](http://incompleteideas.net/papers/TheEraOfExperience.pdf) | (omnibus → [Reward-Design](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/): user-guided reward adaptation over grounded signals; bi-level optimization) |
| Why LMs Hallucinate | Why Language Models Hallucinate | OpenAI | 2025 | [paper](https://arxiv.org/abs/2509.04664) | (omnibus → [Reward-Design](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/): hallucination as a form of reward hack — binary benchmarks make "admit uncertainty" never optimal) |

### Verifier-Free RL (internal-feedback RL)

> Two blogs ([Verifier-Free RL](https://yam.gift/2025/11/11/NLP/LLM-Training/2025-11-11-RM-New-Paradigm-Verifier-Free-RL/) and [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) cover the algorithms below — listed individually for searchability.

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| NOVER | NOVER: Incentive Training without External Verifiers | — | 2025 | [paper](https://arxiv.org/abs/2505.16022) | [无验证器 RL 与 Reference 的妙用](https://yam.gift/2025/11/11/NLP/LLM-Training/2025-11-11-RM-New-Paradigm-Verifier-Free-RL/) |
| TTRL | TTRL: Test-Time Reinforcement Learning | — | 2025 | [paper](https://arxiv.org/abs/2504.16084) | [无验证 RL——当模型只能相信自己](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/) |
| SRT | Can Large Reasoning Models Self-Train? | — | 2025 | [paper](https://arxiv.org/abs/2505.21444) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| EM | The Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning | — | 2025 | [paper](https://arxiv.org/abs/2505.15134) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/); covers EM-FT / EM-RL / EM-INF) |
| RENT | Maximizing Confidence Alone Improves Reasoning | — | 2025 | [paper](https://arxiv.org/abs/2505.22660) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| EMPO | Right Question is Already Half the Answer: Fully Unsupervised LLM Reasoning Incentivization | — | 2025 | [paper](https://arxiv.org/abs/2504.05812) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| Intuitor | Learning to Reason without External Rewards | — | 2025 | [paper](https://arxiv.org/abs/2505.19590) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| ETTRL | ETTRL: Balancing Exploration and Exploitation via Entropy Mechanism | — | 2025 | [paper](https://arxiv.org/abs/2508.11356) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| Darling | Jointly Reinforcing Diversity and Quality in Language Model Generations | — | 2025 | [paper](https://arxiv.org/abs/2509.02534) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| EVOL-RL | Evolving Language Models without Labels: Majority Drives Selection, Novelty Promotes Variation | — | 2025 | [paper](https://arxiv.org/abs/2509.15194) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| RESTRAIN | RESTRAIN: From Spurious Votes to Signals — Self-Driven RL with Self-Penalization | — | 2025 | [paper](https://arxiv.org/abs/2510.02172) | (omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |
| No Free Lunch | No Free Lunch: Rethinking Internal Feedback for LLM Reasoning | — | 2025 | [paper](https://arxiv.org/abs/2506.17219) | (theoretical critique of Verify-Free; omnibus → [Verify-Free RL](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/)) |

### Alignment Classics

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| RLHF | Training language models to follow instructions with human feedback | OpenAI | 2022 | [paper](https://arxiv.org/abs/2203.02155) | [HuggingLLM 1.3.3：RLHF 流程与思想](https://github.com/datawhalechina/hugging-llm/blob/main/docs/chapter1/chapter1.md) |
| RLOO | Back to Basics: Revisiting REINFORCE Style Optimization for RLHF | Cohere | 2024 | [paper](https://arxiv.org/abs/2402.14740) | (derived in [GiGPO](https://yam.gift/2025/07/25/NLP/LLM-Training/2025-07-25-GiGPO/): GRPO with Fnorm=1 ≡ RLOO) |
| ReMax | ReMax: A Simple, Effective, and Efficient RL Method for LLM | CUHK | 2024 | [paper](https://arxiv.org/abs/2310.10505) | (contrasted in [Reinforce++](https://yam.gift/2025/10/24/NLP/LLM-Training/2025-10-24-ReinforcePP/): greedy-baseline variant — inefficient because greedy response is unused for training) |

### MoE RL Stability

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| R3 | Stabilizing MoE RL by Aligning Training and Inference Routers | Xiaomi | 2025 | [paper](https://arxiv.org/abs/2510.11370) | [稳定压倒一切：MoE RL 训推不一致问题及解决策略](https://yam.gift/2026/01/17/NLP/LLM-Training/2026-01-17-RL-MoE-Stable/) |
| IcePop | Small Leak Can Sink a Great Ship — Boost RL Training on MoE | Ant | 2025 | [paper](https://ringtech.notion.site/icepop) | (omnibus → [RL-MoE-Stable](https://yam.gift/2026/01/17/NLP/LLM-Training/2026-01-17-RL-MoE-Stable/)) |
| TIS | Your Efficient RL Framework Secretly Brings You Off-Policy RL Training | UCSD | 2025 | [paper](https://fengyao.notion.site/off-policy-rl) | (omnibus → [RL-MoE-Stable](https://yam.gift/2026/01/17/NLP/LLM-Training/2026-01-17-RL-MoE-Stable/)) |
| KAT | KAT-Coder Tech Report | Kuaishou | 2026 | [blog](https://kwai-kat.github.io/) | [MoE RL 训练不稳定性再思考：训推不一致，还是采样噪声？](https://yam.gift/2026/01/22/NLP/LLM-Training/2026-01-22-RL-MoE-Stable-2/) |

### Agentic RL (Step-Level Credit Assignment)

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| GiGPO | Group-in-Group Policy Optimization for LLM Agent Training | NTU, Skywork AI | 2025 | [paper](https://arxiv.org/abs/2505.10978), [GitHub](https://github.com/langfengQ/verl-agent) | [GiGPO：双层级优势函数驱动的 Agent RL 新范式](https://yam.gift/2025/07/25/NLP/LLM-Training/2025-07-25-GiGPO/) |
| COPO | Think Fast and Slow: Step-Level Cognitive Depth Adaptation for LLM Agents | Tencent | 2026 | [paper](https://arxiv.org/abs/2602.12662), [GitHub](https://github.com/rhyang2021/CogRouter) | [COPO：基于认知模式的 Step-Level Agentic RL 优化](https://yam.gift/2026/04/23/NLP/LLM-Training/2026-04-23-COPO/) |
| GAGPO | Generalized Advantage Grouped Policy Optimization | — | 2026 | [paper](https://arxiv.org/abs/2605.13217) | [GAGPO：如果把GiGPO拉回PPO+GAE](https://yam.gift/2026/05/18/NLP/LLM-Training/2026-05-18-GAGPO/) |
| SVM | Learning Process Rewards via Success Visitation Matching for Efficient RL | — | 2026 | [paper](https://arxiv.org/abs/2606.23640) | [从 SVM 到分布对齐：后训练方法的另一个统一视角](https://yam.gift/2026/07/04/NLP/LLM-Training/2026-07-04-SVM-to-Alignment/) |
| ReTool | Reinforcement Learning for Strategic Tool Use in LLMs | — | 2025 | [paper](https://arxiv.org/abs/2504.11536) | (covered in [指令跟随近期工作梳理](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/): learn when to call a code interpreter and use execution as verification) |

### Instruction Following & Constraint Alignment

> The post-training slice of a broader 35-paper survey: decompose complex instructions, construct verifiable constraints, then optimize with RL or preference data.

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| IF-RL | Incentivizing Reasoning for Advanced Instruction-Following of Large Language Models | — | 2025 | [paper](https://arxiv.org/abs/2506.01413) | [指令跟随近期工作梳理](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/) (decompose multi-constraint instructions, then train with RL and rule-verifiable rewards) |
| VerIF | Verification Engineering for Reinforcement Learning in Instruction Following | — | 2025 | [paper](https://arxiv.org/abs/2506.09942) | (omnibus → [Instruction Following](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/): rules for hard constraints, model judges for semantic constraints) |
| RECAST | Strengthening LLMs' Complex Instruction Following with Constraint-Verifiable Data | — | 2025 | [paper](https://arxiv.org/abs/2505.19030) | (omnibus → [Instruction Following](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/): construct training data around constraints that can actually be checked) |
| MuSC | Improving Complex Instruction Following with Multi-granularity Self-Contrastive Training | — | 2025 | [paper](https://arxiv.org/abs/2502.11541) | (omnibus → [Instruction Following](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/): coarse constraint-aware preferences plus token-level dynamic supervision) |
| IOPO | Empowering LLMs with Complex Instruction Following via Input-Output Preference Optimization | — | 2024 | [paper](https://arxiv.org/abs/2411.06208) | (omnibus → [Instruction Following](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/): preference optimization over matched input-output groups rather than outputs alone) |
| RPO-IF | Reverse Preference Optimization for Complex Instruction Following | — | 2025 | [paper](https://arxiv.org/abs/2505.22172) | (omnibus → [Instruction Following](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/): reverse unmet constraints to synthesize cleaner preference pairs) |

### GRPO Family & Industrial Recipes

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| GRPO | DeepSeekMath: Pushing the Limits of Mathematical Reasoning | DeepSeek | 2024 | [paper](https://arxiv.org/abs/2402.03300) | (covered in [DAPO](https://yam.gift/2025/03/19/NLP/LLM-Training/2025-03-19-LLM-PostTrain-DAPO/) and [R1](https://yam.gift/2025/02/17/NLP/LLM-Training/2025-02-17-DeepSeek-R1/)) |
| DAPO | DAPO: An Open-Source LLM RL System at Scale | ByteDance Seed | 2025 | [paper](https://arxiv.org/abs/2503.14476), [GitHub](https://github.com/BytedTsinghua-SIA/DAPO) | [DAPO：为 GRPO 的锦上加四点花](https://yam.gift/2025/03/19/NLP/LLM-Training/2025-03-19-LLM-PostTrain-DAPO/) |
| Dr.GRPO | Understanding R1-Zero-Like Training: A Critical Perspective | Sea AI Lab | 2025 | [paper](http://arxiv.org/abs/2503.20783), [GitHub](https://github.com/sail-sg/understand-r1-zero) | [异曲同工的 Dr.GRPO](https://yam.gift/2025/03/28/NLP/LLM-Training/2025-03-28-LLM-PostTrain-DrGRPO/) |
| VAPO | VAPO: Efficient and Reliable RL for Advanced Reasoning | ByteDance Seed | 2025 | [paper](https://arxiv.org/abs/2504.05118) | [VAPO：基于价值方法的新突破](https://yam.gift/2025/04/19/NLP/LLM-Training/2025-04-19-VAPO/) |
| CISPO | MiniMax-M1: Scaling Test-Time Compute Efficiently | MiniMax | 2025 | [paper](https://arxiv.org/abs/2506.13585), [GitHub](https://github.com/MiniMax-AI/MiniMax-M1) | [GRPO 优化在继续：CISPO 和熵](https://yam.gift/2025/06/19/NLP/LLM-Training/2025-06-19-CISPO-and-Entropy/) |
| GSPO | Group Sequence Policy Optimization | Qwen | 2025 | [paper](https://arxiv.org/abs/2507.18071) | [Token Level X：DAPO/DrGRPO 与 GSPO/GMPO 的殊途同归](https://yam.gift/2025/08/14/NLP/LLM-Training/2025-08-14-Token-Level-GSPO-GMPO/) |
| GMPO | Geometric-Mean Policy Optimization | UCAS, Microsoft | 2025 | [paper](https://arxiv.org/abs/2507.20673), [GitHub](https://github.com/callsys/GMPO) | (omnibus → [Token-Level-GSPO-GMPO](https://yam.gift/2025/08/14/NLP/LLM-Training/2025-08-14-Token-Level-GSPO-GMPO/)) |
| GTPO | GTPO: Trajectory-Based Policy Optimization in LLMs | — | 2025 | [paper](https://arxiv.org/abs/2508.03772) | [GRPO「第一背锅侠」X2：GTPO 双 T 傍地走](https://yam.gift/2025/08/30/NLP/LLM-Training/2025-08-30-GTPO/) |
| Reinforce++ | REINFORCE++: Stabilizing Critic-Free Policy Optimization | OpenRLHF | 2025 | [paper](https://arxiv.org/abs/2501.03262), [GitHub](https://github.com/OpenRLHF/OpenRLHF) | [Reinforce++ 和它的 KL Loss 选择](https://yam.gift/2025/10/24/NLP/LLM-Training/2025-10-24-ReinforcePP/) |
| KimiRL | Kimi k1.5: Scaling RL with LLMs | Kimi | 2025 | [paper](https://arxiv.org/abs/2501.12599) | (omnibus → [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/)) |
| AGAPO | EXAONE 4.0: Unified LLM Integrating Non-reasoning and Reasoning Modes | LG AI | 2025 | [paper](https://arxiv.org/abs/2507.11407) | (omnibus → [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/)) |
| K-EXAONE | EXAONE-2 Tech Report | LG AI | 2026 | [paper](https://arxiv.org/abs/2601.01739) | (omnibus → [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/)) |
| MOPD | MiMo-V2-Flash Technical Report | Xiaomi | 2026 | [paper](https://arxiv.org/abs/2601.02780) | (omnibus → [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/)) |
| SAPO | Soft Adaptive Policy Optimization | Qwen | 2026 | [paper](https://arxiv.org/abs/2511.20347) | (omnibus → [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/)) |

### Exploration, Advantage & Sampling

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| DCPO | DCPO: Dynamic Clipping Policy Optimization | Baichuan | 2025 | [paper](https://arxiv.org/abs/2509.02333), [GitHub](https://github.com/lime-RL/DCPO) | (described in [GRPO-Clip](https://yam.gift/2025/09/12/NLP/LLM-Training/2025-09-12-GRPO-Clip/): adaptive clip bounds based on token prior probability — expanding exploration room for low-probability tokens) |
| JustGRPO | The Flexibility Trap: Why Arbitrary Order Limits Reasoning Potential in Diffusion Language Models | — | 2026 | [paper](https://arxiv.org/abs/2601.15165) | [DLM 的 RL 后训练：灵活性陷阱](https://yam.gift/2026/03/01/NLP/LLM/2026-03-01-DLM/#RL-Post-Train) (arbitrary order avoids high-entropy branch points; train DLM autoregressively, retain parallel decoding at inference) |
| SIS | Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment | RUC, JD | 2026 | [paper](https://arxiv.org/abs/2607.04728) | [SIS：不硬clip，大部分token其实可转为on-policy](https://yam.gift/2026/07/13/NLP/LLM-Training/2026-07-13-SIS/) |
| Pass@k Training | Pass@k Training for Adaptively Balancing Exploration and Exploitation | ByteDance Seed, RUC | 2025 | [paper](https://arxiv.org/abs/2508.10751) | [从Pass@k到advantage，一场意想不到的邂逅](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/) |
| AAPO | AAPO: Enhancing Reasoning with Advantage Margin | — | 2025 | [paper](https://arxiv.org/abs/2505.14264) | (omnibus → [PassK-Training](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/): frozen-reference margin keeps gradient alive when GRPO advantage → 0) |
| ProGRPO | Back to Basics: Revisiting Exploration via Generative Probabilities | — | 2026 | [paper](https://arxiv.org/abs/2602.05281) | (omnibus → [PassK-Training](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/): advantage bias = difficulty × generative confidence, 2-D correction) |
| GRPOEA | Reasoning with Exploration: An Entropy Perspective | — | 2025 | [paper](https://arxiv.org/abs/2506.14758) | (first in [CISPO-and-Entropy](https://yam.gift/2025/06/19/NLP/LLM-Training/2025-06-19-CISPO-and-Entropy/): add a clipped, stop-grad entropy term straight onto advantage; revisited in [PassK-Training](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/)) |
| EMPG | Entropy-Modulated Policy Gradients for Long-Horizon LLM Agents | — | 2025 | [paper](https://arxiv.org/abs/2509.09265) | (omnibus → [PassK-Training](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/): multiplicative entropy gate g(H) — amplify confident steps, damp uncertain ones) |
| BAPO | BAPO: Balanced Policy Optimization with Adaptive Clipping | — | 2025 | [paper](https://arxiv.org/abs/2510.18927) | (omnibus → [PassK-Training](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/): negatives dominate the gradient & clip blocks entropy-raising updates → adaptive c_high/c_low) |
| ASPO | When Importance Sampling Misallocates Credit: Asymmetric Ratios | — | 2025 | [paper](https://arxiv.org/abs/2510.06062) | (omnibus → [PassK-Training](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/): flip the IS ratio for positive tokens only — low-prob key tokens finally get strong updates) |
| Pass@K PO | Pass@K Policy Optimization: Solving Harder RL Problems | DeepMind | 2025 | [paper](https://arxiv.org/abs/2505.15201) | *to-write* (low-variance unbiased pass@k gradient estimator — the proof-heavy companion to Pass@k Training) |
| OPO | On-Policy RL with Optimal Reward Baseline | Microsoft | 2025 | [paper](https://arxiv.org/abs/2505.23585) | (described in [Token-Level-GSPO-GMPO](https://yam.gift/2025/08/14/NLP/LLM-Training/2025-08-14-Token-Level-GSPO-GMPO/): optimal reward baseline minimizes gradient variance; contrasted in [GTPO](https://yam.gift/2025/08/30/NLP/LLM-Training/2025-08-30-GTPO/): focuses on advantage/reward level rather than token level) |
| SRPO | SRPO: Cross-Domain Implementation of Large-Scale RL on LLM | Kuaishou | 2025 | [paper](https://arxiv.org/abs/2504.14286), [HF](https://huggingface.co/Kwaipilot/SRPO-Qwen-32B) | (contrasted in [Token-Level-GSPO-GMPO](https://yam.gift/2025/08/14/NLP/LLM-Training/2025-08-14-Token-Level-GSPO-GMPO/): historical resampling retains key samples to improve sample efficiency) |

### Policy Optimization Foundations

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| DPO | Direct Preference Optimization | Stanford | 2024 | [paper](https://arxiv.org/abs/2305.18290) | (compared inside [DPO-Data](https://yam.gift/2025/03/02/NLP/LLM-Training/2025-03-02-LLM-PostTrain-DPO-Data/)) |
| TRPO | Trust Region Policy Optimization | Berkeley | 2015 | [paper](https://arxiv.org/abs/1502.05477) | [TRPO深度拆解：为什么做后训练应该读懂TRPO](https://yam.gift/2026/05/11/NLP/LLM-Training/2026-05-11-TRPO/) |
| FiberPO | FiberPO (vanishing theorem & δ-relaxation) | — | 2026 | — | [为什么TRPO在LLM里不能用？——FiberPO的起点](https://yam.gift/2026/06/22/NLP/LLM-Training/2026-06-22-TRPO-Vanishing/) (series part 1) |
| PPO | Proximal Policy Optimization Algorithms | OpenAI | 2017 | [paper](https://arxiv.org/abs/1707.06347) | (extended in [VAPO](https://yam.gift/2025/04/19/NLP/LLM-Training/2025-04-19-VAPO/): Value-based Augmented PPO with GAE refinements / value-pretraining; contrasted in [Reinforce++](https://yam.gift/2025/10/24/NLP/LLM-Training/2025-10-24-ReinforcePP/): PPO with critic vs critic-free Reinforce-style) |
| REINFORCE | Simple Statistical Gradient-Following Algorithms | Northeastern | 1992 | [paper](https://people.cs.umass.edu/~barto/courses/cs687/williams92simple.pdf) | (extended in [CISPO](https://yam.gift/2025/06/19/NLP/LLM-Training/2025-06-19-CISPO-and-Entropy/): REINFORCE + IS → CISPO loss; framed in [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/): REINFORCE-with-baseline as analytic frame for all GRPO variants) |

### Pre-R1 Foundations (Historical Anchors)

> Pre-R1 RL × NLP works the author considers personally important. Kept here for sentimental and historical reasons rather than as active reading. Includes the *final days* of the pre-R1 era — PRIME and rStar-Math shipped in early January 2025, and R1 (Jan 20) buried their lines within weeks. The author's full reflection: [《通向 AGI 的技术路径：多模态、强化学习与新架构的交汇点》](https://yam.gift/2026/01/25/AI/2026-01-25-AI-Future-Framework/) — *"22 年 RL4LMs 出来后我兴奋的晚上觉都没睡着，第一时间就读了他们的代码。"*

| Abbr | Title | From | Year | Link | Note |
|------|-------|------|------|------|------|
| RL4LMs / NLPO | RL (Not) for NLP: Benchmarks, Baselines, Building Blocks | Allen | 2022 | [paper](http://arxiv.org/abs/2210.01241), [GitHub](https://github.com/allenai/rl4lms) | Personally cited milestone in [AI-Future-Framework](https://yam.gift/2026/01/25/AI/2026-01-25-AI-Future-Framework/) — first felt RL × NLP could really land |
| FTHP | Fine-Tuning Language Models from Human Preferences | OpenAI | 2020 | [paper](http://arxiv.org/abs/1909.08593), [GitHub](https://github.com/openai/lm-human-preferences) | OpenAI's earliest RLHF experiment; the seed of InstructGPT/ChatGPT |
| Quark | Quark: Controllable Text Generation with Reinforced [Un]learning | Allen | 2022 | [paper](http://arxiv.org/abs/2205.13636), [GitHub](https://github.com/GXimingLu/Quark) | Early attempt at RL for controllable generation × unlearning — niche but conceptually clean |
| DT | Decision Transformer: RL via Sequence Modeling | Berkeley | 2021 | [paper](https://arxiv.org/abs/2106.01345), [GitHub](https://github.com/kzl/decision-transformer) | The "RL = sequence modeling" reframing — a parallel branch that diverged from the LLM-RL trunk |
| rStar | rStar: Mutual Reasoning Makes Smaller LLMs Stronger | Microsoft | 2024 | [paper](https://arxiv.org/pdf/2408.06195), [GitHub](https://github.com/zhentingqi/rStar) | High-water mark of the MCTS + SLM mutual-reasoning line — conceptually clean, ended by R1 along with the rest of the search-based branch |
| rStar-Math | rStar-Math: Small LLMs Can Master Math Reasoning | Microsoft | 2025 | [paper](https://arxiv.org/abs/2501.04519), [GitHub](https://github.com/microsoft/rStar) | Shipped 12 days before R1 — the MCTS+PRM line's peak, instantly buried. The author had a blog half-written when R1 landed: a genuinely good paper born in the wrong era; (described in [R1-New-Paradigm](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/): rule-based verification on intermediate results via Python execution) |
| PRIME | Process Reinforcement through Implicit Rewards | PRIME-RL | 2025 | [paper](https://curvy-check-498.notion.site/Process-Reinforcement-through-Implicit-Rewards-15f4fcb9c42180f1b498cc9b2eaf896f), [GitHub](https://github.com/PRIME-RL/PRIME) | Implicit PRM (trained as ORM, used as PRM) — the line died with R1, though process reward itself returned later as Track 07's dense rewards; (described in [R1-New-Paradigm](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/)) |

### Frontier RL — Boundary, Process Reward & Experience

> Pure RL frontier: where the *training* loop itself is being pushed (boundary, process reward, experience-as-data, planning-as-data).

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| DeepSeek-V3.2 Post-train | DeepSeek-V3.2 Tech Report | DeepSeek | 2025 | [paper](https://github.com/deepseek-ai/DeepSeek-V3) | [DeepSeek V3.2 后训练：稳定压倒一切](https://yam.gift/2025/12/03/NLP/LLM-Training/2025-12-03-DeepSeek-V32-PostTraining/) |
| RL Boundary (Yue) | Does RL Really Incentivize Reasoning Capacity Beyond the Base Model? | — | 2025 | [paper](https://arxiv.org/abs/2504.13837) | [RL 究竟能不能突破 Base 边界](https://yam.gift/2025/12/31/NLP/LLM-Training/2025-12-31-RL-Are-You-OK/) |
| Invisible Leash | Invisible Leash | Wu et al. | 2025 | [paper](https://arxiv.org/abs/2507.14843) | (omnibus → [RL-Are-You-OK](https://yam.gift/2025/12/31/NLP/LLM-Training/2025-12-31-RL-Are-You-OK/)) |
| ProRL | ProRL: Prolonged RL Expands Reasoning Boundaries | NVIDIA | 2025 | [paper](https://arxiv.org/abs/2505.24864) | (omnibus → [RL-Are-You-OK](https://yam.gift/2025/12/31/NLP/LLM-Training/2025-12-31-RL-Are-You-OK/)) |
| DELTA | DELTA: Dense Process Reward for RL Boundary Extrapolation | — | 2025 | — | (omnibus → [RL-Are-You-OK](https://yam.gift/2025/12/31/NLP/LLM-Training/2025-12-31-RL-Are-You-OK/)) |
| ERL | Experience-as-RL | — | 2026 | [paper](https://arxiv.org/abs/2602.13949) | [RL 新范式：从经验到更高质量数据](https://yam.gift/2026/03/29/NLP/LLM-Training/2026-03-29-RL-New-Paradigm-Data/) |
| MR-Search | MR-Search: Meta-Reasoning Search | — | 2026 | [paper](https://arxiv.org/abs/2603.11327) | (omnibus → [RL-New-Paradigm-Data](https://yam.gift/2026/03/29/NLP/LLM-Training/2026-03-29-RL-New-Paradigm-Data/)) |
| OEL | Open-Ended Learning | — | 2026 | [paper](https://arxiv.org/abs/2603.16856) | (omnibus → [RL-New-Paradigm-Data](https://yam.gift/2026/03/29/NLP/LLM-Training/2026-03-29-RL-New-Paradigm-Data/)) |
| LEPA | LEPA: Learn to Plan before Answering | — | 2025 | [paper](https://arxiv.org/abs/2505.00031) | [从「会答」到「会想」：Planning as Data 与思考范式重构](https://yam.gift/2026/04/17/NLP/LLM-Training/2026-04-17-Think-Strategy/) |
| Self-Steering | Self-Steering | — | 2025 | [paper](https://arxiv.org/abs/2504.07081) | (omnibus → [Think-Strategy](https://yam.gift/2026/04/17/NLP/LLM-Training/2026-04-17-Think-Strategy/)) |

### SFT × RL Interplay

> SFT as a special case of RL, forgetting dynamics, unified post-training theory.

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| GFT | From Imitation to Reward Fine-Tuning with Unbiased Group Advantages | — | 2026 | [paper](https://arxiv.org/abs/2604.14258) | [你可能没那么懂 SFT：SFT 与 RL 的爱恨纠葛](https://yam.gift/2026/06/01/NLP/LLM-Training/2026-06-01-SFT-vs-RL/) |
| HPT | Towards a Unified View of Large Language Model Post-Training | — | 2025 | [paper](https://arxiv.org/abs/2509.04419) | (omnibus → [SFT-vs-RL](https://yam.gift/2026/06/01/NLP/LLM-Training/2026-06-01-SFT-vs-RL/)) |
| RL's Razor | Why Online Reinforcement Learning Forgets Less | — | 2025 | [paper](https://arxiv.org/abs/2509.04259) | (omnibus → [SFT-vs-RL](https://yam.gift/2026/06/01/NLP/LLM-Training/2026-06-01-SFT-vs-RL/)) |
| Conditional SFT | Rethinking Generalization in Reasoning SFT | — | 2026 | [paper](https://arxiv.org/abs/2604.06628) | (omnibus → [SFT-vs-RL](https://yam.gift/2026/06/01/NLP/LLM-Training/2026-06-01-SFT-vs-RL/)) |
| MiniLLM | MiniLLM: Knowledge Distillation of Large Language Models | THU, MSR | 2023 | [paper](https://arxiv.org/abs/2306.08543) | (described in [Open-LLM-RL-ShowCase](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/): forward vs reverse KL in distillation; connected in [SVM-to-Alignment](https://yam.gift/2026/07/04/NLP/LLM-Training/2026-07-04-SVM-to-Alignment/): reverse-KL distillation sits on the same mode-seeking axis as RL/DPO) |

### On-Policy Distillation & Policy-Diff Learning

> Not every work below is RL. They belong together because policy diff is the shared training signal: it first reconstructs or extrapolates a target, then crosses into RL as an implicit reward or a transformation of verifier gradients.

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| W2S-OPD | Weak-to-Strong On-Policy Distillation | Microsoft | 2026 | [paper](https://arxiv.org/abs/2607.26246) | [「差值即信号」：OPD 蒸馏的新范式](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/) |
| Lightning OPD 2.0 | Mitigating Style Bias in Cross-Teacher On-Policy Distillation | MIT | 2026 | [paper](https://arxiv.org/abs/2607.28449) | (omnibus → [OPD-Diff-is-Signal](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/): subtract cross-fitted style bias so the residual better isolates problem-specific reasoning signal) |
| VAD | Attributing Visual Evidence for Target Reconstruction in Multimodal OPD | Xiaohongshu | 2026 | [paper](https://arxiv.org/abs/2607.28590) | (omnibus → [OPD-Diff-is-Signal](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/): project teacher correction onto the counterfactual visual-evidence direction) |
| RP-OPSD | Resolution-Privileged On-Policy Self-Distillation for MLLMs | USTC | 2026 | [paper](https://arxiv.org/abs/2607.24447) | (omnibus → [OPD-Diff-is-Signal](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/): resolution supplies privileged information without external models or annotations) |
| STEP-OPD | Rethinking Output Targets and Internal Dynamics in OPD for Diffusion Models | Alibaba | 2026 | [paper](https://arxiv.org/abs/2608.04887) | (omnibus → [OPD-Diff-is-Signal](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/): extrapolate the teacher-minus-base capability direction beyond the teacher) |
| Poly-OPD | Heterogeneous Multi-Teacher OPD for Capability-Selectable Flow Models | JD Joy | 2026 | [paper](https://arxiv.org/abs/2608.04349) | (omnibus → [OPD-Diff-is-Signal](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/): allocate training budget by the remaining teacher–student capability gap) |
| Direct-OPD | Weak-to-Strong Generalization via Direct On-Policy Distillation | Tsinghua, ByteDance | 2026 | [paper](https://arxiv.org/abs/2607.05394) | [OPD-RL 新范式：diff 出圈](https://yam.gift/2026/10/15/NLP/LLM-Training/2026-10-15-OPD-RL-New-Paradigm/) |
| RG-OPD | Reward-Gated On-Policy Distillation | — | 2026 | [paper](https://arxiv.org/abs/2607.04037) | (contrasted in [OPD-RL](https://yam.gift/2026/10/15/NLP/LLM-Training/2026-10-15-OPD-RL-New-Paradigm/): reward gates trajectories whose teacher–student likelihood gap agrees with advantage) |
| OPRD | Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation | — | 2026 | [paper](https://arxiv.org/abs/2609.08798) | (derived in [OPD-RL](https://yam.gift/2026/10/15/NLP/LLM-Training/2026-10-15-OPD-RL-New-Paradigm/): project verifier gradients onto the teacher-diff direction and amplify that component without introducing new stationary points) |
| Beyond Teacher | Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation | — | 2026 | [paper](https://arxiv.org/abs/2602.12125) | (connected in [OPD-RL](https://yam.gift/2026/10/15/NLP/LLM-Training/2026-10-15-OPD-RL-New-Paradigm/): OPD is a special case of dense KL-regularized RL) |
| OPDD | On-Policy Delta Distillation | — | 2026 | [paper](https://arxiv.org/abs/2607.15161) | (connected in [OPD-RL](https://yam.gift/2026/10/15/NLP/LLM-Training/2026-10-15-OPD-RL-New-Paradigm/): policy delta used directly as a dense reward) |

### Beyond RL — Training-Free / Behavior Shaping / Real-time PEFT

> *Post-RL* directions covered in the same blogs. The paradigm is moving away from classical RL training, into context, behavior, and parameter-efficient adaptation. They are not RL by the textbook definition, but they share the same goal — shape model behavior — and several of them (Activation Steering, Context Engineering) are the **upstream signals** that Training-Free RL only later named explicitly.

| Abbr | Title | From | Year | Link | My Notes |
|------|-------|------|------|------|----------|
| TRT | Test-time Recursive Thinking: Self-Improvement without External Feedback | Microsoft | 2026 | [paper](https://arxiv.org/abs/2602.03094) | [Training-Free RL：当训练不再更新参数，而是更新上下文](https://yam.gift/2026/03/24/NLP/LLM-Training/2026-03-24-RL-New-Paradigm-Traning-Free/) |
| Training-Free GRPO | Training-Free Group Relative Policy Optimization | — | 2025 | [paper](https://arxiv.org/abs/2510.08191) | (omnibus → [Training-Free RL](https://yam.gift/2026/03/24/NLP/LLM-Training/2026-03-24-RL-New-Paradigm-Traning-Free/)) |
| MemAPO | MemAPO: Memory-Augmented Policy Optimization | — | 2026 | [paper](https://arxiv.org/abs/2603.21520) | (omnibus → [Training-Free RL](https://yam.gift/2026/03/24/NLP/LLM-Training/2026-03-24-RL-New-Paradigm-Traning-Free/)) |
| Update-Free Steering | Update-Free On-Policy Steering via Verifiers | — | 2026 | [paper](https://arxiv.org/abs/2603.10282) | (omnibus → [Training-Free RL](https://yam.gift/2026/03/24/NLP/LLM-Training/2026-03-24-RL-New-Paradigm-Traning-Free/)) |
| Activation Engineering | Steering Language Models With Activation Engineering | — | 2023 | [paper](https://arxiv.org/abs/2308.10248) | [激活诱导 LLM 指令跟随](https://yam.gift/2025/07/01/NLP/LLM-IF/2025-07-01-Activation-Steering/) |
| Activation Steering (IF) | Improving Instruction-Following in Language Models through Activation Steering | Microsoft | 2024 | [paper](https://arxiv.org/abs/2410.12877) | (omnibus → [激活诱导 LLM 指令跟随](https://yam.gift/2025/07/01/NLP/LLM-IF/2025-07-01-Activation-Steering/)) |
| Context Engineering | Context Engineering for AI Agents: Lessons from Building Manus | Manus | 2025 | [blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | [重识 LLM 法则：上下文工程与数据进化](https://yam.gift/2025/07/27/NLP/LLM-Context/2025-07-27-Context-Engineering-and-Data/) |
| MiCA | MiCA: Minor-Component Adaptation | — | 2026 | [paper](https://arxiv.org/abs/2604.01694) | [实时学习：极致高效的子空间微调](https://yam.gift/2026/04/11/NLP/LLM-Training/2026-04-11-Real-time-Learning-from-PEFT/) |
| TinyLoRA | TinyLoRA | — | 2026 | — | (omnibus → [Real-time-Learning-from-PEFT](https://yam.gift/2026/04/11/NLP/LLM-Training/2026-04-11-Real-time-Learning-from-PEFT/)) |

---

## Chronological Blog Timeline

All blog posts in publishing order, with the author's one-sentence takeaway. Use this when you want to *follow the narrative arc* rather than search by paper.

| Date | Track | Blog (Chinese) | One-sentence takeaway |
|------|-------|----------------|------------------------|
| 2025-02-17 | 01 | [DeepSeek R1 深度技术解析及其影响](https://yam.gift/2025/02/17/NLP/LLM-Training/2025-02-17-DeepSeek-R1/) | Data sets the ceiling, algorithms approach it; pure rule-based RL works. |
| 2025-02-18 | 01 | [少量高质量数据 SFT 激活推理](https://yam.gift/2025/02/18/NLP/LLM-Training/2025-02-18-LLM-PostTrain-SFT-Data/) | LIMO/s1: small high-quality SFT *activates* reasoning, doesn't *teach* it. |
| 2025-02-27 | 01 | [R1 相关：RL 数据选择与 Scaling](https://yam.gift/2025/02/27/NLP/LLM-Training/2025-02-27-LLM-PostTrain-PPO-Data/) | LIMR/ORZ: less-is-more applies to RL data, not just SFT. |
| 2025-03-02 | 01 | [R1 相关：DPO 数据选择与 DPO 等 RL 算法](https://yam.gift/2025/03/02/NLP/LLM-Training/2025-03-02-LLM-PostTrain-DPO-Data/) | Online-DPO can rival PPO when paired with the right data pipeline. |
| 2025-03-15 | 01 | [DeepSeek R1 后 LLM 新范式](https://yam.gift/2025/03/15/NLP/LLM-Training/2025-03-15-R1-New-Paradigm/) | The post-R1 path forks into multiple parallel lines (length, scaling, MRT, …). |
| 2025-03-19 | 02 | [DAPO：为 GRPO 的锦上加四点花](https://yam.gift/2025/03/19/NLP/LLM-Training/2025-03-19-LLM-PostTrain-DAPO/) | DAPO = Clip-Higher + Dynamic Sampling + Token-Level Loss + Overlong Reward Shaping. |
| 2025-03-28 | 02 | [异曲同工的 Dr.GRPO](https://yam.gift/2025/03/28/NLP/LLM-Training/2025-03-28-LLM-PostTrain-DrGRPO/) | Dr.GRPO removes the length & std normalization biases hidden in vanilla GRPO. |
| 2025-04-10 | 01 | [R1-Zero 的进一步理解和探索](https://yam.gift/2025/04/10/NLP/LLM-Training/2025-04-10-Think-More-about-R1-Zero/) | R1-Zero behavior depends heavily on base model; "Aha moment" is partly base-pretrain artifact. |
| 2025-04-19 | 02 | [VAPO：基于价值方法的新突破](https://yam.gift/2025/04/19/NLP/LLM-Training/2025-04-19-VAPO/) | Value-based methods come back to compete with critic-free GRPO. |
| 2025-04-26 | 01 | [Yarz-Logic：R1-Zero 相关实验报告](https://yam.gift/2025/04/26/NLP/LLM-Training/2025-04-26-R1-Zero-Lab-Yarz-Logic/) | Hands-on Logic-RL replication: where R1-Zero's edges are in practice. |
| 2025-05-01 | 01 | [R1 后范式最佳实践：Seed-Thinking 和 Qwen3](https://yam.gift/2025/05/01/NLP/LLM-Training/2025-05-01-Seed-Thinking-Qwen3/) | Seed-Thinking + Qwen3 are the two most complete industrial post-R1 recipes. |
| 2025-06-09 | 03 | [Reward Model 建模](https://yam.gift/2025/06/09/NLP/LLM-Training/2025-06-09-RM-Modeling/) | General-domain RM needs principles+critique, not a single scalar (DeepSeek-GRM). |
| 2025-06-19 | 02 | [GRPO 优化在继续：CISPO 和熵](https://yam.gift/2025/06/19/NLP/LLM-Training/2025-06-19-CISPO-and-Entropy/) | CISPO shows clip is not just stability — it shapes the explore/exploit edge. |
| 2025-06-26 | 05 | [指令跟随近期工作梳理（2025 年上半年）](https://yam.gift/2025/06/26/NLP/LLM-IF/2025-06-26-Instruction-Following/) | Complex instruction following becomes post-training once constraints are decomposed into verifiable rewards or preference pairs. |
| 2025-07-01 | 05 | [激活诱导 LLM 指令跟随](https://yam.gift/2025/07/01/NLP/LLM-IF/2025-07-01-Activation-Steering/) | Activation Steering: behavior shaping without weight updates — the prequel to Update-Free Steering. |
| 2025-07-13 | 03 | [Reward 数据如何塑造与激发推理策略](https://yam.gift/2025/07/13/NLP/LLM-Training/2025-07-13-RM-Data/) | Good reward data unlocks pre-existing strategies; even spurious rewards can do this. |
| 2025-07-25 | 07 | [GiGPO：双层级优势函数驱动的 Agent RL 新范式](https://yam.gift/2025/07/25/NLP/LLM-Training/2025-07-25-GiGPO/) | Agent RL needs hierarchical (group-in-group) advantages for proper credit assignment. |
| 2025-07-27 | 05 | [重识 LLM 法则：上下文工程与数据进化](https://yam.gift/2025/07/27/NLP/LLM-Context/2025-07-27-Context-Engineering-and-Data/) | "Everything is context" — the early manifesto behind Training-Free RL. |
| 2025-08-14 | 02 | [Token Level X：DAPO/DrGRPO 与 GSPO/GMPO 的殊途同归](https://yam.gift/2025/08/14/NLP/LLM-Training/2025-08-14-Token-Level-GSPO-GMPO/) | Token-level vs sequence-level is THE axis of the GRPO family. |
| 2025-08-30 | 02 | [GRPO「第一背锅侠」X2：GTPO 双 T 傍地走](https://yam.gift/2025/08/30/NLP/LLM-Training/2025-08-30-GTPO/) | GTPO: trajectory-level view exposes more of GRPO's hidden assumptions. |
| 2025-09-12 | 02 | [GRPO「又一背锅侠」：Clip 的各种拉扯](https://yam.gift/2025/09/12/NLP/LLM-Training/2025-09-12-GRPO-Clip/) | Side-by-side: Clip-Higher vs Clip-Wider vs Spurious Rewards on the same axis. |
| 2025-10-24 | 02 | [Reinforce++ 和它的 KL Loss 选择](https://yam.gift/2025/10/24/NLP/LLM-Training/2025-10-24-ReinforcePP/) | KL Loss choice (k2 vs k3) matters more than usually credited. |
| 2025-11-11 | 03 | [无验证器 RL 与 Reference 的妙用](https://yam.gift/2025/11/11/NLP/LLM-Training/2025-11-11-RM-New-Paradigm-Verifier-Free-RL/) | Without verifiers, use PPL / reference-likelihood / reverse-self-eval as proxies. |
| 2025-11-29 | 03 | [DeepSeekMath-V2 自我验证：搞数据的风吹到了 RM](https://yam.gift/2025/11/29/NLP/LLM-Training/2025-11-29-Reward-Data-Self-Verified/) | Reward should model "where the answer is wrong"; generation ↔ verification co-evolve. |
| 2025-12-03 | 02 | [DeepSeek V3.2 后训练：稳定压倒一切](https://yam.gift/2025/12/03/NLP/LLM-Training/2025-12-03-DeepSeek-V32-PostTraining/) | Industry's MoE post-train recipe: stability above all else. |
| 2025-12-21 | 03 | [无验证 RL——当模型只能相信自己](https://yam.gift/2025/12/21/NLP/LLM-Training/2025-12-21-RM-New-Paradigm-Verify-Free-RL/) | All internal-feedback methods compress entropy → exploration crisis sooner or later. |
| 2025-12-31 | 05 | [RL 究竟能不能突破 Base 边界](https://yam.gift/2025/12/31/NLP/LLM-Training/2025-12-31-RL-Are-You-OK/) | Most RL is sampling polish; true extrapolation needs edge data + process reward. |
| 2026-01-14 | 02 | [LLM 强化的「炼金术」：主流开源模型的 RL 优化策略赏析](https://yam.gift/2026/01/14/NLP/LLM-Training/2026-01-14-Open-LLM-RL-ShowCase/) | 5 industrial GRPO variants (Kimi/EXAONE/MiMo/MiniMax/Qwen) compared side-by-side — every team is patching the same holes. |
| 2026-01-17 | 04 | [稳定压倒一切：MoE RL 训推不一致问题及解决策略](https://yam.gift/2026/01/17/NLP/LLM-Training/2026-01-17-RL-MoE-Stable/) | Train-infer router mismatch is the surface; R3 / IcePop / TIS each take a different angle. |
| 2026-01-22 | 04 | [MoE RL 训练不稳定性再思考：训推不一致，还是采样噪声？](https://yam.gift/2026/01/22/NLP/LLM-Training/2026-01-22-RL-MoE-Stable-2/) | Even *recomputing* logprobs on MoE drifts; the deeper cause is sampling noise, not routing. |
| 2026-03-01 | 02 | [DLM 的 RL 后训练：灵活性陷阱](https://yam.gift/2026/03/01/NLP/LLM/2026-03-01-DLM/#RL-Post-Train) | Arbitrary generation order can suppress exploration by deferring high-entropy choices; JustGRPO makes training autoregressive while preserving parallel inference. |
| 2026-03-24 | 05 | [Training-Free RL：当训练不再更新参数，而是更新上下文](https://yam.gift/2026/03/24/NLP/LLM-Training/2026-03-24-RL-New-Paradigm-Traning-Free/) | Advantage in text/context, not in weight space — fixed model can still "RL". |
| 2026-03-29 | 05 | [RL 新范式：从经验到更高质量数据](https://yam.gift/2026/03/29/NLP/LLM-Training/2026-03-29-RL-New-Paradigm-Data/) | The loop becomes "trajectory → information gain → re-supervision". |
| 2026-04-11 | 05 | [实时学习：极致高效的子空间微调](https://yam.gift/2026/04/11/NLP/LLM-Training/2026-04-11-Real-time-Learning-from-PEFT/) | MiCA/TinyLoRA: pluggable real-time learning by occupying the *minor* singular directions. |
| 2026-04-17 | 05 | [从「会答」到「会想」：Planning as Data 与思考范式重构](https://yam.gift/2026/04/17/NLP/LLM-Training/2026-04-17-Think-Strategy/) | Reasoning becomes a *data format*; the next battle is how to construct planning data. |
| 2026-04-23 | 07 | [COPO：基于认知模式的 Step-Level Agentic RL 优化](https://yam.gift/2026/04/23/NLP/LLM-Training/2026-04-23-COPO/) | Step-level cognitive advantage reweighting — GRPO should not treat all steps equally in agentic tasks. |
| 2026-05-11 | 02 | [TRPO深度拆解：为什么做后训练应该读懂TRPO](https://yam.gift/2026/05/11/NLP/LLM-Training/2026-05-11-TRPO/) | TRPO is the theoretical bedrock of PPO and GRPO — IS + Trust Region + Advantage are the three pillars. |
| 2026-05-18 | 07 | [GAGPO：如果把GiGPO拉回PPO+GAE](https://yam.gift/2026/05/18/NLP/LLM-Training/2026-05-18-GAGPO/) | Critic-free Agentic RL: use GRPO's grouping to estimate V, then GAE for per-step advantage. |
| 2026-06-01 | 06 | [你可能没那么懂 SFT：SFT 与 RL 的爱恨纠葛](https://yam.gift/2026/06/01/NLP/LLM-Training/2026-06-01-SFT-vs-RL/) | SFT is a special case of RL; the question is "which layer is activating vs. memorizing?" |
| 2026-06-22 | 02 | [为什么TRPO在LLM里不能用？——FiberPO的起点](https://yam.gift/2026/06/22/NLP/LLM-Training/2026-06-22-TRPO-Vanishing/) | γ must be 1 in LLM RL → TRPO trust region vanishes to zero; PPO/GRPO clip is empirical δ-relaxation. |
| 2026-07-04 | 06 | [从 SVM 到分布对齐：后训练方法的另一个统一视角](https://yam.gift/2026/07/04/NLP/LLM-Training/2026-07-04-SVM-to-Alignment/) | SVM/DPO/RLHF/SFT are all distribution alignment — differing in anchor count, KL direction, and anchor observability. |
| 2026-07-13 | 02 | [SIS：不硬clip，大部分token其实可转为on-policy](https://yam.gift/2026/07/13/NLP/LLM-Training/2026-07-13-SIS/) | Rejection sampling turns most off-policy tokens on-policy — keep the gradient signal instead of clipping it; provably tighter error bound (D_SIS ≤ D). |
| 2026-08-11 | 06 | [「差值即信号」：OPD 蒸馏的新范式](https://yam.gift/2026/08/11/NLP/LLM-Training/2026-08-11-OPD-Diff-is-Signal/) | Distill the teacher's capability direction, not its raw output: counterfactual policy differences can reconstruct targets, extrapolate beyond teachers, and drive capability-aware curricula. |
| 2026-08-26 | 03 | [Reward 设计的本质：从 hack 到 hard](https://yam.gift/2026/08/26/AI/2026-08-26-Reward-Design-Philosophy/) | Reward is a lossy compression of preference; reward hack is structural, not a bug — treat reward as a prior to revise, not ground truth. |
| 2026-09-11 | 02 | [从Pass@k到advantage，一场意想不到的邂逅](https://yam.gift/2026/09/11/NLP/LLM-Training/2026-09-11-PassK-Training/) | Pass@k training = dynamically weakening negative-advantage by global correct-count; converges to the whole 2025-H2 advantage-shaping red ocean (AAPO/ProGRPO/GRPOEA/EMPG/BAPO/ASPO). |
| 2026-10-15 | 06 | [OPD-RL 新范式：diff 出圈——从目标，到奖励，再到梯度](https://yam.gift/2026/10/15/NLP/LLM-Training/2026-10-15-OPD-RL-New-Paradigm/) | A teacher's policy diff can reconstruct a target, act as an implicit dense reward, or recondition verifier gradients — distillation and RL meet through the same directional signal. |

---

## Appendix

### Maintenance

The index is deliberately hand-curated. Run `python3 scripts/check_readme.py` before pushing; CI reports the current totals and verifies table shape, timeline order, and duplicate blog links.

### Library

| GitHub | From | Year | Description |
|--------|------|------|-------------|
| [prime-rl](https://github.com/PrimeIntellect-ai/prime-rl) | PrimeIntellect-ai | 2025 | Decentralized large-scale RL training framework |
| [PRIME](https://github.com/PRIME-RL/PRIME) | PRIME-RL | 2025 | Scalable RL recipe for reasoning |
| [rStar](https://github.com/microsoft/rStar) | Microsoft | 2025 | Self-evolved deep reasoning for SLMs |
| [veRL](https://github.com/volcengine/verl) | ByteDance | 2024 | LLM RL training framework (Volcano Engine) |
| [trl](https://github.com/huggingface/trl) | HuggingFace | 2024 | Train language models with RL |
| [RL4LMs](https://github.com/allenai/RL4LMs) | Allen | 2023 | Aligning LMs to human preference via RL |
| [alignment-handbook](https://github.com/huggingface/alignment-handbook) | HuggingFace | 2023 | Recipes for aligning to human/AI preference |

### Citation / Feedback

If this index or the linked blog posts are useful, leave a note on [GitHub Issues](https://github.com/hscspring/llm-post-training-atlas/issues), or cite [yam.gift](https://yam.gift) when referencing.

> "Don't chase the wind — chase the long view; measure one year by the yardstick of ten." — 长琴
