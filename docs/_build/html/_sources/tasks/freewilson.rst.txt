Free-Wilson Analysis
====================

Overview
--------

Free-Wilson analysis is a classical quantitative structure-activity relationship (QSAR) method used to dissect the contributions of individual substituents or chemical fragments to the overall biological activity of a compound. Introduced in the 1960s by Free and Wilson, this additive model assumes that the activity of a molecule can be decomposed into the sum of its structural features' contributions.

This approach is particularly useful in lead optimization phases of drug discovery, where small changes to a chemical scaffold can dramatically influence potency, selectivity, or pharmacokinetics.

Scientific Basis
----------------

The core hypothesis of Free-Wilson analysis is the additivity principle:

.. math::

    \log(\text{Activity}) = \sum_{i} c_i x_i + \epsilon

Where:
- :math:`x_i` represents the presence or absence (typically binary) of a specific substituent at a given position,
- :math:`c_i` is the contribution coefficient of that substituent,
- :math:`\epsilon` is the error term.

The model relies on having a consistent molecular scaffold, where variations in activity are attributed to the substitution patterns at defined positions. Each substituent’s contribution can be estimated using regression techniques, most commonly ordinary least squares.

How It Works
------------

1. **Define a Core Scaffold**:
   A series of compounds sharing the same molecular backbone is selected. Variations among them occur at specific substitution points (e.g., R-groups).

2. **Substituent Encoding**:
   Each substituent is represented using binary indicator variables. For instance, R1=OH becomes a feature `R1_OH=1` and all other R1 options are set to 0.

3. **Activity Regression**:
   The experimental activity values (e.g., pIC50) are regressed onto the binary matrix to determine the relative contribution of each substituent.

4. **Interpretation**:
   Coefficients with positive values indicate substituents that enhance activity, while negative coefficients suggest unfavorable modifications. The intercept corresponds to the baseline activity of the core scaffold.

Applications and Use Cases
--------------------------

Free-Wilson analysis is primarily used in:

- Lead optimization: guiding chemists on which substituents are most beneficial.
- SAR interpretation: quantifying the effect of structural changes.
- Series expansion: predicting activity of hypothetical compounds before synthesis.
- Prioritization of analogs for synthesis or testing.

Scientific Considerations
-------------------------

- The assumption of additivity may not hold in cases where significant steric clashes or conformational changes occur.
- Activity cliffs—where small changes result in large differences in activity—are not well modeled.
- Requires a reasonably sized and diverse training set with consistent experimental data.
- Works best with congeneric series and should not be applied across structurally diverse datasets.

Benefits of Free-Wilson Models
------------------------------

- Fast and interpretable: results are directly actionable by medicinal chemists.
- Requires no 3D structures or docking: purely based on 2D structure and bioactivity data.
- Complements machine learning approaches by offering mechanistic insights.
- Can highlight non-obvious trends in structure-activity data.

Integration in Qubio
--------------------

In Qubio, Free-Wilson analysis acts as a lightweight interpretability and predictive tool for ligand optimization pipelines. When used alongside generative tools (e.g., REINVENT, LigandMPNN), it helps validate and rank proposed modifications to a known scaffold series.

Workflow Integration
--------------------

1. Curate a set of ligands with a common scaffold and associated activity data.
2. Run Free-Wilson regression to compute fragment contributions.
3. Analyze coefficients and visualize favorable vs unfavorable R-groups.
4. Use insights to design or prioritize the next generation of analogs.

Conclusion
----------

Free-Wilson analysis remains a foundational method in medicinal chemistry for rationalizing SAR and predicting ligand activity based on structural substitutions. It excels in contexts where interpretability, speed, and ease of use are valued. As part of Qubio’s ligand-centric design suite, Free-Wilson analysis provides a transparent and efficient path toward data-driven decision-making in early drug discovery.

For complementary approaches, see:

- :doc:`reinvent`
- :doc:`ligandmpnn`
- :doc:`admet_ai`
