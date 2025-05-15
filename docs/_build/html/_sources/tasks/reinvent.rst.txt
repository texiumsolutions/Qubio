REINVENT
========

Overview
--------

REINVENT is a deep generative model for de novo molecular design. It uses reinforcement learning (RL) to guide the generation of novel chemical structures that fulfill predefined objectives, such as activity against a biological target, drug-likeness, or synthetic accessibility.

This model represents a powerful approach in cheminformatics, enabling exploration of vast chemical space with control over desired molecular properties. Unlike classical virtual screening, which selects from existing libraries, REINVENT designs new molecules from scratch while adhering to medicinal chemistry constraints.

Scientific Motivation
---------------------

The search for new small molecules with therapeutic potential is central to drug discovery. However, the number of possible drug-like molecules is estimated to be between 10²³ and 10⁶⁰ — far beyond what brute-force enumeration or screening can cover.

REINVENT addresses this challenge by:

- Learning from known molecules to understand drug-like patterns.
- Sampling novel compounds from this learned chemical space.
- Guiding generation toward specific objectives via reinforcement learning.

This combination of deep learning and reward-driven optimization enables generation of structurally novel, property-compliant molecules at scale.

Core Methodology
----------------

REINVENT is built on a recurrent neural network (RNN) trained on SMILES strings — textual representations of molecules. Its architecture and workflow include:

1. Prior Model:
   An RNN trained on a large chemical database (e.g., ChEMBL) to learn the grammar of valid SMILES strings and the distribution of drug-like molecules.

2. Agent Model:
   A copy of the prior model that is fine-tuned via reinforcement learning to bias generation toward user-defined goals.

3. Scoring Functions:
   External evaluators compute rewards for generated molecules. These can include:
   
   - Docking score against a target protein.
   - LogP (lipophilicity), TPSA (polarity), or QED (drug-likeness).
   - Toxicity predictions or synthetic accessibility.
   - Binary or regression models of biological activity.

4. Reinforcement Learning Loop:
   The agent generates SMILES strings, receives feedback via the scoring function, and updates its policy to maximize expected reward using policy gradient methods.

5. Diversity Filters:
   Penalize repetitive or similar scaffolds to ensure chemical diversity.

Applications
------------

REINVENT can be used for a wide range of drug discovery and design tasks:

- Hit generation: Finding novel scaffolds with predicted activity.
- Lead optimization: Modifying known actives to improve ADMET properties.
- Multi-objective optimization: Balancing potency, selectivity, solubility, and synthetic feasibility.
- Scaffold hopping: Discovering alternative cores with retained function.

Input Requirements
------------------

REINVENT typically requires the following:

- A pretrained prior model (available from public sources or trained in-house).
- A scoring script or API that evaluates the properties of generated molecules.
- (Optional) A starting set of known actives to guide early exploration.
- Configuration files defining optimization parameters (e.g., batch size, learning rate, reward functions).

The model operates directly on SMILES strings, ensuring compatibility with most cheminformatics toolkits.

Output Data
-----------

REINVENT produces:

- Lists of novel SMILES strings ranked by total reward or individual objectives.
- Log files showing training progress, including average scores and diversity metrics.
- Optionally, decoded molecular graphs or 2D structures via RDKit or similar libraries.

Scientific Insights
-------------------

- Exploration vs. Exploitation:
  REINVENT balances the tradeoff between generating novel molecules and exploiting known scoring patterns.

- Reward Shaping:
  Composite scoring functions allow nuanced objectives (e.g., low toxicity + high affinity + novel scaffold).

- Representation Power:
  The SMILES-based RNN can generate syntactically valid, chemically plausible molecules even after extensive training.

Limitations and Considerations
------------------------------

- Dependence on Scoring Function:
  The quality of generated molecules is limited by the accuracy of the scoring model or function used.

- Synthetic Feasibility:
  While REINVENT can bias toward easy-to-synthesize molecules, this is not guaranteed unless explicitly modeled.

- Lack of Structural Context:
  REINVENT operates on 1D representations (SMILES), not 3D protein-ligand interactions, unless docking is included in the reward.

Integration in Design Pipelines
-------------------------------

REINVENT fits into the broader drug design workflow:

1. Define target profile (e.g., binding + solubility + low toxicity).
2. Use REINVENT to generate molecules meeting multi-objective criteria.
3. Dock top candidates to protein structure (e.g., with ColabDock).
4. Filter with ADMET or ParaSurf tools for further selection.
5. Synthesize and test top candidates experimentally.

Conclusion
----------

REINVENT represents a shift from passive screening to active molecular design. Its reinforcement learning core makes it adaptive and target-aware, while its generative model ensures novelty. In Qubio, REINVENT is the principal module for drug-like molecule generation, enabling iterative, goal-driven chemical discovery.

Related modules:

- :doc:`colabdock`
- :doc:`admet_ai`
- :doc:`ligandmpnn`
