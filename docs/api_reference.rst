API Documentation
==================

This document describes the API endpoints available for various services. Each service has its own set of routes, which allow users to upload files, run analysis, and check task statuses.

---

==============================
API Documentation for all Tasks
==============================

This section provides an overview of the available tasks and their API endpoints.

Available Tasks
===============

1. **AntiFold**
   - **AntiFold Prediction**  
     **Endpoint:** `/v1/api/antifold/predict`  
     **Description:** Predicts protein structures using AntiFold.
   
   - **Check AntiFold Status**  
     **Endpoint:** `/v1/api/antifold/check_status/<task_id>`  
     **Description:** Checks the prediction status of AntiFold.

2. **ProteinMPNN**
   - **ProteinMPNN ddG Prediction**  
     **Endpoint:** `/v1/api/proteinmpnn/ddg`  
     **Description:** Predicts stability or binding affinity changes for mutations.
   
   - **Check ProteinMPNN Status**  
     **Endpoint:** `/v1/api/proteinmpnn/check_status/<task_id>`  
     **Description:** Checks the processing status of ProteinMPNN.

3. **Thompson Sampling**
   - **Run Thompson Sampling**  
     **Endpoint:** `/v1/api/thompson_sampling/run_ts`  
     **Description:** Performs Thompson Sampling for reaction optimization.
   
   - **Check Thompson Sampling Status**  
     **Endpoint:** `/v1/api/thompson_sampling/check_status/<task_id>`  
     **Description:** Checks the status of a Thompson Sampling task.

4. **Free-Wilson**
   - **Run Free-Wilson Analysis**  
     **Endpoint:** `/v1/api/freewilson/run_fw`  
     **Description:** Runs Free-Wilson analysis for molecular property prediction.
   
   - **Check Free-Wilson Status**  
     **Endpoint:** `/v1/api/freewilson/check_status/<task_id>`  
     **Description:** Checks Free-Wilson analysis task status.

5. **LigandMPNN**
   - **Run LigandMPNN**  
     **Endpoint:** `/v1/api/ligandmpnn/run_lmpnn`  
     **Description:** Generates ligand mutations using LigandMPNN.
   
   - **Check LigandMPNN Status**  
     **Endpoint:** `/v1/api/ligandmpnn/check_status/<task_id>`  
     **Description:** Checks LigandMPNN task processing status.

6. **LocalColabFold**
   - **Run LocalColabFold**  
     **Endpoint:** `/v1/api/localcolabfold/run_colabfold`  
     **Description:** Performs protein folding using LocalColabFold.
   
   - **Check LocalColabFold Status**  
     **Endpoint:** `/v1/api/localcolabfold/check_status/<task_id>`  
     **Description:** Checks the status of LocalColabFold folding tasks.

7. **ParaSurf**
   - **Run ParaSurf Analysis**  
     **Endpoint:** `/v1/api/parasurf/run_ps`  
     **Description:** Runs ParaSurf for protein surface prediction.
   
   - **Check ParaSurf Status**  
     **Endpoint:** `/v1/api/parasurf/check_status/<task_id>`  
     **Description:** Checks the processing status of ParaSurf.

8. **REINVENT**
   - **Run REINVENT**  
     **Endpoint:** `/v1/api/reinvent/run_reinvent`  
     **Description:** Runs REINVENT for drug design and optimization.
   
   - **Check REINVENT Status**  
     **Endpoint:** `/v1/api/reinvent/check_status/<task_id>`  
     **Description:** Checks REINVENT task processing status.

9. **ThermoMPNN**
   - **Run ThermoMPNN**  
     **Endpoint:** `/v1/api/thermomppn/run_tmppn`  
     **Description:** Runs ThermoMPNN for stability prediction.
   
   - **Check ThermoMPNN Status**  
     **Endpoint:** `/v1/api/thermomppn/check_status/<task_id>`  
     **Description:** Checks ThermoMPNN task processing status.

