=====================================================
Master test plan for Google cloud storage fuel plugin
=====================================================

Introduction
============

* Purpose

  This document describes Master Test Plan for GCS Fuel Plugin. The scope of
  this plan defines the following objectives:

  - describe testing activities;
  - outline testing approach, test types, test cycles that will be used;
  - test mission;
  - deliverables;

* Intended Audience

  This document is intended for GCS project team staff (QA and Dev engineers
  and managers) all other persons who are interested in testing results.

Governing Evaluation Mission
============================

GCS plugin for Fuel provides the functionality to add backup option to
Google Cloud for Mirantis OpenStack. It uses Fuel plugin architecture along
with pluggable architecture enhancements introduced in latest Mirantis
OpenStack Fuel.
The plugin must be compatible with the version 9.0 of Mirantis OpenStack.

* Evaluation Test Mission

  - Lab environment deployment.
  - Deploy MOS with developed plugin installed.
  - Create and run specific tests for plugin/deployment.
  - Documentation

* Test Items

  - GCS UI;
  - Fuel CLI;
  - Fuel API;
  - Fuel UI;
  - MOS;
  - MOS API.

Test Approach
=============

The project test approach consists of BVT, Integration/System, Regression and
Acceptance test levels.

* Criteria for test process starting

  Before test process can be started it is needed to make some preparation
  actions - to execute important preconditions. The following steps must be
  executed successfully for starting test phase:

  - all project requirements are reviewed and confirmed;
  - implementation of testing features has finished (a new build is ready for testing);
  - implementation code is stored in GIT;
  - bvt-tests are executed successfully (100% success);
  - test environment is prepared with correct configuration;
  - test environment contains the last delivered build for testing;
  - test plan is ready and confirmed internally;
  - implementation of manual tests and necessary autotests has finished.

* Suspension Criteria
  Testing of a particular feature is suspended if there is a blocking issue
  which prevents tests execution. Blocking issue can be one of the following:

  - Feature has a blocking defect, which prevents further usage of this feature
    and there is no workaround available;
  - CI test automation scripts failure.

* Feature Testing Exit Criteria
  Testing of a feature can be finished when:

  - All planned tests (prepared before) for the feature are executed; no
    defects are found during this run;
  - All planned tests for the feature are executed; defects found during this
    run are verified or confirmed to be acceptable (known issues);
  - The time for testing of that feature according to the project plan has run
    out and Project Manager confirms that no changes to the schedule are
    possible.

Deliverables
============

* List of deliverables
  Project testing activities are to be resulted in the following reporting
  documents:

  - Test plan;
  - Test run report;

* Acceptance criteria
  90% of tests cases should be with status - passed. Critical and high issues
  are fixed. Such manual tests should be executed and passed (100% of them):

  - Deploy cluster with GCS plugin enabled.

    - Boot VM with proper image.
    - Create a snapshot of recently booted vm.
    - Backup that snapshot on a GCS.
    - Destroy VM.
    - Download the snapshot from a GCS.
    - Boot VM with downloaded from GCS snapshot.

Test Cycle Structure
====================
An ordinary test cycle for each iteration consists of the following steps:

  - Smoke testing of each build ready for testing;
  - Verification testing of each build ready for testing;
  - Regression testing cycles in the end of iteration;
  - Creation of a new test case for covering of a new found bug (if such test
    does not exist).

  * Smoke Testing
    Smoke testing is intended to check a correct work of a system after new
    build delivery. Smoke tests allow to be sure that all main system
    functions/features work correctly according to customer requirements.

  * Verification testing
    Verification testing includes functional testing covering the following:

    - new functionality (implemented in the current build);
    - critical and major defect fixes (introduced in the current build).

    Some iteration test cycles also include non-functional testing types
    described in Overview of Planned Tests.

  * Regression testing
    Regression testing includes execution of a set of test cases for features
    implemented before current iteration to ensure that following modifications
    of the system haven't introduced or uncovered software defects. It also
    includes verification of minor defect fixes introduced in the current
    iteration.

  * Bug coverage by new test case
    Bug detection starts after all manual and automated tests are prepared and
    test process initiated. Ideally, each bug must be clearly documented and
    covered by test case. If a bug without a test coverage was found it must
    be clearly documented and covered by custom test case to prevent occurrence
    of this bug in future deployments/releases etc. All custom manual test
    cases suppose to be added into TestRail and automated tests suppose to be
    pushed to Git/Gerrit repo.

