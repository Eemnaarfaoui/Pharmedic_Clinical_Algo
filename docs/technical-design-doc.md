# Pharmedic System – Technical Design Document

**Date:** July 2025  
**Authors:** Intern Team Raheel Sidiqui, Alagappan Alagappan, Fathima Arfa & Emna Arfaoui
**Version:** v0.1 (Draft)

---

##  1. Overview

This document outlines the technical design of the core module integration in the Pharmedic platform. It includes architecture choices, model explainability, and integration strategies for internal APIs.

---

##   2. System Architecture

### 2.1 Architecture Diagram

![System Architecture](./system-architecture.png)

### 2.2 Components

- **Model A – Model Name** (Raheel)
- **Model B – Model Name** (Fathima)
- **Model C – Model Name** (Alagappan)
- **Internal REST API Layer**
- **Mock Input/Output Interface**
- **Data Ingestion (CSV or API)**

---

##  3. Model Explainability

### 🟢 Model A – ADR Risk Classifier

- **Inputs:** SNPs (e.g., rs1799853), adverse drug history  
- **Outputs:** Risk level (e.g., “High”, “Moderate”, “Low”)  
- **Logic:**  
- **Use Case:** 