10. **ADMET AI**
    - **Run ADMET AI Prediction**  
      **Endpoint:** `/v1/api/admet_ai/run_admet`  
      **Description:** Predicts ADMET properties using AI models.
    
    - **Check ADMET AI Status**  
      **Endpoint:** `/v1/api/admet_ai/check_status/<task_id>`  
      **Description:** Checks the status of ADMET AI prediction tasks.

ADMET AI Service
================

**Blueprint Name**: `admet_ai`

**Base URL**: `/admet_ai`

### Endpoints

**POST /predict_admet**
------------------------
Predicts ADMET properties for a given SMILES file.

- **Request**:
  - **smiles_file** (file): The SMILES file containing molecular data to be analyzed.
  
- **Response**:
  - **200 OK**: Prediction results as JSON.
  - **400 Bad Request**: If no SMILES file is provided.
  - **500 Internal Server Error**: If an error occurs during prediction.

**GET /check_admet_status/<task_id>**
-------------------------------------
Checks the status of an ADMET prediction task.

- **Parameters**:
  - **task_id** (string): The unique task ID for the prediction.
  
- **Response**:
  - **200 OK**: JSON response with logs and uploaded Azure files.
  - **404 Not Found**: If the task ID is not found.
  - **500 Internal Server Error**: If an error occurs while checking status.

---

AntiFold Service
================

**Blueprint Name**: `antifold`

**Base URL**: `/antifold`

### Endpoints

**POST /predict**
-----------------
Runs the AntiFold prediction for a given PDB file.

- **Request**:
  - **pdb_file** (file) or **pdb_url** (string): The PDB file or URL pointing to the PDB file to be analyzed.
  - **task_type** (string): Type of the task to run.
  - **heavy_chain** (string): Heavy chain sequence (optional).
  - **light_chain** (string): Light chain sequence (optional).

- **Response**:
  - **200 OK**: Prediction results as JSON.
  - **400 Bad Request**: If neither a PDB file nor URL is provided.
  - **500 Internal Server Error**: If an error occurs during prediction.

**GET /check_status/<task_id>**
------------------------------
Checks the status of an AntiFold task.

- **Parameters**:
  - **task_id** (string): The unique task ID for the prediction.
  
- **Response**:
  - **200 OK**: JSON response with logs and uploaded Azure files.
  - **404 Not Found**: If the task ID is not found.
  - **500 Internal Server Error**: If an error occurs while checking status.

---

ColabDock Service
=================

**Blueprint Name**: `colabdock`

**Base URL**: `/colabdock`

### Endpoints

**POST /dock**
--------------
Runs the ColabDock docking task.

- **Request**:
  - **pdb_file** (file) or **pdb_url** (string): The PDB file or URL pointing to the PDB file to be docked.

- **Response**:
  - **200 OK**: Docking results as JSON.
  - **400 Bad Request**: If neither a PDB file nor URL is provided.
  - **500 Internal Server Error**: If an error occurs during docking.

**GET /check_status/<task_id>**
------------------------------
Checks the status of a ColabDock docking task.

- **Parameters**:
  - **task_id** (string): The unique task ID for the docking.

- **Response**:
  - **200 OK**: JSON response with logs and uploaded Azure files.
  - **404 Not Found**: If the task ID is not found.
  - **500 Internal Server Error**: If an error occurs while checking status.

---

Free-Wilson Service
===================

**Blueprint Name**: `freewilson`

**Base URL**: `/freewilson`

### Endpoints

**POST /run_analysis**
-----------------------
Runs the Free-Wilson analysis.

- **Request**:
  - **scaffold_file** (file) or **scaffold_url** (string): The scaffold file or URL.
  - **input_smiles_file** (file) or **input_smiles_url** (string): The SMILES file or URL.
  - **activity_file** (file) or **activity_url** (string): The activity file or URL.
  - **prefix** (string): A unique task ID (optional).
  
- **Response**:
  - **200 OK**: Analysis results as JSON.
  - **400 Bad Request**: If required files or URLs are missing.
  - **500 Internal Server Error**: If an error occurs during analysis.

