ThermoSMP (Thermostability Sampling)
====================================

Overview
--------

ThermoSMP (Thermostability Sampling) is a computational method designed to explore the sequence space around a given protein structure with a focus on enhancing thermal stability. It integrates sampling strategies with stability prediction models to identify promising mutations or variants that improve protein robustness under elevated temperatures.

ThermoSMP is particularly useful for navigating the combinatorial explosion of possible mutations by efficiently sampling variants predicted to be more thermostable.

Scientific Motivation
---------------------

Protein thermostability is crucial for numerous applications such as industrial enzymes, biosensors, and therapeutic proteins that must retain function under harsh conditions. However, exhaustive experimental mutagenesis is unfeasible due to the vast mutation space.

ThermoSMP employs informed sampling guided by stability predictors (e.g., ThermoMPNN) and structural context to prioritize mutants likely to increase melting temperature (Tm) or folding free energy (ΔG).

By combining stochastic sampling with machine learning predictions, ThermoSMP offers:

- Efficient exploration of mutational landscapes.
- Identification of combinatorial mutations with additive or synergistic effects.
- Guidance for experimental mutagenesis campaigns.

Methodology
-----------

1. Initial Setup:
   - Input a high-quality protein structure (PDB format).
   - Define regions or residues of interest (e.g., active site, surface, core).

2. Sampling Strategy:
   - Use Markov Chain Monte Carlo (MCMC), Metropolis-Hastings, or other probabilistic algorithms to propose mutations.
   - Mutations are proposed based on residue-specific probabilities or biochemical constraints (e.g., hydrophobicity, charge).

3. Stability Evaluation:
   - Each sampled mutant is evaluated using a stability predictor such as ThermoMPNN.
   - Acceptance or rejection of proposed mutations follows criteria based on predicted ΔΔG or ΔTm.

4. Iterative Refinement:
   - Sampling iterates to converge on sequences predicted to have higher stability.
   - Sampling can include single or multiple mutations per iteration.

5. Output:
   - Ranked list of mutations or variants with predicted thermostability scores.
   - Optionally, structural models of the top variants for further analysis.

Applications
------------

ThermoSMP supports diverse protein engineering tasks, including:

- Directed evolution in silico for thermostabilization.
- Design of stable variants for industrial catalysts.
- Exploration of mutational effects beyond single-point changes.
- Integration with downstream design tools for multi-objective optimization.

Advantages
----------

- Efficient exploration without exhaustive enumeration.
- Integration of biochemical knowledge with data-driven predictions.
- Flexibility to incorporate various stability models or scoring functions.
- Ability to model epistatic effects through multi-mutation sampling.

Limitations
-----------

- Quality of stability predictions directly impacts sampling efficiency.
- Sampling algorithms may get trapped in local minima without sufficient exploration.
- Computational cost can rise with increasing mutation numbers and protein size.
- Assumes the input structure is an accurate representation of the native fold.

Input and Output
----------------

Input:

- Protein structure file (PDB).
- Mutation target sites or entire sequence.
- Sampling parameters (number of iterations, mutation rates, acceptance thresholds).

Output:

- List of sampled sequences ranked by predicted stability.
- Predicted stability metrics (ΔΔG, ΔTm).
- Optional mutant structural models (PDB files).

Integration with Qubio
----------------------

ThermoSMP complements ThermoMPNN and ProteinMPNN by providing a sampling framework to generate and evaluate mutations in a thermostability-driven manner.

Typical pipeline:

1. Obtain or predict protein structure (AntiFold, LocalColabFold).
2. Use ThermoSMP to sample stable mutations guided by ThermoMPNN.
3. Select top candidates for further characterization or experimental validation.

Conclusion
----------

ThermoSMP offers a powerful computational approach for exploring protein sequence space with a focus on enhancing thermostability. By marrying stochastic sampling algorithms with advanced stability predictors, it accelerates the design of robust proteins fit for challenging environments.

It serves as a key module in Qubio’s protein property characterization and optimization toolkit.

Related Tools
-------------

- :doc:`thermompnn`
- :doc:`proteinmpnn`
- :doc:`antifold`
- :doc:`localcolabfold`
