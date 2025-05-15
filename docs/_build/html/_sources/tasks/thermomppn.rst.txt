ThermoMPNN
==========

Overview
--------

ThermoMPNN is a deep learning framework designed to predict and optimize the thermal stability of proteins. Built upon the foundational ProteinMPNN architecture, ThermoMPNN introduces supervised learning mechanisms to capture the thermodynamic effects of point mutations or sequence changes, specifically with respect to protein melting temperature (Tm) or Gibbs free energy of unfolding (ΔG).

This tool is critical for engineering proteins that function in extreme conditions, stabilizing therapeutic proteins, and exploring the relationship between sequence, structure, and stability.

Scientific Motivation
---------------------

Protein stability is a major determinant of:

- Foldability and expression yield.
- Functional longevity (especially in industrial or therapeutic contexts).
- Resistance to denaturation or aggregation.

However, experimental approaches like thermal shift assays or calorimetry are labor-intensive. ThermoMPNN addresses this bottleneck using graph-based neural networks trained on experimental ΔΔG and Tm data.

By learning the nuanced sequence-structure-stability relationships, ThermoMPNN enables:

- Prioritization of stabilizing mutations.
- Computational saturation mutagenesis.
- Thermostability optimization during protein design.

Methodology
-----------

ThermoMPNN uses a message-passing neural network (MPNN) that operates on residue-level graphs derived from 3D protein structures.

Key steps include:

1. Graph Construction:
   - Nodes represent amino acid residues.
   - Edges encode spatial proximity, orientation, and chemical context.

2. Input Representation:
   - The protein structure is parsed from PDB files.
   - Atomic coordinates are converted into geometric and chemical features.
   - Mutations are introduced in silico for stability scanning.

3. Model Architecture:
   - A graph neural network encodes the local environment of each residue.
   - The model is trained on curated datasets of single-point mutations with known ΔΔG (e.g., from ProTherm, FireProtDB).
   - Outputs include a scalar stability prediction for each variant.

4. Stability Prediction:
   - ΔΔG or ΔTm values are predicted for single mutants or multiple mutants.
   - Results can be filtered based on position, distance to active sites, or disulfide constraints.

Use Cases
---------

ThermoMPNN is suitable for:

- Rational thermostabilization of enzymes.
- Improving biotherapeutic shelf-life.
- Screening stabilizing vs. destabilizing mutations.
- Coupling with generative design models like ProteinMPNN to select stable variants.

Stability Types
---------------

ThermoMPNN can evaluate:

- ΔΔG of folding: Change in free energy upon mutation.
- ΔTm: Shift in melting temperature.
- Both metrics are proxies for thermodynamic stability, depending on the training regime.

Input Requirements
------------------

ThermoMPNN accepts:

- A protein structure in PDB format (wild-type).
- A list of mutations (e.g., A123V, T56K).
- Optional filtering parameters:
  - Residue type (polar/non-polar).
  - Distance constraints (e.g., surface or core).
  - Contact with catalytic or ligand-binding residues.

Output Formats
--------------

- CSV or JSON with:
  - Mutation identifiers.
  - Predicted ΔΔG or ΔTm.
  - Rank or score confidence.
- (Optional) Mutant structure files if modeling mutations structurally.

Scientific Insights
-------------------

- Stability prediction is highly dependent on local structural context.
- Destabilizing mutations often introduce voids, charge clashes, or break hydrogen bonds.
- ThermoMPNN can learn compensatory effects of buried residues, surface entropy, or secondary structure positioning.

Limitations
-----------

- Predictions assume correct wild-type structure — quality of input PDB is critical.
- Highly flexible or disordered regions may reduce accuracy.
- Multi-mutant effects (epistasis) are only partially captured unless explicitly modeled.

Design Integration
------------------

ThermoMPNN works seamlessly within Qubio’s protein engineering pipeline:

1. Predict structure using AntiFold or LocalColabFold.
2. Design sequences with ProteinMPNN.
3. Score variants for thermostability using ThermoMPNN.
4. Filter or re-rank based on stability, function, or solubility.
5. Advance top variants to in vitro testing.

Conclusion
----------

ThermoMPNN empowers protein engineers to explore the stability landscape of proteins with unprecedented resolution. By coupling structure-based modeling with supervised learning, it provides a practical, interpretable, and scalable method for designing thermodynamically robust proteins.

For stability-constrained design, ThermoMPNN is the backbone tool in Qubio’s property characterization module.

Related tools:

- :doc:`proteinmpnn`
- :doc:`antifold`
- :doc:`parasurf`
