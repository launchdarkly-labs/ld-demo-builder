import os
import sys
import json
from datetime import datetime
import randomname
import boto3
import FinTechBuilder
import UserProfileBuilder

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
    demo_type = "FinTech"
    demo = None

    body = json.loads(event["body"])

    if "action" not in body:
        return json.dumps({"statusCode": 400, "body": {"message": "Missing action"}})

    action = body["action"].lower()

    if "project-key" in body:
        project_key = body["project-key"].lower()

    if "customName" in body:
        custom_name = body["customName"]

    if "demoType" in body:
        demo_type = body["demoType"]

    if "apiToken" in body:
        LD_API_KEY = body["apiToken"]

    match action:
        case "build":
            email = ""
            if "email" in body:
                email = body["email"].lower()
            # else:
            #     return json.dumps(
            #         {"statusCode": 400, "body": {"message": "Missing email"}}
            #     )

            pname = randomname.get_name().lower()
            if custom_name == "":
                project_name = "Coast Demo (" + pname + ")"
            else:
                project_name = custom_name

            create_project = False

            if project_key == "":
                create_project = True
                project_key = "cxld-" + pname
            else:
                project_name = "Coast Demo (" + project_key.replace("cxld-", "") + ")"

            print("Project Key: " + project_key)

            match demo_type.lower():
                case "userprofile":
                    demo_type = "UserProfile"
                    demo = UserProfileBuilder.UserProfileBuilder(
                        LD_API_KEY, email, LD_API_KEY_USER, project_key, project_name
                    )
                case _:
                    demo_type = "FinTech"
                    demo = FinTechBuilder.FinTechBuilder(
                        LD_API_KEY, email, LD_API_KEY_USER, project_key, project_name
                    )

            if not create_project:
                demo.project_created = True

            demo.build()

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
                    "DemoType": demo_type,
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
                        "demoType": demo_type,
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

            demo = FinTechBuilder.FinTechBuilder(
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
