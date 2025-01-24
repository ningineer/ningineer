# Multi-Region S3 Backup Implementation

## ⚠️ Disclaimer
This project is intended solely for educational and security best practice purposes within authorized AWS environments. Ensure proper permissions before implementing these configurations in a production environment.

## Project Overview
- **Technology Used:** AWS S3, AWS S3 Replication, AWS KMS, AWS Lambda, AWS CloudWatch, AWS IAM
- **Purpose:** Enable automated, cross-region S3 backups to improve data durability and disaster recovery.
- **Output:** A fully functional multi-region S3 backup solution with encryption, monitoring, and lifecycle policies.

## Prerequisites
- AWS Account with administrative privileges
- Two S3 buckets in different AWS regions
- IAM Role with necessary permissions
- AWS CLI configured or AWS Console access

## Setup and Implementation
### Step 1: Create Source and Destination S3 Buckets
#### 1. Create Source S3 Bucket
```sh
aws s3api create-bucket --bucket source-bucket-name --region us-east-1 --create-bucket-configuration LocationConstraint=us-east-1
```

#### 2. Create Destination S3 Bucket
```sh
aws s3api create-bucket --bucket destination-bucket-name --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
```

### Step 2: Enable Versioning on Both Buckets
```sh
aws s3api put-bucket-versioning --bucket source-bucket-name --versioning-configuration Status=Enabled
aws s3api put-bucket-versioning --bucket destination-bucket-name --versioning-configuration Status=Enabled
```

### Step 3: Set Up Cross-Region Replication (CRR)
#### 1. Create IAM Role for Replication
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "s3.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}
```

#### 2. Attach IAM Policy for Replication
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ReplicateObject",
                "s3:ReplicateDelete",
                "s3:ReplicateTags"
            ],
            "Resource": [
                "arn:aws:s3:::source-bucket-name/*",
                "arn:aws:s3:::destination-bucket-name/*"
            ]
        }
    ]
}
```

#### 3. Configure Replication Rule
```json
{
    "Role": "arn:aws:iam::account-id:role/replication-role",
    "Rules": [
        {
            "Status": "Enabled",
            "Priority": 1,
            "DeleteMarkerReplication": {"Status": "Enabled"},
            "Filter": {},
            "Destination": {
                "Bucket": "arn:aws:s3:::destination-bucket-name",
                "StorageClass": "STANDARD"
            }
        }
    ]
}
```

### Step 4: Enable Server-Side Encryption with AWS KMS
#### 1. Create a KMS Key
```sh
aws kms create-key --description "S3 Backup Encryption Key"
```
#### 2. Apply Encryption to Both Buckets
```json
{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "your-kms-key-id"
            }
        }
    ]
}
```

### Step 5: Monitor Backup with CloudWatch and EventBridge
#### 1. Enable CloudWatch Metrics for S3
```sh
aws s3api put-bucket-metrics-configuration --bucket source-bucket-name --id replication-metrics --metrics-configuration '{"Id": "replication-metrics"}'
```
#### 2. Create an EventBridge Rule for Replication Status
```json
{
    "Source": ["aws.s3"],
    "DetailType": ["AWS API Call via CloudTrail"],
    "Detail": {
        "eventSource": ["s3.amazonaws.com"],
        "eventName": ["ReplicateObject"]
    }
}
```

### Step 6: Automate Backup Validation with AWS Lambda
#### 1. Create Lambda Function to Verify Backups
```python
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    source_bucket = "source-bucket-name"
    destination_bucket = "destination-bucket-name"
    
    source_objects = s3.list_objects_v2(Bucket=source_bucket)['Contents']
    destination_objects = s3.list_objects_v2(Bucket=destination_bucket)['Contents']
    
    source_keys = {obj['Key'] for obj in source_objects}
    destination_keys = {obj['Key'] for obj in destination_objects}
    
    missing_files = source_keys - destination_keys
    if missing_files:
        print(f"Missing files: {missing_files}")
    else:
        print("All files successfully replicated.")
```

## Validation & Testing
- **Check replication status** in the AWS Console (S3 Replication Metrics).
- **Manually upload a file** to the source bucket and verify replication to the destination bucket.
- **Trigger AWS Lambda function** to validate replicated files.

## Key Features
- **Automated Multi-Region Backup:** Ensures data redundancy.
- **Cross-Region Replication:** Immediate synchronization.
- **Server-Side Encryption:** Secures data at rest.
- **Monitoring & Alerts:** CloudWatch, EventBridge, Lambda validation.

## Future Enhancements
- Implement **S3 Intelligent-Tiering** for cost optimization.
- Use **Amazon S3 Glacier** for long-term archival.
- Configure **AWS Backup** for centralized backup management.

## Conclusion
Implementing a multi-region S3 backup enhances data resilience and disaster recovery. With encryption, monitoring, and automated validation, this solution ensures critical data remains available even in case of regional failures.

## References
- AWS S3 Documentation: [Amazon S3](https://docs.aws.amazon.com/s3/)
- AWS KMS Guide: [AWS KMS](https://docs.aws.amazon.com/kms/)
