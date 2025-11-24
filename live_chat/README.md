
# Global Data Science Challenge 2025

This file explains the architecture and how to use the Global Data Science Challenge 2025 project.

## Architecture
This project is currently designed as a Proof of Concept based on a series of notebooks that can be executed one after the other.
Each notebook executes a step needed to iterate through user interaction.

## List of Notebooks
### Training Information Extraction and Classification
This category of notebooks includes preparation steps. Once executed, they don't need to be run before each interview.

#### N1.1_trainings_parsing
Extract title and short description for each training

#### N1.2_trainings_clustering
Group trainings in domain clusters using sentence_transformers and K-means
Group trainings in trainin skills clusters using sentence_transformers and K-means

#### N1.3_trainings_clusters_labeling
This notebook computes human-readable labels for each training cluster. These labels help interpret the clustering results and improve the explainability of the recommendation system.

#### N1.4_trainings_final_labeling
This step updates the original training data with the computed cluster labels, enabling downstream tasks to use enriched training metadata.

### Job Information Extraction and Classification
#### N2.1_jobs_parsing
Extracts structured information from job descriptions. This includes job titles, responsibilities, and required skills.

#### N2.2_jobs_clustering
Jobs are grouped into clusters using sentence transformers and K-means, similar to the training clustering process. This helps identify job families and common skill sets.

#### N2.3_jobs_clusters_labeling
Generates labels for each job cluster to make them interpretable and usable in recommendations.

#### N2.4_jobs_skill_domains_classification
Tags each job with related skill domains, enabling better matching with training clusters.

#### N2.5_match_jobs_trainings
Maps skills between jobs and trainings to identify which trainings are relevant for each job.

#### N2.6_jobs_short_description
Adds a short, user-friendly description to each job to improve readability and user engagement during interviews.

### Initial Interviews
#### N3.1_initial_interviews
Collects initial persona information such as interests, age, and city. This is the first step in building a personalized recommendation.

#### N3.2_initial_personas_infos
Processes and extracts structured data from the initial interview responses.

### Job Extension Interviews
#### N5.1_job_extension_interviews
Extends the interview to refine the persona’s targeted activity domain. Includes logic to detect and handle age misreporting.

#### N5.2_job_recommandation_consolidation
Refreshes persona recommendations, updated goals, location, and education level.

#### N5.3_job_personas_infos
Extracts and cleans persona data related to targeted activity domains and location diversity.

#### N5.4_persona_age_consolidation
Handles specific cases where young users may have misreported their age, ensuring accurate profiling.

### Compute Proposed Jobs
#### N6_compute_proposed_jobs
Generates a list of proposed jobs for each persona based on their profile and preferences.

### Job Feedback Interview
#### N7.1_interviews_update_for_jobs
Extends the interview to present selected job options to the persona and gather feedback.

#### N7.2_refresh_personas_infos_jobs
Reevaluates persona interest in jobs and extracts updated skill information.

### Training Extension Interviews
#### N8.1_training_domain_extension_interviews
Extends the interview to gather persona preferences for training domains.

#### N8.2_training_skills_extension_interviews
Collects feedback on proposed trainings and evaluates proficiency levels. Also reevaluates interest in training domains.

#### N8.3_training_personas_infos
Extracts persona skills and proficiency levels, and updates training interest data.

### Prepare Submission
#### N10_prepare_submission
Final step that matches personas with jobs and trainings. Constructs the submission file for the challenge.


