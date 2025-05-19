API Documentation
=================

This document describes the API endpoints available for various services. Each service has its own set of routes, which allow users to upload files, run analysis, and check task statuses.

Available Tasks
---------------

1. **AntiFold**
   - **Prediction**: ``/v1/api/antifold/predict``  
     Predicts protein structures using AntiFold.
   - **Check Status**: ``/v1/api/antifold/check_status/<task_id>``  
     Checks the prediction status of AntiFold.

2. **ProteinMPNN**
   - **ddG Prediction**: ``/v1/api/proteinmpnn/ddg``  
     Predicts stability or binding affinity changes for mutations.
   - **Check Status**: ``/v1/api/proteinmpnn/check_status/<task_id>``  
     Checks the processing status of ProteinMPNN.

3. **Thompson Sampling**
   - **Run**: ``/v1/api/thompson_sampling/run_ts``  
     Performs Thompson Sampling for reaction optimization.
   - **Check Status**: ``/v1/api/thompson_sampling/check_status/<task_id>``  
     Checks the status of a Thompson Sampling task.

4. **Free-Wilson**
   - **Run Analysis**: ``/v1/api/freewilson/run_fw``  
     Runs Free-Wilson analysis for molecular property prediction.
   - **Check Status**: ``/v1/api/freewilson/check_status/<task_id>``  
     Checks Free-Wilson analysis task status.

5. **LigandMPNN**
   - **Run Design**: ``/v1/api/ligandmpnn/run_lmpnn``  
     Generates ligand mutations using LigandMPNN.
   - **Check Status**: ``/v1/api/ligandmpnn/check_status/<task_id>``  
     Checks LigandMPNN task processing status.

6. **LocalColabFold**
   - **Run**: ``/v1/api/localcolabfold/run_colabfold``  
     Performs protein folding using LocalColabFold.
   - **Check Status**: ``/v1/api/localcolabfold/check_status/<task_id>``  
     Checks the status of LocalColabFold folding tasks.

7. **ParaSurf**
   - **Run**: ``/v1/api/parasurf/run_ps``  
     Runs ParaSurf for protein surface prediction.
   - **Check Status**: ``/v1/api/parasurf/check_status/<task_id>``  
     Checks the processing status of ParaSurf.

8. **REINVENT**
   - **Run**: ``/v1/api/reinvent/run_reinvent``  
     Runs REINVENT for drug design and optimization.
   - **Check Status**: ``/v1/api/reinvent/check_status/<task_id>``  
     Checks REINVENT task processing status.

9. **ThermoMPNN**
   - **Run**: ``/v1/api/thermomppn/run_tmppn``  
     Runs ThermoMPNN for stability prediction.
   - **Check Status**: ``/v1/api/thermomppn/check_status/<task_id>``  
     Checks ThermoMPNN task processing status.

10. **ADMET AI**
    - **Run Prediction**: ``/v1/api/admet_ai/run_admet``  
      Predicts ADMET properties using AI models.
    - **Check Status**: ``/v1/api/admet_ai/check_status/<task_id>``  
      Checks the status of ADMET AI prediction tasks.

ADMET AI Service
----------------

**Blueprint Name**: ``admet_ai``  
**Base URL**: ``/admet_ai``

**POST /predict_admet**  
Predicts ADMET properties for a given SMILES file.

- **Request**:
  - `smiles_file` (file): The SMILES file containing molecular data.
- **Response**:
  - `200 OK`: JSON result of prediction.
  - `400 Bad Request`: No file provided.
  - `500 Internal Server Error`: Prediction failure.

**GET /check_admet_status/<task_id>**  
Checks the status of an ADMET task.

- **Parameters**:
  - `task_id` (string): Unique task identifier.
- **Response**:
  - `200 OK`: Log and file upload summary.
  - `404 Not Found`: Invalid task ID.
  - `500 Internal Server Error`: Internal failure.

AntiFold Service
----------------

**Blueprint Name**: ``antifold``  
**Base URL**: ``/antifold``

**POST /predict**  
Runs AntiFold prediction.

- **Request**:
  - `pdb_file` (file) or `pdb_url` (string)
  - `task_type` (string)
  - `heavy_chain`, `light_chain` (optional)
- **Response**:
  - `200 OK`: JSON result.
  - `400 Bad Request`: No file/URL.
  - `500 Internal Server Error`: Processing error.

**GET /check_status/<task_id>**  
Check AntiFold task status.

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and upload info.
  - `404 Not Found`: Task missing.
  - `500 Internal Server Error`: Failure.

