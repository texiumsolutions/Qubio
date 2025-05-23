Finetuning for Molecular Optimization
=====================================

Overview
--------

Finetuning in computational biology refers to adapting general-purpose models or algorithms for specific molecular tasks—such as drug optimization, protein engineering, or synthetic route planning—using domain-specific data. It is a powerful method to improve accuracy, efficiency, or target-specificity of AI models in bio/cheminformatics pipelines.

Why Finetuning Matters
----------------------

- 🔬 Specialization: General models can be tailored to focus on specific properties like solubility, toxicity, or binding affinity.
- 💡 Low Data Regimes: Enables transfer learning on small datasets.
- 🧪 Experimental Efficiency: Reduces the number of wet-lab experiments by optimizing in silico.
- 🧬 Personalized Molecule Design: Useful in precision medicine and adaptive drug development.

In Qubio, the concept of finetuning is applied not in the traditional deep learning sense alone, but also in probabilistic exploration of design spaces—e.g., reaction optimization or compound selection.

Finetuning Tools in Qubio
-------------------------

Qubio currently supports the following tools that fall under the broad umbrella of "finetuning" or intelligent sampling/optimization of chemical design space:

1. Thompson Sampling
   ^^^^^^^^^^^^^^^^^^^

   - **Endpoint:** ``/v1/api/thompson_sampling/run_ts``
   - **Description:** Thompson Sampling is a Bayesian optimization strategy that helps select the next most informative compounds to explore, based on prior experimental results.
   - **Input:** Historical molecular or reaction data, experimental outcome metrics (e.g., yield, activity).
   - **Output:** Suggested next points to test in the design space.

   Technical Insight:

   - Thompson Sampling maintains a probabilistic belief over the outcome function (e.g., Gaussian Processes).
   - At each iteration, it samples a function from the posterior and selects the optimal candidate according to that sample.
   - Ideal for adaptive design of experiments in drug synthesis or chemical reaction optimization.

   Use Cases:

   - Reaction condition optimization (temperature, solvent, time).
   - Compound selection for ADMET screening.
   - Exploration of molecular derivatives for improved efficacy.

2. REINVENT (AI-based Molecular Generation)
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Endpoint:** ``/v1/api/reinvent/run_reinvent``
   - **Description:** REINVENT is a generative model that produces new molecular structures using reinforcement learning (RL) to guide toward desirable chemical properties.
   - **Input:** Prior SMILES strings, scoring function or QSAR model.
   - **Output:** Novel molecules predicted to satisfy target criteria (e.g., low toxicity, high logP, IC50 thresholds).

   Technical Insight:

   - Uses Recurrent Neural Networks (RNNs) trained on SMILES strings.
   - Reward function is defined using a multi-objective scoring system (e.g., QED, docking score, synthetic accessibility).
   - Reinforcement learning is used to shift the model distribution toward molecules with higher reward.

   Use Cases:

   - Lead optimization in drug discovery.
   - Biasing generative models toward patentable chemical space.
   - De novo molecular design under constraint (e.g., molecular weight, rotatable bonds).

Finetuning Approaches
---------------------

Different strategies are used based on the task and data availability:

- Transfer Learning: Pretrained molecular models are adapted to a narrow task using smaller labeled datasets.
- Bayesian Optimization: Iteratively selects samples to evaluate based on uncertainty models (as in Thompson Sampling).
- Reinforcement Learning: Explores a chemical space by assigning rewards and learning optimal generation strategies (as in REINVENT).
- Active Learning: Combines model training with data acquisition to refine predictions efficiently.

Input & Output Formats
----------------------

- Inputs:

  - Tabular data (CSV) for historical measurements (TS).
  - SMILES strings with scoring functions or constraints (REINVENT).

- Outputs:

  - Ranked list of optimized candidates.
  - Generation logs and summary statistics (mean reward, diversity, etc.).

Best Practices
--------------

- Always normalize and clean experimental data before feeding into Thompson Sampling.
- Define clear and measurable scoring metrics when using REINVENT.
- Validate in silico predictions with expert review or docking simulations.

Summary
-------

Finetuning tools in Qubio allow users to go beyond static prediction and actively guide the molecular design process. Whether through Bayesian sampling or reinforcement-based generation, these tools help optimize candidates with high confidence and reduced experimental overhead.

Refer to individual documentation for more detail:

- :doc:`tasks/thompson_sampling`
- :doc:`tasks/reinvent`

