EVENTS = [
    {
        "event_time": "2026-04-12 09:15:00",
        "event_name": "DescribeInstances",
        "event_source": "ec2.amazonaws.com",
        "username": "ops-sarah",
        "source_ip": "10.0.1.50",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-04-12 02:47:11",
        "event_name": "ConsoleLogin",
        "event_source": "signin.amazonaws.com",
        "username": "jdoe",
        "source_ip": "198.51.100.23",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-04-12 11:30:00",
        "event_name": "UpdateFunctionCode",
        "event_source": "lambda.amazonaws.com",
        "username": "dev-amira",
        "source_ip": "10.0.1.72",
        "error_code": None,
        "request_parameters": {
            "functionName": "order-processing"
        }
    },

    {
        "event_time": "2026-04-12 02:51:40",
        "event_name": "GetSecretValue",
        "event_source": "secretsmanager.amazonaws.com",
        "username": "jdoe",
        "source_ip": "198.51.100.23",
        "error_code": None,
        "request_parameters": {
            "secretId": "prod/database/master-password"
        }
    },

    {
        "event_time": "2026-04-12 12:00:00",
        "event_name": "AssumeRole",
        "event_source": "sts.amazonaws.com",
        "username": "N/A",
        "source_ip": "config.amazonaws.com",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-04-12 02:55:02",
        "event_name": "AttachUserPolicy",
        "event_source": "iam.amazonaws.com",
        "username": "jdoe",
        "source_ip": "198.51.100.23",
        "error_code": None,
        "request_parameters": {
            "userName": "jdoe",
            "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
        }
    },

    {
        "event_time": "2026-04-12 13:45:00",
        "event_name": "GetMetricData",
        "event_source": "monitoring.amazonaws.com",
        "username": "ops-sarah",
        "source_ip": "10.0.1.50",
        "error_code": None,
        "request_parameters": {}
    },

    {
        "event_time": "2026-04-12 02:58:30",
        "event_name": "StopLogging",
        "event_source": "cloudtrail.amazonaws.com",
        "username": "jdoe",
        "source_ip": "198.51.100.23",
        "error_code": None,
        "request_parameters": {
            "name": "management-events-trail"
        }
    },

    {
        "event_time": "2026-04-12 14:20:00",
        "event_name": "GetLogEvents",
        "event_source": "logs.amazonaws.com",
        "username": "dev-amira",
        "source_ip": "10.0.1.72",
        "error_code": None,
        "request_parameters": {
            "logGroupName": "/aws/lambda/order-processing"
        }
    },

    {
        "event_time": "2026-04-12 03:02:15",
        "event_name": "CreateUser",
        "event_source": "iam.amazonaws.com",
        "username": "jdoe",
        "source_ip": "198.51.100.23",
        "error_code": None,
        "request_parameters": {
            "userName": "backup-svc-account"
        }
    }

]