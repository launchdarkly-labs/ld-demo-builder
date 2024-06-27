import os
import sys
import json
from datetime import datetime
import randomname
import boto3
import DemoBuilder

LD_API_KEY = os.environ["LD_API_KEY"]
ddb_table = boto3.resource("dynamodb").Table(os.environ["DDB_TABLE"])
logs = boto3.client("logs")


def lambda_handler(event, context):
    global LD_API_KEY
    global ddb_table
    global logs

    project_key = ""
    project_name = ""

    body = json.loads(event["body"])

    if "action" not in body:
        return json.dumps({"statusCode": 400, "body": {"message": "Missing action"}})

    action = body["action"].lower()

    if "project-key" in body:
        project_key = body["project-key"].lower()

    match action:
        case "build":
            create_project = False
            if project_key == "":
                create_project = True
                pname = randomname.get_name()
                project_key = "cxld-" + pname
                project_name = "Coast Demo (" + pname + ")"
            else:
                project_name = "Coast Demo (" + project_key.replace("cxld-", "") + ")"
            demo = DemoBuilder.DemoBuilder(LD_API_KEY, project_key, project_name)
            if create_project:
                demo.create_project()
            else:
                demo.project_created = True

            demo.create_flags()
            demo.create_metrics()
            demo.create_metric_groups()
            demo.run_experiment()

            print(project_name)
            print(project_key)
            print(demo.client_id)
            print(demo.sdk_key)

            ddb_table.put_item(
                Item={
                    "ProjectKey": project_key,
                    "ProjectName": project_name,
                    "ClientId": demo.client_id,
                    "SdkKey": demo.sdk_key,
                    "UserId": "TDB",
                    "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

            return json.dumps(
                {
                    "statusCode": 200,
                    "body": {
                        "projectName": project_name,
                        "projectKey": project_key,
                        "clientId": demo.client_id,
                        "sdkKey": demo.sdk_key,
                    },
                }
            )
        case "cleanup":
            if project_key == "":
                return json.dumps(
                    {
                        "statusCode": 400,
                        "body": json.dumps({"message": "Missing project key"}),
                    }
                )
            if not project_key.startswith("cxld-"):
                return json.dumps(
                    {
                        "statusCode": 400,
                        "body": json.dumps(
                            {
                                "message": "This does not appear to be a Coast demo project."
                            }
                        ),
                    }
                )

            demo = DemoBuilder.DemoBuilder(LD_API_KEY, project_key, project_name)
            demo.cleanup()
            ddb_table.delete_item(Key={"ProjectKey": project_key})
            return json.dumps(
                {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Project deleted"}),
                }
            )