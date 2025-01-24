# Zero-Trust Security Model Implementation in AWS

## ⚠️ Disclaimer
This project is intended solely for educational and security best practice purposes within authorized AWS environments. Unauthorized security testing or policy enforcement may lead to unintended consequences. Ensure you have permission before implementing these configurations in a production environment.

## Project Overview
- **Technology Used:** AWS IAM, AWS Security Hub, AWS GuardDuty, AWS WAF, AWS Systems Manager, AWS KMS, AWS Config, AWS CloudTrail
- **Purpose:** Implement a Zero-Trust security model in AWS by enforcing strict identity verification, network segmentation, and continuous monitoring.
- **Output:** A secure AWS environment following Zero-Trust principles with automated security policies and compliance enforcement.

## Prerequisites
- AWS Account with administrative access
- Knowledge of AWS Security Tools (AWS WAF, AWS Shield, AWS IAM, AWS Organizations, AWS VPC, AWS Config)
- Understanding of Zero-Trust principles and best practices

## Setup and Implementation
### Step 1: Define and Enforce Identity-Based Access Control
#### 1. Implement IAM Least Privilege Access
- Create an IAM role with **only the necessary permissions**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```
- Assign IAM roles instead of users for applications and services.
- Use **IAM Access Analyzer** to detect overly permissive policies.

#### 2. Enforce Multi-Factor Authentication (MFA)
- Enable MFA for all users using AWS CLI:
```sh
aws iam update-login-profile --user-name AdminUser --password-reset-required
```
- Require MFA in IAM policies:
```json
{
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
        "BoolIfExists": {
            "aws:MultiFactorAuthPresent": "false"
        }
    }
}
```

#### 3. Use AWS IAM Identity Center (SSO)
- Enable AWS SSO via AWS Organizations.
- Configure **Federated Authentication** using an Identity Provider (Okta, Azure AD).

### Step 2: Secure Network and Workloads with Micro-Segmentation
#### 1. Use AWS VPC with Private Subnets
- Create a private subnet using AWS CLI:
```sh
aws ec2 create-subnet --vpc-id vpc-xxxxxxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
```

#### 2. Implement AWS Network Firewall
- Enable **AWS Network Firewall** and configure rules for inbound and outbound traffic.
- Sample firewall rule:
```json
{
    "RuleVariables": {},
    "RulesSource": {
        "RulesString": "alert tcp any any -> any any (msg:\"TCP packet detected\"; sid:1;)"
    }
}
```

### Step 3: Implement Continuous Monitoring and Threat Detection
#### 1. Enable AWS GuardDuty
```sh
aws guardduty create-detector --enable
```
#### 2. Enable AWS Security Hub
```sh
aws securityhub enable-security-hub
```
#### 3. Set up AWS CloudTrail Logging
```sh
aws cloudtrail create-trail --name ZeroTrustTrail --s3-bucket-name my-cloudtrail-logs
```

### Step 4: Secure Endpoints and Enforce Device Compliance
#### 1. Use AWS Systems Manager Session Manager
```sh
aws ssm start-session --target instance-id
```
#### 2. Enforce Compliance Policies with AWS Systems Manager State Manager
```sh
aws ssm create-association --name "AWS-UpdateSSMAgent" --targets "Key=InstanceIds,Values=i-xxxxxx"
```

### Step 5: Implement Data Protection Mechanisms
#### 1. Encrypt Data Using AWS KMS
- Create a KMS key:
```sh
aws kms create-key --description "Zero Trust Encryption Key"
```
- Encrypt an S3 object using KMS:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": "aws:kms"
                }
            }
        }
    ]
}
```

### Step 6: Automate Incident Response
#### 1. Create Automated Response Workflows
- Use AWS Lambda to remediate security risks automatically.
```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.revoke_security_group_ingress(
        GroupId='sg-xxxxxxxx',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        CidrIp='0.0.0.0/0'
    )
    return response
```
#### 2. Configure AWS Config Rules for Auto-Remediation
```sh
aws configservice put-config-rule --config-rule file://deny-open-security-groups.json
```

## Validation & Testing
- **Test IAM policies** using **IAM Policy Simulator**.
- **Analyze VPC Flow Logs** to detect unauthorized access.
- **Trigger GuardDuty findings** using AWS pre-defined test events.
```sh
aws guardduty create-sample-findings --detector-id detector-id
```

## Key Features
- **Strict Identity Access Control:** IAM least privilege, MFA enforcement.
- **Network Segmentation:** Private subnets, security groups, AWS Firewall.
- **Continuous Monitoring:** GuardDuty, Security Hub, CloudTrail, AWS Config.
- **Automated Remediation:** AWS Lambda, AWS Config Rules, EventBridge.

## Future Enhancements
- Integrate **AWS Control Tower** for multi-account security.
- Deploy **Zero-Trust Network Access (ZTNA)** using AWS PrivateLink.
- Utilize **Machine Learning-Based Anomaly Detection** with Amazon SageMaker.

## Conclusion
By implementing Zero-Trust in AWS, organizations can significantly enhance their security posture, reducing the attack surface and ensuring continuous monitoring and compliance. This approach enforces strict access controls, network segmentation, real-time threat detection, and automated remediation to mitigate security risks effectively.

## References
- AWS Security Best Practices: [AWS Security Documentation](https://docs.aws.amazon.com/security/)
- AWS Zero-Trust Whitepaper: [AWS Zero Trust](https://aws.amazon.com/security/zero-trust/)
