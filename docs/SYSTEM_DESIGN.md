# Digital Asset Fundraising Operations Platform

## System Overview

This platform supports investor onboarding, fundraising operations, payment verification, allocation management and administrative reporting.

## Core Components

### Investor Portal
- Purchase workflow
- Wallet registration
- Allocation visibility

### Payment Verification Service
- Etherscan integration
- Transaction validation
- Confirmation processing

### Allocation Engine
- ETH conversion
- Token allocation calculations
- Bonus allocation support

### Administrative Operations
- Investor management
- Transaction oversight
- Fundraising reporting

## Future Architecture

```text
src/
├── api/
├── services/
├── database/
├── schemas/
├── integrations/
└── config/
```

## Event Model

PurchaseCreated
PaymentSubmitted
PaymentVerified
AllocationCalculated
InvestorUpdated
ReportGenerated