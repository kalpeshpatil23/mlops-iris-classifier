# DVC Workflow

## 1. Objective

This experiment demonstrates dataset versioning using Data Version Control (DVC) integrated with Git.

The Iris dataset was tracked using DVC, stored in a local DVC remote, and different dataset versions were compared and restored.

## 2. DVC Remote Configuration

A local folder was used as the DVC remote storage.

The remote was configured using:

```bash
dvc remote add -d myremote ~/dvc-remote-storage
