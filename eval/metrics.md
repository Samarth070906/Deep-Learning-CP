# TrustAgent Evaluation Metrics

This document defines the evaluation metrics for every stage of the TrustAgent pipeline.

## 1. Claim Extraction
- **Metric**: F1-Score of extracted claims vs. ground truth annotations.
- **Description**: Measures the accuracy of extracting verifiable atomic claims from input text.

## 2. Evidence Retrieval
- **Metric**: MRR@3 (Mean Reciprocal Rank) / Recall@3
- **Description**: Measures the ability of the FAISS index to retrieve the correct supporting/contradicting evidence in the top 3 results.

## 3. Text Verifier
- **Metric**: Accuracy and F1-Score
- **Description**: Evaluates the DeBERTa NLI model on classifying text pairs into SUPPORT, CONTRADICT, or NO_EVIDENCE.

## 4. Image Verifier
- **Metric**: Accuracy and F1-Score
- **Description**: Evaluates the CLIP-based verifier. Explicitly accounts for handling of NO_EVIDENCE when `visually_verifiable` is False or the image is missing/invalid.

## 5. MultiModalConsistencyNet
- **Metric**: Precision, Recall, F1-Score, and Calibration Curve
- **Description**: Measures the network's ability to correctly predict consistency based on inputs (text_score, image_score, num_modalities_available, pairwise_disagreement_flag). Precision/Recall are measured particularly for contradiction detection.

## 6. TrustScoreNet
- **Metric**: Pearson/Spearman Correlation and MAE (Mean Absolute Error)
- **Description**: Evaluates the final continuous trust score's alignment with human-annotated trust levels.

## 7. End-to-End Decision Accuracy
- **Metric**: Overall Accuracy / F1-Score
- **Description**: Measures the correctness of the final verification decision (e.g., Trusted, Flagged, Needs Review) across the entire pipeline.
