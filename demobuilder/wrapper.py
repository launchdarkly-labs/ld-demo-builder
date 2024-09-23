import os
import sys
import json
from datetime import datetime
import randomname
import boto3
import DemoBuilder

LD_API_KEY = os.environ["LD_API_KEY"]
LD_API_KEY_USER = os.environ["LD_API_KEY_USER"]
ddb_table = boto3.resource("dynamodb").Table(os.environ["DDB_TABLE"])
logs = boto3.client("logs")


def lambda_handler(event, context):
    global LD_API_KEY
    global ddb_table
    global logs

    project_key = ""
    project_name = ""
    custom_name = ""

    body = json.loads(event["body"])

    if "action" not in body:
        return json.dumps({"statusCode": 400, "body": {"message": "Missing action"}})

    action = body["action"].lower()

    if "project-key" in body:
        project_key = body["project-key"].lower()

    if "customName" in body:
        custom_name = body["customName"]

    match action:
        case "build":
            if "email" not in body:
                return json.dumps(
                    {"statusCode": 400, "body": {"message": "Missing email"}}
                )
            email = body["email"].lower()
            create_project = False
            if project_key == "":
                create_project = True
                pname = randomname.get_name()
                project_key = "cxld-" + pname
                if custom_name != "":
                    project_name = custom_name
                else:
                    project_name = "Coast Demo (" + pname + ")"
            else:
                project_name = "Coast Demo (" + project_key.replace("cxld-", "") + ")"
            demo = DemoBuilder.DemoBuilder(
                LD_API_KEY, email, LD_API_KEY_USER, project_key, project_name
            )
            if create_project:
                demo.create_project()
            else:
                demo.project_created = True

            demo.create_flags()
            demo.create_segments()
            demo.create_metrics()
            demo.create_metric_groups()
            demo.run_experiment()
            demo.setup_release_pipeline()
            # demo.setup_flag_shortcuts()
            demo.update_add_userid_to_flags()

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
                    "UserId": email,
                    "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ExpRunning": False,
                    "EvalRunning": False,
                    "RGRunning": False,
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

            demo = DemoBuilder.DemoBuilder(
                LD_API_KEY, None, LD_API_KEY_USER, project_key, project_name
            )
            demo.cleanup()
            ddb_table.delete_item(Key={"ProjectKey": project_key})
            return json.dumps(
                {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Project deleted"}),
                }
            )