* Performance testing
  Performance testing will be executed on the scale lab and a custom set of
  Rally scenarios (or other performance tool) must be executed with GCS
  environment.

* Metrics
  Test case metrics are aimed to estimate a quality of bug fixing; detect not
  executed tests and schedule their execution. Passed / Failed test cases -
  this metric shows results of test cases execution, especially, a ratio
  between test cases passed successfully and failed ones. Such statistics must
  be gathered after each delivered build test. This will help to identify a
  progress in successful bugs fixing. Ideally, a count of failed test cases
  should aim to a zero.
  Not Run test cases - this metric shows a count of test cases which should be
  run within a current test phase (have not run yet). Having such statistics,
  there is an opportunity to detect and analyze a scope of not run test cases,
  causes of their non execution and planning of their further execution
  (detect time frames, responsible QA).

Test list
=========

* Block storage operations

  Tempest test cases executed by Rally tempest runner framework. Will execute
  all available scenarios.

* System tests

  * Install plugin and deploy environment (deploy_gcs_ha)

    - Upload plugin to the master node
    - Install plugin
    - Create cluster
    - Add 3 nodes with controller role
    - Add 1 node with compute role
    - Add 1 node with cinder role
    - Deploy the cluster
    - Run network verification
    - Check plugin installation
    - Run OSTF

    Expected Result:

    - OSTF passes successfully

  * Remove, add controller in cluster with plugin
    (deploy_gcs_ha_remove_add_controller)

    - Upload plugin to the master node
    - Install plugin
    - Create cluster
    - Add 3 controllers and 1 compute and 1 cinder node
    - Deploy the cluster
    - Run OSTF
    - Remove 1 controller
    - Deploy changes
    - Run OSTF
    - Add 1 controller
    - Deploy changes
    - Run OSTF

    Expected Result

    - OSTF passes successfully

  * Remove, add compute in cluster with plugin
    (deploy_gcs_ha_remove_add_compute)

    - Upload plugin to the master node
    - Install plugin
    - Create cluster
    - Add 3 controllers, 2 computes and 1 cinder node
    - Deploy the cluster
    - Run OSTF
    - Remove 1 compute node
    - Deploy changes
    - Run OSTF
    - Add 1 compute
    - Deploy cluster
    - Run OSTF

    Expected Result

    - OSTF passes successfully

  * Remove, add cinder in cluster with plugin
    (deploy_gcs_ha_remove_add_cinder)

    - Upload plugin to the master node
    - Install plugin
    - Create cluster
    - Add 3 controllers, 1 compute and 2 cinder nodes
    - Deploy the cluster
    - Run OSTF
    - Remove 1 cinder node
    - Deploy changes
    - Run OSTF
    - Add 1 cinder node
    - Deploy cluster
    - Run OSTF

    Expected Result

    - OSTF passes successfully

* Functional tests

  * Backup Volume and reattach it to the VM (reattach_backupped_vol_from_gcs)

    - Boot server
    - Create and attach volume to the server
    - Backup volume
    - Detach and delete volume
    - Restore volume from GCS backup
    - Attach volume

    Expected Result

    - VM Active, Volume active and attached

  * Write/Read data to/from volume (test_volume_data_integrity_after_backup)

    - Boot server
    - Create volume
    - Attach volume to a instance
    - Mount, make filesystem
    - Write test data
    - Unmount
    - Backup volume on the GCS
    - Detach and delete volume
    - Restore volume from GCS backup and attach it to a instance
    - Mount volume
    - Check test data

    Expected Result

    - Test data is available and accurate
