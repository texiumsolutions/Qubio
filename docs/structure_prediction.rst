Protein Structure Prediction
============================

Overview
--------

Protein structure prediction refers to the computational process of determining a protein’s three-dimensional (3D) conformation from its amino acid sequence. Since protein function is intricately linked to structure, predicting structure is a foundational task in molecular biology, bioinformatics, and drug discovery.

Traditionally, determining protein structure required experimental techniques like:

- X-ray crystallography
- NMR spectroscopy
- Cryo-electron microscopy (cryo-EM)

However, these are time-consuming and costly. Recent advances in machine learning have enabled rapid and accurate structure prediction using only sequence information.

Why It Matters
--------------

- 🧬 Understanding Function: Structure reveals how a protein performs its biological role.
- 🧪 Drug Design: Enables structure-based drug design (SBDD) by identifying binding pockets.
- 🔬 Mutational Analysis: Helps assess the impact of mutations on stability and function.
- 🧫 Synthetic Biology: Facilitates the design of new proteins by modeling their folds before synthesis.

Structure prediction is also crucial for downstream applications such as molecular docking, stability prediction, or ligand binding.

Structure Prediction Methods
----------------------------

There are three main types of structure prediction:

1. Homology Modeling:

   Based on similarity to known structures (templates).

2. Threading (Fold Recognition):

   Fits a sequence into a structural framework, even without close homologs.

3. Ab Initio / de novo Prediction:

   Predicts structure from scratch using physical principles and/or deep learning.

Tools in Qubio for Structure Prediction
---------------------------------------

Qubio provides the following tools that contribute to accurate structure prediction:

1. AntiFold
   ^^^^^^^^^^^

   - **Endpoint:** ``/v1/api/antifold/predict``
   - **Description:** Predicts protein structures using an open-source implementation inspired by AlphaFold2.
   - **Input:** FASTA-formatted sequence.
   - **Output:** 3D structure in PDB format.
   - **Technical Insight:** Uses deep learning on evolutionary, structural, and positional features derived from multiple sequence alignments (MSAs) and templates (if provided). Incorporates attention-based networks to predict inter-residue distances and angles, folding them into a 3D structure.

2. LocalColabFold
   ^^^^^^^^^^^^^^^^^

   - **Endpoint:** ``/v1/api/localcolabfold/run_colabfold``
   - **Description:** Predicts structures locally using ColabFold, a faster and more accessible implementation of AlphaFold2.
   - **Input:** Amino acid sequence.
   - **Output:** Predicted 3D structure (.pdb) and confidence scores.
   - **Technical Insight:** LocalColabFold speeds up MSA generation using MMseqs2 and avoids reliance on Google Colab. Predicts backbone and side-chain atom positions using end-to-end neural networks trained on experimentally solved structures.

Technical Foundations
---------------------

Protein folding is governed by several atomic-scale forces and geometric constraints:

- Backbone Geometry: φ (phi), ψ (psi), and ω (omega) torsion angles define peptide chain conformation.
- Hydrogen Bonding: Stabilizes secondary structures like α-helices and β-sheets.
- Hydrophobic Collapse: Drives non-polar residues into the core of globular proteins.
- Side Chain Packing: Influences steric compatibility and van der Waals interactions.
- Solvent Accessibility: Determines whether residues are buried or exposed.

Deep learning models predict residue-residue distance maps, contact maps, and torsion angles, then reconstruct 3D coordinates using gradient descent or attention-guided folding algorithms.

Input and Output Formats
------------------------

- Input: Protein sequence in FASTA format or a plain string.
- Output:

  - PDB structure files.
  - Predicted alignment error (PAE) maps.
  - Confidence metrics (pLDDT scores).

Sample Workflow
---------------

1. Start with a novel protein sequence.
2. Use AntiFold or LocalColabFold to predict the 3D structure.
3. Visualize the output in PyMOL, ChimeraX, or web tools like 3Dmol.js.
4. (Optional) Pass the predicted structure into ProteinMPNN, ThermoMPNN, or ParaSurf for further analysis or design.

Summary
-------

Protein structure prediction is foundational to modern biology and drug discovery. The tools provided in Qubio abstract away the complexities of deep learning models and make accurate structure prediction accessible via simple APIs.

For deeper integration, refer to individual tool documentation:

- :doc:`tasks/antifold`
- :doc:`tasks/localcolabfold`

