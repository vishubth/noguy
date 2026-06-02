# NoGuy - Cryptocurrency Token Sale Operations Platform

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-green)
![Blockchain](https://img.shields.io/badge/domain-Web3-orange)
![Backend](https://img.shields.io/badge/focus-Backend%20Systems-black)

## Overview

NoGuy is a cryptocurrency token sale operations platform designed to support investor onboarding, payment verification, token allocation workflows, transaction tracking, and administrative operations management.

The platform was developed to streamline token sale activities by combining blockchain payment validation, investor account management, real-time pricing integration, and operational dashboards into a unified workflow.

---

## Business Problem

Token sale operations often require teams to manually:

- verify blockchain transactions
- calculate token allocations
- track investor purchases
- manage payment confirmations
- monitor fundraising activity
- provide investor visibility

This platform automates those operational workflows through a centralized application layer.

---

## Core Platform Capabilities

### Investor Operations

- token purchase workflows
- wallet-based transaction tracking
- purchase history management
- allocation visibility
- investor dashboard experience

### Payment Verification

- Ethereum transaction verification
- blockchain payment confirmation
- Etherscan integration
- transaction validation workflows
- payment status tracking

### Token Allocation Engine

- dynamic allocation calculations
- ETH conversion support
- configurable token distribution logic
- bonus allocation support

### Administrative Operations

- transaction monitoring
- purchase management
- investor record management
- operational reporting
- fundraising visibility

---

## System Architecture

```text
Investor Interface
        ↓
FastAPI Application Layer
        ↓
Purchase Processing Engine
        ↓
Blockchain Verification Services
        ↓
Allocation & Tracking Engine
        ↓
Administrative Dashboard
```

---

## Technical Components

### Backend

- FastAPI
- Python
- REST APIs
- Session Management

### Data Layer

- SQLite
- Transaction Persistence
- Purchase Records

### Blockchain Integration

- Ethereum Transaction Validation
- Etherscan API
- Wallet Verification
- Payment Confirmation Workflows

### Frontend

- Jinja2 Templates
- Dashboard Interfaces
- Administrative Views

---

## Engineering Highlights

This project demonstrates practical implementation experience in:

- backend systems engineering
- financial transaction workflows
- blockchain integrations
- API design
- administrative operations tooling
- payment verification systems
- database-backed applications
- operational dashboard development

---

## Repository Structure

```text
static/
templates/
main.py
requirements.txt
```

The current repository represents a client-delivery implementation and serves as a reference architecture for token sale operations workflows.

---

## Future Architecture Evolution

Planned modernization areas include:

```text
src/
├── api/
├── services/
├── database/
├── models/
├── admin/
└── config/
```

Potential improvements:

- service-layer separation
- SQLAlchemy integration
- environment-based configuration
- automated testing
- CI/CD pipelines
- containerized deployment
- observability and monitoring

---

## Portfolio Relevance

This project highlights experience building operational systems that combine:

- Web3 infrastructure
- transaction processing
- financial workflow automation
- backend application development
- dashboard-driven operations management

It demonstrates the intersection of software engineering, blockchain integrations, and business operations tooling.
