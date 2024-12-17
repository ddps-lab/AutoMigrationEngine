## Migration Experiment Automation
* Process Migration Experiment Automation
* Automatic Detection of Process Correctness and Debugging for Abnormal Termination After Migration

### 1. Experiment Set Configuration

1.	/data_processing_for_lscpu/entire/CreateAllCpuFeature.py
    * Removes CPU features that are either universally present or absent across all instances.
2.	/data_processing_for_lscpu/entire/GroupByAWS.py
    * Groups instances with identical CPU features.
3.	/data_processing_for_lscpu/entire/SimplizedAwsGroup(all).py
    * Excludes instances that are excessively large or small.
4.	/data_processing_for_lscpu/entire/MinimizedAwsGroup(all).py
    * Selects the most cost-effective instances within each group.

### 2. Install LiveMigrate-Detector

Clone LiveMigrate-Detector into the experiment environment.

git clone https://github.com/ddps-lab/LiveMigrate-Detector.git

### 3. Infrastructure Configuration

1.	Update /infrastructure/*/variables.tf
    * Set region, key, AMI ID, and other parameters.

### 4. Experiment Execution

1.	/ExternalMigration(all of cases).py
    * Performs migration experiments across instance groups.
2.	/ExternalMigration(re-experiment).py
    * Automatically detects and re-executes missing experiment cases, such as failed instance creation.
3.	/InternalMigration.py
    * Conducts migration experiments between instances within the same group with identical CPU features.