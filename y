version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "AppCranealPatientDates"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-zbvoc7j5fftz"
s3_prefix = "AppCranealPatientDates"
region = "eu-central-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
parameter_overrides = "DynamoDBCreationParameter=\"0\""
