# AWS Control Tower for Enterprise Governance & Security

## ⚠️ Disclaimer
This project is intended solely for educational and security best practice purposes within authorized AWS environments. Ensure proper permissions before implementing these configurations in a production environment.

## Project Overview
- **Technology Used:** AWS Control Tower, AWS Organizations, AWS IAM, AWS SCPs, AWS Config, AWS Security Hub
- **Purpose:** Implement AWS Control Tower to enforce governance, security, and compliance across multiple AWS accounts.
- **Output:** A well-structured multi-account AWS environment with automated security controls and compliance monitoring.

## Prerequisites
- AWS Organization with management account access
- Permissions to enable AWS Control Tower
- IAM Role with required administrative privileges

## Setup and Implementation
### Step 1: Enable AWS Control Tower
#### 1. Navigate to AWS Control Tower Console
- Sign in to the AWS Management Console
- Go to **AWS Control Tower** service
- Click **Set up landing zone**

#### 2. Configure Organizational Units (OUs)
- Create Organizational Units (OUs) for different environments (e.g., **Security**, **Infrastructure**, **Development**, **Production**)
- Assign AWS accounts to respective OUs

### Step 2: Implement Guardrails and Security Policies
#### 1. Enable Preventive and Detective Guardrails
- **Preventive Guardrails:** Enforce security baselines (e.g., restrict public S3 buckets, enforce MFA)
- **Detective Guardrails:** Monitor compliance with AWS Config and Security Hub

#### 2. Apply Service Control Policies (SCPs)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "s3:PutBucketPublicAccessBlock",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": "us-east-1"
                }
            }
        }
    ]
}
```

### Step 3: Configure AWS Security Hub & AWS Config
#### 1. Enable AWS Security Hub
```sh
aws securityhub enable-security-hub
```
#### 2. Enable AWS Config for Compliance Audits
```sh
aws configservice put-configuration-recorder --configuration-recorder "name=default,roleARN=arn:aws:iam::account-id:role/config-role"
```

### Step 4: Implement IAM Identity Center (AWS SSO)
#### 1. Enable AWS IAM Identity Center
- Navigate to AWS IAM Identity Center
- Configure user access and permissions

#### 2. Define Permission Sets for Different Roles
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        }
    ]
}
```

### Step 5: Automate Security Monitoring with AWS Lambda
#### 1. Create Lambda Function to Detect Non-Compliant Resources
```python
import boto3

def lambda_handler(event, context):
    client = boto3.client('config')
    response = client.describe_compliance_by_config_rule()
    for rule in response['ComplianceByConfigRules']:
        if rule['Compliance']['ComplianceType'] != 'COMPLIANT':
            print(f"Non-compliant rule: {rule['ConfigRuleName']}")
```

## Validation & Testing
- Verify AWS Control Tower landing zone setup
- Check SCPs applied to Organizational Units
- Test IAM Identity Center role assignments
- Ensure AWS Config compliance reports are generated

## Key Features
- **Automated Multi-Account Governance**
- **Enforced Security Policies with SCPs**
- **Continuous Compliance Monitoring with AWS Config**
- **Centralized Security Visibility with Security Hub**

## Future Enhancements
- Integrate AWS Audit Manager for compliance reporting
- Implement AWS Security Hub findings automation with EventBridge
- Extend IAM Identity Center to federate with enterprise identity providers

## Conclusion
AWS Control Tower simplifies governance and security enforcement in multi-account AWS environments. By leveraging SCPs, AWS Config, and AWS Security Hub, enterprises can achieve scalable and secure cloud operations.

## References
- AWS Control Tower Documentation: [AWS Control Tower](https://docs.aws.amazon.com/controltower/)
- AWS Security Hub Guide: [AWS Security Hub](https://docs.aws.amazon.com/securityhub/)
