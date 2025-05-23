Protein Characterization and Property Prediction
================================================

Overview
--------

Protein characterization involves the computational and experimental determination of various physicochemical, biochemical, and biological properties of proteins. Understanding these properties is essential for insights into protein stability, function, interaction potential, and suitability for therapeutic or industrial applications.

Why Characterization Matters
----------------------------

- 🔬 **Stability Assessment:** Predicts thermal stability, solubility, and aggregation propensity which impact protein formulation and shelf-life.
- 🧪 **Functionality Insight:** Helps infer enzymatic activity, binding affinities, and structural dynamics.
- 🧬 **Mutational Effects:** Evaluates how amino acid substitutions alter protein behavior and stability.
- 💊 **Drug Design Support:** Guides selection of druggable targets and design of stable therapeutic proteins or antibodies.

Qubio integrates several advanced tools that analyze protein properties computationally, enabling rapid screening and prioritization before wet-lab experiments.

Characterization Tools in Qubio
-------------------------------

1. **ThermoMPNN**
   ^^^^^^^^^^^^^^

   - **Endpoint:** `/v1/api/thermomppn/run_tmppn`  
   - **Description:** Predicts protein thermostability and stability changes upon single or multiple mutations.  
   - **Input:** Protein structure files and mutation lists.  
   - **Output:** Predicted stability metrics such as ΔΔG values and melting temperature changes.

   Technical Details:

   - Uses a machine learning model trained on mutation-stability datasets.
   - Employs graph neural networks to incorporate atomic-level structural context.
   - Useful for guiding protein engineering efforts toward more stable variants.

2. **ParaSurf**
   ^^^^^^^^^^^^^

   - **Endpoint:** `/v1/api/parasurf/run_ps`  
   - **Description:** Predicts and analyzes protein surface properties such as electrostatic potential and solvent accessibility.  
   - **Input:** Protein 3D structure files (e.g., PDB).  
   - **Output:** Surface maps, property scores, and visualizable data.

   Technical Details:

   - Computes physicochemical surface features relevant for protein-protein and protein-ligand interactions.
   - Assists in epitope mapping and binding site identification.

3. **ADMET AI**
   ^^^^^^^^^^^^^

   - **Endpoint:** `/v1/api/admet_ai/run_admet`  
   - **Description:** Predicts Absorption, Distribution, Metabolism, Excretion, and Toxicity (ADMET) properties of compounds.  
   - **Input:** Molecular structures (SMILES or SDF).  
   - **Output:** Predicted ADMET profiles to prioritize drug candidates.

   Technical Details:

   - Combines multiple AI models trained on pharmacokinetic and toxicological data.
   - Facilitates early identification of potential liabilities in drug design.

Why Use Computational Characterization?
---------------------------------------

- Rapid screening of protein variants or compounds without costly lab experiments.
- Early detection of problematic mutations or molecular features.
- Complementary insights to experimental data.
- Integration into automated pipelines for high-throughput screening.

Input and Output Formats
------------------------

- Protein structures in PDB or mmCIF format.
- Mutation files as plain text or CSV listing substitutions.
- Compound structures in SMILES, SDF, or MOL2 formats.
- Outputs as CSV reports, 3D structure annotations, or interactive visualization files.

Best Practices
--------------

- Validate input structures for completeness and quality before analysis.
- Combine multiple property predictions for a comprehensive view.
- Use predictions to guide experimental design and mutation prioritization.
- Interpret results in the context of biological function and experimental conditions.

Summary
-------

Protein characterization tools in Qubio enable detailed in silico evaluation of protein properties critical for engineering, drug discovery, and functional studies. By leveraging state-of-the-art AI and physics-based methods, these tools accelerate the molecular design cycle with greater confidence.

For detailed usage, refer to individual tool documentation:

- :doc:`tasks/thermomppn`
- :doc:`tasks/parasurf`
- :doc:`tasks/admet_ai`
