config = {
    "interfaces": {
        "google.pubsub.v1.Publisher": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "http_get": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": [],
                "one_plus_delivery": [
                    "ABORTED", "CANCELLED", "DEADLINE_EXCEEDED", "INTERNAL",
                    "RESOURCE_EXHAUSTED", "UNAVAILABLE", "UNKNOWN"
                ]
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 60000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 60000,
                    "total_timeout_millis": 600000
                },
                "messaging": {
                    "initial_retry_delay_millis": 100,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 12000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 30000,
                    "total_timeout_millis": 600000
                }
            },
            "methods": {
                "CreateTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "UpdateTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "Publish": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "one_plus_delivery",
                    "retry_params_name": "messaging",
                    "bundling": {
                        "element_count_threshold": 10,
                        "element_count_limit": 1000,
                        "request_byte_threshold": 1024,
                        "request_byte_limit": 10485760,
                        "delay_threshold_millis": 10
                    }
                },
                "GetTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListTopics": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "ListTopicSubscriptions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "DeleteTopic": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "SetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "GetIamPolicy": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "TestIamPermissions": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