ColabDock Service
-----------------

**Blueprint Name**: ``colabdock``  
**Base URL**: ``/colabdock``

**POST /dock**  
Run docking task.

- **Request**:
  - `pdb_file` (file) or `pdb_url` (string)
- **Response**:
  - `200 OK`: Docking results.
  - `400 Bad Request`: Input missing.
  - `500 Internal Server Error`: Docking failed.

**GET /check_status/<task_id>**  
Check docking task status.

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and files.
  - `404 Not Found`: Task not found.
  - `500 Internal Server Error`: Internal error.

Free-Wilson Service
-------------------

**Blueprint Name**: ``freewilson``  
**Base URL**: ``/freewilson``

**POST /run_analysis**  
Runs Free-Wilson analysis.

- **Request**:
  - `scaffold_file` / `scaffold_url`
  - `input_smiles_file` / `input_smiles_url`
  - `activity_file` / `activity_url`
  - `prefix` (optional)
- **Response**:
  - `200 OK`: JSON results.
  - `400 Bad Request`: Inputs missing.
  - `500 Internal Server Error`: Analysis failed.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and uploads.
  - `404 Not Found`: Task ID invalid.
  - `500 Internal Server Error`: Check failed.

LigandMPNN Service
------------------

**Blueprint Name**: ``ligandmpnn``  
**Base URL**: ``/ligandmpnn``

**POST /design**  
Starts LigandMPNN design.

- **Request**:
  - `pdb_file` / `pdb_file_url`
  - `chains_to_design` (string)
  - `fixed_residues`, `residues_to_design` (optional)
  - `temperature` (float), `number_of_batches` (int)
- **Response**:
  - `200 OK`: Design output.
  - `400 Bad Request`: Input issues.
  - `500 Internal Server Error`: Internal error.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and files.
  - `404 Not Found`: Task missing.
  - `500 Internal Server Error`: Check failed.

LocalColabFold API
------------------

**Blueprint Name**: ``localcolabfold``

**POST /predict**  
Runs structure prediction.

- **Request**:
  - `fasta_file` or `fasta_file_url`
- **Response**:
  - `200 OK`: Structure output.
  - `400 Bad Request`: Missing input.
  - `500 Internal Server Error`: Error occurred.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and Azure files.
  - `404 Not Found`: Task invalid.
  - `500 Internal Server Error`: Status error.

ParaSurf API
------------

**Blueprint Name**: ``parasurf``

**POST /predict**  
Run ParaSurf prediction.

- **Request**:
  - `pdb_file` or `pdb_url`
- **Response**:
  - `200 OK`: Surface output.
  - `400 Bad Request`: Missing input.
  - `500 Internal Server Error`: Internal failure.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and uploads.
  - `404 Not Found`: Task not found.
  - `500 Internal Server Error`: Status failure.

ProteinMPNN API
---------------

**Blueprint Name**: ``proteinmpnn``

**POST /ddg**  
Run ddG prediction.

- **Request**:
  - `pdb_file` / `pdb_file_url`
  - `chain` (default "A")
- **Response**:
  - `200 OK`: ddG results.
  - `400 Bad Request`: Input missing.
  - `500 Internal Server Error`: Prediction failure.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and files.
  - `404 Not Found`: Task ID missing.
  - `500 Internal Server Error`: Failure occurred.

REINVENT API
------------

**Blueprint Name**: ``reinvent``

**POST /predict**  
Runs REINVENT for generation.

- **Request**:
  - `smiles` (string)
- **Response**:
  - `200 OK`: Molecule data.
  - `400 Bad Request`: Missing SMILES.
  - `500 Internal Server Error`: Failure.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and files.
  - `404 Not Found`: Task invalid.
  - `500 Internal Server Error`: Check error.

ThermoMPNN API
--------------

**Blueprint Name**: ``thermompnn``

**POST /predict**  
Runs ThermoMPNN prediction.

- **Request**:
  - `task_type` (single, double, epistatic)
  - `pdb_file` or `pdb_file_url`
- **Response**:
  - `200 OK`: Prediction results.
  - `400 Bad Request`: Invalid input.
  - `500 Internal Server Error`: Prediction error.

**GET /check_status/<task_id>**

- **Parameters**:
  - `task_id` (string)
- **Response**:
  - `200 OK`: Logs and Azure outputs.
  - `404 Not Found`: Task not found.
  - `500 Internal Server Error`: Check failure.
