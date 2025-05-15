ProteinMPNN
===========

Overview
--------

ProteinMPNN is a machine learning-based framework for sequence design — the process of predicting amino acid sequences that will fold into a given 3D protein structure. This is known as inverse folding. While traditional protein design approaches relied on physics-based modeling, ProteinMPNN uses deep learning to directly model the complex relationship between structure and sequence.

The method is trained to understand how amino acid residues fit within a fixed structural context, enabling it to generate or optimize sequences that are compatible with a desired backbone conformation.

Scientific Motivation
---------------------

The function of a protein is determined by its three-dimensional structure, which is, in turn, determined by its amino acid sequence. Inverse folding — predicting a sequence that will assume a particular structure — is a central problem in protein engineering. It allows:

- Rational design of protein sequences with desirable properties (e.g., solubility, stability, binding).
- Mutation tolerance analysis for therapeutic protein engineering.
- De novo protein design: constructing entirely new proteins from scratch.

ProteinMPNN enables high-throughput, accurate, and structure-aware design with minimal reliance on template sequences or known motifs.

Core Principles
---------------

ProteinMPNN uses a graph-based deep neural network architecture designed to capture the geometric and chemical environment of protein residues. Its main components are:

- Structural Encoding:
  The input to ProteinMPNN is a 3D protein backbone (typically a PDB file). The model encodes geometric features such as distances, orientations, and angles between residues.

- Residue Graph Construction:
  The protein is modeled as a graph, where each node corresponds to an amino acid and edges encode spatial relationships. This graph represents the local environment of each residue.

- Sequence Prediction:
  A masked language modeling approach is applied, where the model predicts the most likely residue types given their spatial neighbors. It generates a probability distribution over 20 amino acids at each position.

- Energy Optimization:
  The network is trained to minimize loss functions that reflect sequence-structure compatibility, ensuring the designed sequences are likely to fold into the provided structure.

Applications
------------

ProteinMPNN can be applied to a range of protein design challenges:

- Stabilizing mutations for therapeutic proteins and enzymes.
- Designing protein-protein interfaces or antibody-antigen interactions.
- Engineering scaffolds for molecular recognition or catalysis.
- Tuning binding specificity and affinity through targeted mutations.

It can be used either for global redesign (entire sequence) or local design (specific regions such as loops or interfaces).

Input Requirements
------------------

ProteinMPNN typically requires:

- A 3D protein backbone structure in PDB format.
- Optionally, a mask indicating which residues are to be redesigned or kept fixed.
- (For ΔΔG evaluation) Mutant and wild-type structures or sequences for comparison.

Side chain atoms are not needed — the backbone alone suffices, as the model focuses on sequence-to-backbone compatibility.

Output Data
-----------

ProteinMPNN produces:

- Amino acid sequences predicted to be compatible with the given backbone.
- Probabilistic outputs (e.g., per-position confidence or entropy).
- ΔΔG-like scores estimating the impact of mutations on structure or stability (in specific configurations).

Scientific Insights
-------------------

ProteinMPNN reflects several important principles in protein design:

- Contextual Dependency:
  The identity of a residue is highly dependent on its spatial neighbors — particularly residues within 10 Å.

- Flexibility vs. Robustness:
  Some regions of proteins are tolerant to multiple amino acids (high entropy), while others are highly constrained.

- Energetic Plausibility:
  The model’s scores correlate well with experimentally determined metrics like thermodynamic stability and mutational tolerance.

Limitations and Considerations
------------------------------

- Fixed Backbone:
  ProteinMPNN assumes a fixed backbone geometry. It does not account for conformational shifts that might accompany mutations.

- No Explicit Function Modeling:
  While the model optimizes for structural compatibility, it does not directly predict or optimize functional activity (e.g., catalytic rate or binding).

- Sequence Diversity:
  Output sequences tend to be deterministic unless sampling is explicitly enabled. For exploring sequence space, stochastic decoding should be used.

Integration in Design Pipelines
-------------------------------

ProteinMPNN is often used in tandem with other tools:

1. Predict a structure using AntiFold or LocalColabFold.
2. Design stable or functional sequences with ProteinMPNN.
3. Evaluate thermodynamic properties with ThermoMPNN.
4. Validate or refine designs through docking or wet-lab testing.

Conclusion
----------

ProteinMPNN offers a fast, structure-aware, and data-driven approach to protein sequence design. It has reshaped the field of protein engineering by making inverse folding accessible and scalable. As part of the Qubio suite, it serves as a foundational component in designing novel proteins with structural fidelity and functional potential.

For related modules, see:

- :doc:`thermompnn`
- :doc:`antifold`
- :doc:`localcolabfold`