**GET /check_status/<task_id>**
------------------------------
Checks the status of the Free-Wilson analysis task.

- **Parameters**:
  - **task_id** (string): The unique task ID for the analysis.
  
- **Response**:
  - **200 OK**: JSON response with logs and uploaded Azure files.
  - **404 Not Found**: If the task ID is not found.
  - **500 Internal Server Error**: If an error occurs while checking status.

---

LigandMPNN Service
==================

**Blueprint Name**: `ligandmpnn`

**Base URL**: `/ligandmpnn`

### Endpoints

**POST /design**
-----------------
Starts the LigandMPNN design task.

- **Request**:
  - **pdb_file** (file) or **pdb_file_url** (string): The PDB file or URL pointing to the PDB file.
  - **chains_to_design** (string): The chains to design.
  - **fixed_residues** (string): Fixed residues (optional).
  - **residues_to_design** (string): Residues to design (optional).
  - **temperature** (float): The temperature parameter for the design.
  - **number_of_batches** (int): Number of batches to process.

- **Response**:
  - **200 OK**: Design results as JSON.
  - **400 Bad Request**: If no PDB file is provided or if chains to design are missing.
  - **500 Internal Server Error**: If an error occurs during design.

**GET /check_status/<task_id>**
------------------------------
Checks the status of a LigandMPNN design task.

- **Parameters**:
  - **task_id** (string): The unique task ID for the design.

- **Response**:
  - **200 OK**: JSON response with logs and uploaded Azure files.
  - **404 Not Found**: If the task ID is not found.
  - **500 Internal Server Error**: If an error occurs while checking status.

---

LocalColabFold API
==================

**Blueprint Name**: `localcolabfold`

This API allows users to predict protein structures using the LocalColabFold method.

Routes:
-------

1. **POST /predict**
    - **Description**: Accepts a FASTA file upload or URL and runs the LocalColabFold prediction.
    - **Parameters**:
        - `fasta_file`: The protein sequence in FASTA format (file upload).
        - `fasta_file_url`: The URL of a FASTA file (optional if `fasta_file` is provided).
    - **Response**: Returns a JSON object containing the prediction results.
    - **Errors**:
        - 400: No FASTA file or URL provided.
        - 500: Internal server error.

2. **GET /check_status/<task_id>**
    - **Description**: Checks the status of a task based on the task ID, and retrieves the log and Azure upload results.
    - **Parameters**:
        - `task_id`: The ID of the task to check.
    - **Response**: Returns a JSON object containing the logs and any uploaded files to Azure.
    - **Errors**:
        - 404: Task ID not found.
        - 500: Internal server error.

ParaSurf API
============

**Blueprint Name**: `parasurf`

This API allows users to predict protein surface properties using the ParaSurf tool.

Routes:
-------

1. **POST /predict**
    - **Description**: Accepts a PDB file upload or URL and runs the ParaSurf prediction.
    - **Parameters**:
        - `pdb_file`: A PDB file containing the protein structure (file upload).
        - `pdb_url`: The URL of a PDB file (optional if `pdb_file` is provided).
    - **Response**: Returns a JSON object containing the prediction results.
    - **Errors**:
        - 400: No PDB file or URL provided.
        - 500: Internal server error.

2. **GET /check_status/<task_id>**
    - **Description**: Checks the status of a task based on the task ID, and retrieves the log and Azure upload results.
    - **Parameters**:
        - `task_id`: The ID of the task to check.
    - **Response**: Returns a JSON object containing the logs and any uploaded files to Azure.
    - **Errors**:
        - 404: Task ID not found.
        - 500: Internal server error.

ProteinMPNN API
===============

**Blueprint Name**: `proteinmpnn`

This API predicts the stability and mutation effects of proteins using ProteinMPNN.

Routes:
-------

