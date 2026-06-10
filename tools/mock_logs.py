MOCK_EVENTS = [

    {
        "event_time": "2026-06-09 09:00:00",
        "event_name": "DescribeInstances",
        "event_source": "ec2.amazonaws.com",
        "username": "ops-team-sarah",
        "source_ip": "10.0.1.50",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 09:05:12",
        "event_name": "ListBuckets",
        "event_source": "s3.amazonaws.com",
        "username": "ops-team-sarah",
        "source_ip": "10.0.1.50",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 09:10:30",
        "event_name": "AssumeRole",
        "event_source": "sts.amazonaws.com",
        "username": "N/A",
        "source_ip": "config.amazonaws.com",
        "error_code": None,
        "request_parameters": {
            "roleArn": "arn:aws:iam::160282065513:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig"
        }
    },

    {
        "event_time": "2026-06-09 10:15:44",
        "event_name": "GetLogEvents",
        "event_source": "logs.amazonaws.com",
        "username": "dev-user-amira",
        "source_ip": "10.0.1.72",
        "error_code": None,
        "request_parameters": {
            "logGroupName": "/aws/lambda/order-processing"
        }
    },

    {
        "event_time": "2026-06-09 11:00:00",
        "event_name": "DescribeTrails",
        "event_source": "cloudtrail.amazonaws.com",
        "username": "N/A",
        "source_ip": "cloudtrail.amazonaws.com",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 02:58:10",
        "event_name": "ConsoleLogin",
        "event_source": "signin.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": "Failed authentication",
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 03:01:33",
        "event_name": "ConsoleLogin",
        "event_source": "signin.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": "Failed authentication",
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 03:05:48",
        "event_name": "ConsoleLogin",
        "event_source": "signin.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 03:10:05",
        "event_name": "ListSecrets",
        "event_source": "secretsmanager.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 03:14:22",
        "event_name": "GetSecretValue",
        "event_source": "secretsmanager.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {
            "secretId": "prod/database/master-password"
        }
    },

    {
        "event_time": "2026-06-09 03:19:30",
        "event_name": "StopLogging",
        "event_source": "cloudtrail.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {
            "name": "management-events-trail"
        }
    },

    {
        "event_time": "2026-06-09 03:21:45",
        "event_name": "DeleteTrail",
        "event_source": "cloudtrail.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {
            "name": "management-events-trail"
        }
    },

    {
        "event_time": "2026-06-09 03:25:10",
        "event_name": "AttachUserPolicy",
        "event_source": "iam.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {
            "userName": "dev-user-john",
            "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
        }
    },

    {
        "event_time": "2026-06-09 03:30:55",
        "event_name": "CreateUser",
        "event_source": "iam.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {
            "userName": "backup-svc-account"
        }
    },

    {
        "event_time": "2026-06-09 03:31:30",
        "event_name": "CreateAccessKey",
        "event_source": "iam.amazonaws.com",
        "username": "dev-user-john",
        "source_ip": "45.33.32.156",
        "error_code": None,
        "request_parameters": {
            "userName": "backup-svc-account"
        }
    },

    {
        "event_time": "2026-06-09 03:35:02",
        "event_name": "PutBucketPolicy",
        "event_source": "s3.amazonaws.com",
        "username": "backup-svc-account",
        "source_ip": "45.33.32.156",
        "error_code": "AccessDenied",
        "request_parameters": {
            "bucketName": "company-financial-records"
        }
    },

    {
        "event_time": "2026-06-09 03:36:40",
        "event_name": "PutBucketPolicy",
        "event_source": "s3.amazonaws.com",
        "username": "backup-svc-account",
        "source_ip": "45.33.32.156",
        "error_code": "AccessDenied",
        "request_parameters": {
            "bucketName": "customer-pii-backups"
        }
    },

    {
        "event_time": "2026-06-09 14:20:15",
        "event_name": "UpdateFunctionCode",
        "event_source": "lambda.amazonaws.com",
        "username": "dev-user-amira",
        "source_ip": "10.0.1.72",
        "error_code": None,
        "request_parameters": {
            "functionName": "order-processing"
        }
    },

    {
        "event_time": "2026-06-09 15:05:50",
        "event_name": "GetMetricData",
        "event_source": "monitoring.amazonaws.com",
        "username": "ops-team-sarah",
        "source_ip": "10.0.1.50",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-06-09 16:00:00",
        "event_name": "AssumeRole",
        "event_source": "sts.amazonaws.com",
        "username": "N/A",
        "source_ip": "resource-explorer-2.amazonaws.com",
        "error_code": None,
        "request_parameters": {
            "roleArn": "arn:aws:iam::160282065513:role/aws-service-role/resource-explorer-2.amazonaws.com/AWSServiceRoleForResourceExplorer"
        }
    }

]

def get_mock_events():
    return MOCK_EVENTS