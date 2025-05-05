# BioTasks API
 
 ## Overview
 The BioTasks API provides endpoints for running various protein design and prediction tasks, including **AntiFold**, **LigandMPNN**, and **ProteinMPNN**. Users can submit PDB files and request different types of predictions.
 
 ## Base URL
 ```
 http://your-server-ip/v1/api
 ```
 
 ## API Endpoints
 
 ### AntiFold Prediction
 - **POST `/antifold/predict`**: Starts AntiFold to predict protein structures
 - **GET `/antifold/check_status/<task_id>`**: Check if AntiFold has finished running
 
 ### LigandMPNN Protein Design
 - **POST `/ligandmpnn/design`**: Starts LigandMPNN for protein design
 - **GET `/ligandmpnn/check_status/<task_id>`**: Check if LigandMPNN has finished running
 
 ### ProteinMPNN ddG Prediction
 - **POST `/proteinmpnn/ddg`**: Starts ProteinMPNN to predict ddG changes for mutations
 - **GET `/proteinmpnn/check_status/<task_id>`**: Check if ProteinMPNN has finished running
 
 ### List Available Tasks
 - **GET `/tasks/`**: Returns a list of available tasks in the API
 
 ## Detailed Documentation
 
 ### 1. AntiFold Prediction
 
 #### 1.1 Predict Protein Structure
 **Endpoint:** `POST /antifold/predict`
 
 **Form Data Parameters:**
 | Parameter       | Type   | Required | Description                     |
 |----------------|--------|----------|---------------------------------|
 | `task_type`    | string | No       | Type of prediction task        |
 | `heavy_chain`  | string | No       | Heavy chain specification      |
 | `light_chain`  | string | No       | Light chain specification      |
 | `pdb_file`     | file   | Yes      | PDB file for the prediction    |
 
 **Example Response:**
 ```json
 {
   "task_id": "123e4567-e89b-12d3-a456-426614174000",
   "message": "AntiFold started"
 }
 ```
 
 #### 1.2 Check Prediction Status
 **Endpoint:** `GET /antifold/check_status/<task_id>`
 
 **Example Response:**
 ```json
 {
   "task_id": "123e4567-e89b-12d3-a456-426614174000",
   "logs": [
     "AntiFold process started...",
     "Processing PDB file...",
     "Prediction completed successfully."
   ]
 }
 ```
 
 ### 2. LigandMPNN Protein Design
 
 #### 2.1 Design Protein with LigandMPNN
 **Endpoint:** `POST /ligandmpnn/design`
 
 **Form Data Parameters:**
 | Parameter            | Type   | Required | Description                      |
 |----------------------|--------|----------|----------------------------------|
 | `pdb_file`          | file   | Yes      | PDB file for design             |
 | `chains_to_design`  | string | Yes      | Chains to be designed           |
 | `fixed_residues`    | string | No       | Fixed residues                   |
 | `residues_to_design` | string | No      | Residues to redesign            |
 | `temperature`       | float  | No       | Temperature setting (default 0.1) |
 | `number_of_batches` | int    | No       | Number of batches (default 8)    |
 
 **Example Response:**
 ```json
 {
   "message": "LigandMPNN started",
   "task_id": "123e4567-e89b-12d3-a456-426614174000",
   "log_file": "ligandmpnn_output/123e4567-e89b-12d3-a456-426614174000.log",
   "output_folder": "ligandmpnn_output"
 }
 ```
 
 #### 2.2 Check LigandMPNN Status
 **Endpoint:** `GET /ligandmpnn/check_status/<task_id>`
 
 **Example Response:**
 ```json
 {
   "task_id": "123e4567-e89b-12d3-a456-426614174000",
   "logs": [
     "Designing protein from this path: /uploads/example.pdb",
     "Residues redesigned: ['A1', 'A2', 'A3']",
     "Design completed successfully."
   ]
 }
 ```
 
 ### 3. ProteinMPNN ddG Prediction
 
 #### 3.1 Run ProteinMPNN ddG Prediction
 **Endpoint:** `POST /proteinmpnn/ddg`
 
 **Form Data Parameters:**
 | Parameter  | Type   | Required | Description                  |
 |------------|--------|----------|------------------------------|
 | `pdb_file` | file   | Yes      | PDB file for ddG prediction |
 | `chain`    | string | No       | Chain to be analyzed (default "A") |
 
 **Example Response:**
 ```json
 {
   "message": "ProteinMPNN started",
   "task_id": "987e6543-e89b-12d3-a456-426614174000",
   "log_file": "proteinmpnn_output/987e6543-e89b-12d3-a456-426614174000.log",
   "output_folder": "proteinmpnn_output"
 }
 ```
 
 #### 3.2 Check ProteinMPNN Status
 **Endpoint:** `GET /proteinmpnn/check_status/<task_id>`
 
 **Example Response:**
 ```json
 {
   "task_id": "987e6543-e89b-12d3-a456-426614174000",
   "logs": [
     "Processing PDB file...",
     "Running ProteinMPNN model...",
     "ddG predictions completed."
   ]
 }
 ```
 
 ## Error Handling
 | Error Code | Meaning | Possible Causes |
 |------------|---------|----------------|
 | 400        | Bad Request | Missing required parameters |
 | 404        | Not Found | Task ID does not exist |
 | 500        | Internal Server Error | Unexpected backend failure |
 
 ## Usage Notes
 - Send PDB files as **multipart/form-data** when using tools like Postman
 - Optional parameters have default values that will be used if not explicitly provided
 - The API is asynchronous - after submitting a task, check its status using the corresponding status endpoint
 - All task IDs should be retained for checking status and retrieving results
 