1. **POST /ddg**
    - **Description**: Accepts a PDB file upload or URL and runs the ProteinMPNN prediction.
    - **Parameters**:
        - `pdb_file`: A PDB file (file upload).
        - `pdb_file_url`: The URL of a PDB file (optional if `pdb_file` is provided).
        - `chain`: The chain identifier (optional, default is "A").
    - **Response**: Returns a JSON object containing the prediction results.
    - **Errors**:
        - 400: No PDB file or URL provided.
        - 500: Internal server error.

2. **GET /check_status/<task_id>**
    - **Description**: Checks the status of a task based on the task ID, and retrieves the log and Azure upload results.
    - **Parameters**:
        - `task_id`: The ID of the task to check.
    - **Response**: Returns a JSON object containing the logs and any uploaded files to Azure.
    - **Errors**:
        - 404: Task ID not found.
        - 500: Internal server error.

REINVENT API
============

**Blueprint Name**: `reinvent`

This API allows users to run REINVENT, a tool for molecular generation and optimization.

Routes:
-------

1. **POST /predict**
    - **Description**: Accepts a SMILES string and runs the REINVENT prediction.
    - **Parameters**:
        - `smiles`: The SMILES representation of the molecule.
    - **Response**: Returns a JSON object containing the prediction results.
    - **Errors**:
        - 400: SMILES input is required.
        - 500: Internal server error.

2. **GET /check_status/<task_id>**
    - **Description**: Checks the status of a task based on the task ID, and retrieves the log and Azure upload results.
    - **Parameters**:
        - `task_id`: The ID of the task to check.
    - **Response**: Returns a JSON object containing the logs and any uploaded files to Azure.
    - **Errors**:
        - 404: Task ID not found.
        - 500: Internal server error.

ThermoMPNN API
==============

**Blueprint Name**: `thermompnn`

This API uses ThermoMPNN for predicting the stability of proteins based on mutations.

Routes:
-------

1. **POST /predict**
    - **Description**: Accepts a PDB file upload or URL and starts a ThermoMPNN prediction for stability or mutation effects.
    - **Parameters**:
        - `task_type`: The type of task ('single', 'epistatic', or 'double').
        - `pdb_file`: A PDB file (file upload).
        - `pdb_file_url`: The URL of a PDB file (optional if `pdb_file` is provided).
    - **Response**: Returns a JSON object containing the prediction results.
    - **Errors**:
        - 400: No PDB file or URL provided.
        - 500: Internal server error.

2. **GET /check_status/<task_id>**
    - **Description**: Checks the status of a task based on the task ID, and retrieves the log and Azure upload results.
    - **Parameters**:
        - `task_id`: The ID of the task to check.
    - **Response**: Returns a JSON object containing the logs and any uploaded files to Azure.
    - **Errors**:
        - 404: Task ID not found.
        - 500: Internal server error.

Thompson Sampling API
=====================

**Blueprint Name**: `thompson_sampling`

This API allows users to run the Thompson Sampling algorithm for molecular exploration.

Routes:
-------

1. **POST /run_ts**
    - **Description**: Starts a Thompson Sampling task and returns the task ID with Azure Blob Storage links.
    - **Parameters**:
        - `reaction_smarts`: The SMARTS representation of the reaction.
        - `num_warmup_trials`: The number of warmup trials.
        - `num_ts_iterations`: The number of Thompson Sampling iterations.
        - `evaluator`: The evaluator method (options: "FPEvaluator", "MLClassifierEvaluator", "FredEvaluator", "ROCSEvaluator").
        - `ts_mode`: The Thompson Sampling mode.
    - **Response**: Returns a JSON object containing the task results.
    - **Errors**:
        - 400: Missing required parameters.
        - 500: Internal server error.


General Information
===================

All services are hosted using Flask and accept file uploads via POST requests. Azure Blob Storage is used to store results, and task status can be checked via GET requests. Each service may include logging and file download functionality as part of the process.

---

Last Updated
============

This list was last updated on :date:.

---

Logging
========

The APIs log all interactions for debugging and monitoring. Logs are saved to local files and can be accessed as part of the task status.

